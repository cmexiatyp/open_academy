# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import api, exceptions, fields, models, _


class Session(models.Model):
    _name = "open_academy.session"

    name = fields.Char(requied=True)## cuando no defines un string, por default aplica formato al nombre de la variable Name quedaria
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6,2), help="duration in days")
    seats = fields.Integer(string="Numero de asientos en el curso")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')#podemos aplicar store=True
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
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
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')
    #este campo de tipo calculado va renderizar nuestra vista en gantt
    attendes_count = fields.Integer(string="Attendees Count",
        compute='_get_attendes_count', store=True)
    #este campo entero de tipo calculado se obtiene procesando la funcion_get_attendes_count abajo
    color = fields.Integer()
    #el campo color se requiere para que nos pueda almacenar el id del color que le defina el user via UI
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft', readonly=True)#si no agregas un string, la etiquta sera el nombre del campo

    #para almacenar los estados hay que crear estas funciones
    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

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
                        'title': _("Incorrect 'seats' value"),
                        'message': _("The numbers of available seats may not be negative") 
                    }
            }
        if self.seats < len(self.attendes_ids):
            return {
                'warning': {
                    'title': _("Too Many Attendes"),
                    'message': _("Increase seats or remove excess attendees"),
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
        if self.instructor_id and self.instructor_id in self.attendes_ids:
            raise exceptions.ValidationError("A session's instructor can't be an attendee")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1
    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24
    @api.one
    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('attendes_ids')
    def _get_attendes_count(self):
        self.attendes_count = len(self.attendes_ids)