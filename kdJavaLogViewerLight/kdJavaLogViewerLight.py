'''
Created on 2019年6月17日

@author: bkd
from os import environ
from os.path import expanduser, join
import sys, time
'''
from os import environ
from os.path import expanduser, join
import time
from tkinter.filedialog import LoadFileDialog

from .exception_handler import set_global_callback
from .fileutil import check_and_create_sqlite_file
from .kdJavaLogViewerLight_ui import kdJavaLogViewerLight_ui
from .log import log


class kdJavaLogViewerLight(kdJavaLogViewerLight_ui):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        set_global_callback(self)

        self.last_dir = expanduser("~")
        check_and_create_sqlite_file(
            join(expanduser("~"), ".config/kdJavaLogViewer/data.db"))
        self.log = log()
        self.bindEvent()

    #             获取上一次打开的目录
    def get_last_dir(self):
        if self.last_dir:
            return self.last_dir
        else:
            return join(environ["CATALINA_HOME"], "logs")

    def bindEvent(self):
        self.pb_open_file.click(self.on_pb_open_clicked)
        self.pb_query.click(self.on_pb_query_clicked)

    def on_pb_open_clicked(self):
        #         hour, ok = QInputDialog.getInt(
        # self, "导入指定小时之后的日志", "点击取消将导入全部日志。", 0, 0, 24, 1)
        fd = LoadFileDialog(self)
        selected_file = fd.go(
            dir_or_file=self.get_last_dir(), pattern="*.log")
        if selected_file:
            self.log.delete_all()
            self.showMessage("")
            begin_time = time.time()
            i = 1
            encoding = self.cb_encoding.currentText().strip()
            f = None
            if encoding == "":
                f = open(selected_file, "r")
            else:
                f = open(selected_file, "r",
                         encoding=encoding)

            log_time = None
            thread_id = None
            level = None
            clazz = None
            short_clazz = None
            msg = None
            l = f.readline()
            while l:
                #                     不以时间开头的行，默认不是一行
                if(l[0] != '2'):
                    msg += l
                    i += 1
                    l = f.readline()
                    continue
                # 跳过指定时间之前的日志
#                 elif int(l[11:13]) < hour and ok:
#                     l = f.readline()
#                     continue
                else:
                    #                         print(log_time, thread_id, level, clazz, msg)
                    if log_time:
                        self.log.add_log(
                            log_time, thread_id, level, clazz, msg, short_clazz)
                    log_time = l[11:23]
                    thread_id = l[24:28]
                    level = l[29:35]
                    ll = str(l[35:]).split(']')
                    clazz = ll[0][2:]
                    short_clazz = clazz.split(".")[-1]
                    msg = ll[1][2:]
                    l = f.readline()
                i += 1
            if log_time:
                self.log.add_log(
                    log_time, thread_id, level, clazz, msg, short_clazz)
            self.log.flush_insert()
            end_time = time.time()
            self.showMessage(
                "导入日志成功，耗时" + str(end_time - begin_time) + "秒，行数:" + str(i))
            f.close()

    def on_pb_query_clicked(self):
        self.showMessage("")
        thread_id = self.le_prefex.text().strip() + \
            self.le_thread.text().strip()
        if thread_id == "T":
            thread_id = None
        keyword = self.le_keyword.text().strip()
        short_clazz = self.le_method.text().strip()
        start_time = self.te_start.text()
        end_time = self.te_end.text()
        level_list = []
#         if self.cb_debug.isChecked():
#             level_list.append("DEBUG")
#         if self.cb_info.isChecked():
#             level_list.append("INFO")
#         if self.cb_warn.isChecked():
#             level_list.append("WARN")
#         if self.cb_error.isChecked():
#             level_list.append("ERROR")
        if any([thread_id != "", keyword != ""]):
            log_list = self.log.query(
                thread_id, keyword, short_clazz, start_time, end_time, level_list)
            if not log_list:
                self.showMessage("查询结果为空")
                return
            self.log_list = log_list
            msg = ""
            for item in log_list:
                msg = msg + item[0] + " " + item[1] + " " + \
                    item[2] + " [" + item[3] + "] " + item[4]
            self.le_result.clear()
            self.le_result.setText(msg)
            self.showMessage("查询 " + keyword + " 成功")


def main():
    app = kdJavaLogViewerLight()
    app.showMaximized()
    app.run()
