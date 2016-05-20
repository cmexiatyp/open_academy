# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_session(self):
        return self.env['open_academy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2one('open_academy.session',
        string="Session", required=True , default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")