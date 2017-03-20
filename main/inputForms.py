# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:38:19 2017

@author: xuke2
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, RadioField      
from wtforms.validators import DataRequired

class singleStockForm(Form):
    choices=[('random_strategy','随机'),('smacross_strategy', 'SMA交叉'),('bband_strategy','布林格区间'),('donchain_strategy','唐奇安通道')]
    stockId = StringField('stockId', validators=[DataRequired()])
    initMoney = IntegerField('initMoney', validators=[DataRequired()])
    startDate = DateField('startDate', format = '%Y-%m-%d')
    endDate = DateField('endDate', format = '%Y-%m-%d')
    enterStr = RadioField('enterStr', choices=choices, validators=[DataRequired()])
    exitStr = RadioField('exitStr', choices=choices, validators=[DataRequired()])
    
    smaShort= IntegerField('smaShort')
    smaLong = IntegerField('smaLong')
    donChianShort = IntegerField('donChianShort')
    donChianLong = IntegerField('donChianLong')
    bbandDay = IntegerField('bbandDay')