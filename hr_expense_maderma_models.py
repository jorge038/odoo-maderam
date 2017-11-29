#-*- coding: utf-8 -*-
import itertools
from lxml import etree
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

class hr_expense_expense(models.Model):                 
        _inherit = 'hr.expense.expense'                 #Decimos que sera extension del modeolo hr.expense.expense
        @api.depends('line_ids')                                                #Reescribimos el metodo _amount que es de hr_expense class hr_expense_expense
        def _amount(self):
                        for expense in self:
                                total = 0.0
                                for line in expense.line_ids:
                                        total += line.unit_amount * line.unit_quantity * (1 + line.product_id.supplier_taxes_id.amount)
        state_ids = fields.Many2one(comodel_name='res.country.state',string='Ciudad')           #Creamos el campo state ids que tiene referencia de modelo res.country.state
        partner_ids = fields.Many2many(comodel_name='res.partner',string='Clientes')
        motivos  = fields.Selection([                                                           #Creamos el campo tipo seleccion motivo de gasto
                ('viaje','Viaje'),
                ('junta de vendedores','Junta de vendedores'),
                ('congreso','Congreso'),
                ('revisita','Revisita'),
                ('evento','Evento con cliente'),
                ('capacitacion','Capacitacion')
                ],'',help='Motivo de gasto')
        amount = fields.Float(compute='_amount',store=True)                     


class hr_expense_line(models.Model):
        _inherit = "hr.expense.line"
        @api.depends('product_id','unit_amount')
        def _tax_line(self):
                        for line in self:

                                tax = 0.0
                                for l in line.product_id.supplier_taxes_id:
                                        tax += l.amount * line.unit_amount
                                line.tax_line=tax
        tax_line=fields.Float(compute='_tax_line',store=True)           
