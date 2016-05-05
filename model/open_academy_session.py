# -*- coding: utf-8 -*-
from openerp import fields, models

class Session(models.model):
    _name = "open_academy.Session"

    name = fields.Char(requied=True)## cuando no defines un string, por default aplica formato al nombre de la variable Name quedaria
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), help="duracion en dias")
    seats = fields.Integer(string="Numero de asientos en el curso")