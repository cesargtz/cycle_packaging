# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from openerp.exceptions import ValidationError

class SaleOrderPackaging(models.Model):
    _inherit = 'sale.order'

    packaging_count = fields.Integer(compute="_packaging_count",string="Centro de envases")

    def action_confirm(self):
        res = super(SaleOrderPackaging,self). action_confirm()
        # packaging = self.env['cycle.packaging'].search(('sale_order','=',self.id),('state','=','open'))
        # if len(packaging):
        #     raise exceptions.ValidationError("Existen envases sin regresar.")
        for line in self.order_line:
            if line.product_id.product_tmpl_id.reusable:
                packaging_id = self.env['cycle.packaging'].create({
                    'sale_order' : self.id,
                    'product': line.product_id.product_tmpl_id.container.id,
                    'quantity':line.product_uom_qty,
                    'pending':line.product_uom_qty,
                    'date': self.date_order,
                    'state':'open',
                })
        return res


    def _packaging_count(self):
        for line in self:
            count = 0
            for itr in self.env['cycle.packaging'].search([('sale_order','=', self.id)]):
                if itr.state in ['open','incomplete']:
                    count = itr.pending + count
        self.packaging_count = count


    def sale_order_tree(self):
        return{
                'name'          :   'Ciclo de envases',
                'type'          :   'ir.actions.act_window',
                'view_type'     :   'form', #Tampilan pada tabel pop-up
                'view_mode'     :   'tree,form', # Menampilkan bagian yang di pop up, tree = menampilkan tabel tree nya utk product
                'res_model'     :   'cycle.packaging', #Menampilkan tabel yang akan di show di pop-up screen
                'domain'        :   [('sale_order.id','=', self.id)], #Filter id barang yang ditampilkan
                # 'target'        :   'new',
            }
            #     'views'         :   [(tree_id, 'tree'),(form_id, 'form')],
  
class ResPartnerPackaging(models.Model):
    _inherit = 'res.partner'

    packaging_count = fields.Integer(compute="_packaging_count",string="Centro de envases")

    
    def _packaging_count(self):
        for line in self:
            count = 0
            for itr in self.env['cycle.packaging'].search([('partner','=', self.id),('state','not in',['done','draft'])]):
                count = itr.pending + count
        self.packaging_count = count


    def res_partner_tree(self):
        return{
            'name'          :   'Ciclo de envases',
            'type'          :   'ir.actions.act_window',
            'view_type'     :   'form', #Tampilan pada tabel pop-up
            'view_mode'     :   'tree,form', # Menampilkan bagian yang di pop up, tree = menampilkan tabel tree nya utk product
            'res_model'     :   'cycle.packaging', #Menampilkan tabel yang akan di show di pop-up screen
            'domain'        :   [('partner.id','=', self.id),('state','not in',['done','draft'])], #Filter id barang yang ditampilkan
        }


class StockPickingPackaging(models.Model):
    _inherit = 'stock.picking'

    center_packaging = fields.One2many('cycle.packaging','name', string="Centro de envases", compute="_get_packaging")  

    def _get_packaging(self):
        if self.origin != '':
            partner = self.env['sale.order'].search([('name','=',self.origin)]).partner_id.id
            order_packaging = self.env['cycle.packaging'].search([('partner','=',partner),('state','in',['open','incomplete'])])
            self.center_packaging = order_packaging