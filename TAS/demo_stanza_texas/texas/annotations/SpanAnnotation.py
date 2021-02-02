#!/usr/bin/python
#-*- coding: utf-8 -*-

from .Annotation import Annotation

class SpanAnnotation(Annotation):

    def __init__(self,pStartToken:int, pFinalToken:int, pLabel:str=""):
        self._type = "span"
        self._start_token = pStartToken
        self._final_token = pFinalToken
        self._label = pLabel

    def getStartToken(self):
        return self._start_token

    def getFinalToken(self):
        return self._final_token

    def getLabel(self):
        return self._label

    def jss(self):
        d = {}
        d["type"] = self._type
        d["label"] = self._label
        d["start_token"] = self._start_token
        d["final_token"] = self._final_token
        return d
