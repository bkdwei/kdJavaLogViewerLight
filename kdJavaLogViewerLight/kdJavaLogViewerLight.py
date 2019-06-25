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
from tkinter.simpledialog import askstring, askinteger

from kdGUI import *

from .exception_handler import set_global_callback
from .fileutil import check_and_create_sqlite_file, load_josn_config, save_json_config
from .kdJavaLogViewerLight_ui import kdJavaLogViewerLight_ui
from .log import log


class kdJavaLogViewerLight(kdJavaLogViewerLight_ui):
    '''
    classdocs
    '''
    show_import_info = kdSignal()

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        set_global_callback(self)

        self.last_dir = None
        check_and_create_sqlite_file(
            join(expanduser("~"), ".config/kdJavaLogViewerLight/data.db"))
        self.log = log()
        self.init_ui()
        self.bindEvent()

    def init_ui(self):
#         self.cb_keyword.addItems(['开始发送', "led显示信息", "确认上线", ""])
        self.config = load_josn_config(self.__class__.__name__)
        if self.config and "keyword"  in self.config:
            for word in self.config["keyword"] :
                if  word:
                    self.cb_keyword.addItem(word)
                else :
                    self.cb_keyword.addItem("")
            self.cb_keyword.setCurrentIndex(0)
        else:
            self.config = {"keyword" :[]}

    #             获取上一次打开的目录
    def get_last_dir(self):
        if self.last_dir:
            return self.last_dir
        else:
            return join(environ["CATALINA_HOME"], "logs")

    def bindEvent(self):
        self.pb_open_file.click(self.on_pb_open_clicked)
        self.pb_query.click(self.on_pb_query_clicked)
        self.pb_del_keyword.click(self.del_keyword)
        self.pb_add_keyword.click(self.add_keyword)
        self.show_import_info.connect(self.showMessage)
    
    def add_keyword(self):
        new_value = askstring(
            "新增关键字", "请输入你要保存的关键字")
        if new_value:
            self.config["keyword"].append(new_value)
            save_json_config(self.__class__.__name__, self.config)
            self.showMessage("新增关键字成功，" + new_value)
            self.cb_keyword.addItem(new_value)

    def del_keyword(self):
        curText = self.cb_keyword.currentText()
        if curText in self.config["keyword"] :
            self.config["keyword"].remove(self.cb_keyword.currentText())
            save_json_config(self.__class__.__name__, self.config)
            self.showMessage("删除关键字成功，" + curText)
        else:
            self.showMessage("关键字不在缓存中，" + curText)

    def on_pb_open_clicked(self):
        #         hour, ok = QInputDialog.getInt(
        # self, "导入指定小时之后的日志", "点击取消将导入全部日志。", 0, 0, 24, 1)
        hour = askinteger("导入指定小时之后的日志", "点击取消将导入全部日志")
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
            msg = ""
            l = f.readline()

            while l:
                #                     不以时间开头的行，默认不是一行
                if(l[0] != '2'):
                    msg += l
                    i += 1
                    l = f.readline()
                    continue
                # 跳过指定时间之前的日志
                elif hour and int(l[11:13]) < hour:
                    l = f.readline()
                    continue
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
                
                if i % 1000 == 0:
                    self.show_import_info.emit(l)
            if log_time:
                self.log.add_log(
                    log_time, thread_id, level, clazz, msg, short_clazz)
            self.log.flush_insert()
            end_time = time.time()
            self.showMessage(
                "导入日志成功，耗时" + str(end_time - begin_time) + "秒，行数:" + str(i))
            print("导入结束")
            f.close()

    def on_pb_query_clicked(self):
        self.showMessage("")
        begin_time = time.time()
        thread_id = self.le_prefex.text().strip() + \
            self.le_thread.text().strip()
        if thread_id == "T":
            thread_id = None
        keyword = self.cb_keyword.currentText()
        if keyword :
            keyword = keyword.strip()
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
#             msg = ""
#             for item in log_list:
#                 msg = msg + item[0] + " " + item[1] + " " + \
#                     item[2] + " [" + item[3] + "] " + item[4]
            msg = "".join([" ".join([item[0] , item[1] , item[2], item[3], item[4]]) for item in log_list])
            self.le_result.clear()
            self.le_result.setText(msg)
            end_time = time.time()
            if not keyword:
                keyword = ""
            self.showMessage("查询 " + keyword + " 成功，共" + str(len(log_list)) + "条，耗时" + str(end_time - begin_time) + "秒") 


def main():
    app = kdJavaLogViewerLight()
    app.showMaximized()
    app.run()

