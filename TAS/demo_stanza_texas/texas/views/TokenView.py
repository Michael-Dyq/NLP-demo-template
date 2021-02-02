#!/usr/bin/python
#-*- coding: utf-8 -*-

from .AnnotationView import AnnotationView

class TokenView(AnnotationView):

    def __init__(self, pName:str):
        # automatically set type as "TokenView"
        super(TokenView, self).__init__(pName = pName, pType = "AnnotationView"+"."+"TokenView")
