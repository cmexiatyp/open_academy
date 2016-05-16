# -*- coding: utf-8 -*-
from openerp import api, exceptions, fields, models


class Session(models.Model):
    _name = "open_academy.session"

    name = fields.Char(requied=True)## cuando no defines un string, por default aplica formato al nombre de la variable Name quedaria
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6,2), help="duracion en dias")
    seats = fields.Integer(string="Numero de asientos en el curso")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')#podemos aplicar store=True
    instructor_id = fields.Many2one('res.partner',
                                    string="Instructor",
                                    on_delete="set null",
                                    index=True,
                                    domain=["|",
                                    ("instructor","=","True"),
                                    ("category_id","ilike","Teacher")],
                                    help="Recordad que al momento de crear el partner instructor")
                                    ##agregamos el dominio para que solo nos de a seleccionar partners que estan marcados
                                    ##como instructores o que contienen un tag teacher, Notese que utilizamos la notacion polaca
    course_id = fields.Many2one('open_academy.course',
                                on_delete="cascade",
                                string="Curso",
                                requied=True)
    attendes_ids = fields.Many2many('res.partner',
                                    string="Attendes")
  #                                 relation='open_academy_session_partner',
  #                                 column1='session_id', column2='partner_id', string="Attendes")
    active = fields.Boolean(default=True)
    #Este campo active es una palabra reservada, es decir la procesa orm para establecer un domino
    #con todos los elementros marcados con un true al momento de desplegar la vista default
    #asi mismo los active=False no apareceran de primera instancia en la vista a menos que los filtre


    @api.one #para que entre a cada uno de los registros
    @api.depends('seats','attendes_ids')#de que campos depende para llevar acabo la def
    def _taken_seats(self):
        if not self.seats:
            self.seats = 0
        else:
            self.taken_seats = 100.0 * len(self.attendes_ids) / self.seats

    @api.onchange('seats','attendes_ids')#campos que estamos monitoreando en el evento on change
    def _verify_valid_seats(self):
        if self.seats < 0:
            return{
                    'warning': {
                        'title': "Incorrect 'seats' value",
                        'message': "The numbers of available seats may not be negative"
                    }
            }
        if self.seats < len(self.attendes_ids):
            return {
                'warning': {
                    'title': "Too Many Attendes",
                    'message': "Increase seats or remove excess attendees",
                }
            }
    #los eventos on change se validan en el momento del cambio de valores en nuestros fields
    #en este caso estamos estamos programando un warning(no confundir con constrains) que nos 
    #informa que no estamos siguiendo el flujo deseado del modulo, este mensaje no necesariamente
    #tiene que ser un mensaje de error.
#python constrains
    @api.one
    @api.constrains('instructor_id','attendes_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id:
            raise exceptions.ValidationError("A session's instructor can't be an attendee")