#!/usr/bin/python
#-*- coding: utf-8 -*-

from .SpanView import SpanView
from texas.annotations.SpanAnnotation import SpanAnnotation

class Sentences(SpanView):
    def __init__(self):
        # automatically name "SENTENCES" and set type as "SpanView" 
        super(Sentences, self).__init__(pName = "SENTENCES")

    def add(self,pStartToken:int, pFinalToken:int, pLabel:str = ""):
        self.getAnnSet().add ( SpanAnnotation(pStartToken, pFinalToken, pLabel) )
