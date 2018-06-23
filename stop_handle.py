#! -*- coding: utf-8 -*-

import falcon
import start_handle
import gc


class stopHandle(object):
    # def __init__(self, annoy, wh_lines, start_pig):
    #     self.annoy = annoy
    #     self.wh_lines = wh_lines
    #     self.start_pig = start_pig

    def on_post(self, req, resp):
        # annoy = start_resource.start_Resource.annoy
        # wh_lines = start_resource.start_Resource.wh_lines
        # avg = start_resource.start_Resource.avg
        del start_handle.startHandle.annoy, start_handle.startHandle.wh_lines, start_handle.startHandle.avg
        gc.collect()
        print('server memory has been deleted and service stop!')
        resp.status = falcon.HTTP_200
