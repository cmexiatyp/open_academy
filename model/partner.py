# -*- coding: utf-8 -*-
'''
    En este modelo estamos aplicando la herencia hacia el objeto base, res. partner y agregamos
    una relacion many to many junto con un boleano
'''
from openerp import fields,models

class partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('open_academy.session', string="attended sessions", readonly=True)

	