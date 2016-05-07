###########################################################################
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP.
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Carlos Fernando Mexia
#    Planified by: Moylop
#    Audited by:
# "les piratie este encabezado, me parecio bueno"
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
from openerp import fields, models

'''
    Este modulo nos va crear la vista principal de nuestro modulo de demo! openacademy. com!!

 '''

class curso(models.Model):
    '''
    course module
    '''
    _name = 'open_academy.course' ## modelo llamado open academy para el curso tecnico de moylop

    name = fields.Char(string='Title', required= True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users',# por convencion llamarlo nombrecamppo_id para saber que es un m2o
    					 on_delete="set null",## cuando el valor sea borrado de la base  de datos le arrojaremos un valor por defecto
    					 string="Responsable", index=True)

"""
Por convencion los nombres de las variables hay que setearlas en el idioma base del sistema
que es: ingles(us) 
"""