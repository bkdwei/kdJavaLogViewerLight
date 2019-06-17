
from kdGUI import *
from tkinter.constants import NO


class kdJavaLogViewerLight_ui(Window):

    def __init__(self):
        super().__init__()

        self.setTitle("kdJava日志查看器")

        self.query_layout = GridLayout('导入和查询', self)
        self.addWidget(self.query_layout)

#         第一行
        self.pb_open_file = PushButton(
            '打开日志文件', self.query_layout)
        self.query_layout.addWidget(self.pb_open_file, 0, 0)
        self.Label_0 = Label('编码格式', self.query_layout)
        self.query_layout.addWidget(self.Label_0, 0, 3)
        self.le_encoding = LineEdit(
            'UTF-8', self.query_layout)
        self.query_layout.addWidget(self.le_encoding, 0, 4)
        self.pb_query = PushButton(
            '查询', self.query_layout)
        self.query_layout.addWidget(self.pb_query, 0, 5)

#         第二行

        self.Label_0 = Label('开始时间', self.query_layout)
        self.query_layout.addWidget(self.Label_0, 1, 0)
        self.te_start = LineEdit(
            '00:00:00', self.query_layout)
        self.query_layout.addWidget(self.te_start, 1, 1)
        self.Label_1 = Label('结束时间', self.query_layout)
        self.query_layout.addWidget(self.Label_1, 1, 3)
        self.te_end = LineEdit(
            '00:00:00', self.query_layout)
        self.query_layout.addWidget(self.te_end, 1, 4)

#         第三行
        self.Label_2 = Label('线程号前缀', self.query_layout)
        self.query_layout.addWidget(self.Label_2, 2, 0)
        self.le_prefex = LineEdit('T', self.query_layout)
        self.query_layout.addWidget(self.le_prefex, 2, 1)
        self.Label_3 = Label('线程号', self.query_layout)
        self.query_layout.addWidget(self.Label_3, 2, 3)
        self.le_thread = LineEdit(
            '', self.query_layout)
        self.query_layout.addWidget(self.le_thread, 2, 4)

#         第四行
        self.Label_4 = Label('方法', self.query_layout)
        self.query_layout.addWidget(self.Label_4, 3, 0)
        self.le_method = LineEdit(
            '', self.query_layout)
        self.query_layout.addWidget(self.le_method, 3, 1)
        self.Label_5 = Label('关键字', self.query_layout)
        self.query_layout.addWidget(self.Label_5, 3, 3)
        self.le_keyword = LineEdit(
            '开始发送', self.query_layout)
        self.query_layout.addWidget(self.le_keyword, 3, 4)

        self.hl_result = HorizontalLayout('结果', self)
        self.addWidget(self.hl_result, expand=YES)
        self.le_result = Text(self.hl_result)
        self.hl_result.addWidget(self.le_result)


if __name__ == '__main__':
    app = kdJavaLogViewerLight_ui()
    app.run()
