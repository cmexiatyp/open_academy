# -*- coding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP.
#    All Rights Reserved
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
{
    'name': 'Modulo',
    'suammary': """ Gestionar Entrenamientos!""", 
    'version': '1.0',
    #Las categorias las utilizamos para filtrar dentro de los modulos
    'category': 'Test',
    'description': """

        Este modulo es concebido para hacer los primeros pasos en odoo version 8
        -Agregar Vistas (XML)
        -Cargar datos por default (DATA DEMO)
        -Crear reglas de acceso (ACL)
        -Procesos y objectos (Python)
    """,
    'author': 'Fernando Mexia',
    'website':'www.typrefrigeracion.com.mx',
    #Modulos de los cuales depende nuestro modulo, esto es como una especie de base en la que trabajaremos, siempre tendremos almenos
    #la dependencia base ( modulo core)!
    'depends': ['base'],
    'data': [
        #aqui por ejemplo podemos insertar un archivo .csv con las ACL que nos ayudaran a restringir acciones en nuestro modulo
        #asi como filtrar usuarios  'security/ir.model.access.csv',
        #Tambien podemos añadir un xml con datos por default    'template.xml',
        'view/open_academy_course_view.xml', #xml con las vistas padres
        'view/open_academy_session_view.xml',#xml con vistas child, tener cuidado con esto ya que si se antepone una vista child a una parent, nos marca error
                ],
    'update_xml': [
        #'vista.xml',
        ],
    #Estos son datos que se cargan solamente si aplicamos el flag de instalar datos de demostracion al crear una BD nueva        
    'demo': [
        #'demo.xml',
        'data/demo.xml',
    ],
    'installable': True,
    'active': False,
    'certificate' : False,
}