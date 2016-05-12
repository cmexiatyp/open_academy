# -*- coding: utf-8 -*-
from openerp import fields, models

class Session(models.Model):
    _name = "open_academy.session"

    name = fields.Char(requied=True)## cuando no defines un string, por default aplica formato al nombre de la variable Name quedaria
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), help="duracion en dias")
    seats = fields.Integer(string="Numero de asientos en el curso")
    instructor_id = fields.Many2one('res.partner',
    								string="Instructor",
    								on_delete="set null",
    								index=True)
    course_id = fields.Many2one('open_academy.course',
    							on_delete="cascade",
    							string="Curso",
    							requied=True)
    attendes_ids = fields.Many2many('res.partner', string="Attendes")