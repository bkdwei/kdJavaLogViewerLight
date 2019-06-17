'''
Created on 2019年6月17日

@author: bkd
'''
from .exception_handler import set_global_callback
from .kdJavaLogViewerLight_ui import kdJavaLogViewerLight_ui


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


def main():
    app = kdJavaLogViewerLight()
    app.run()
