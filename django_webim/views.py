#!/usr/bin/env python
#coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')
