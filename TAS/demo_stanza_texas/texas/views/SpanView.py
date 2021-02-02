#!/usr/bin/python
#-*- coding: utf-8 -*-

from .AnnotationView import AnnotationView

class SpanView(AnnotationView):

    def __init__(self, pName:str):
        # automatically set type as "SpanView"
        super(SpanView, self).__init__(pName = pName, pType = "AnnotationView"+"."+"SpanView")
