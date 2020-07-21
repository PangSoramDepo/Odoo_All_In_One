# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

# class my_library_return(models.Model):
#     _name = 'my_library_return.my_library_return'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class LibraryBook(models.Model):
    _inherit    =   'library.book'

    date_return =   fields.Date('Date To Return')

    def make_borrowed(self):
        day_to_borrow   =   self.category_id.max_borrow_days or 10
        self.date_return = fields.Date.today() + timedelta(days=day_to_borrow)
        return super(LibraryBook,self).make_borrowed()

    def make_available(self):
        self.date_return    =   False
        return super(LibraryBook,self).make_available()

class LibraryBookCategory(models.Model):
    _inherit    =   'library.book.category'

    max_borrow_days =   fields.Integer('Maximun borrow days',help='For how many days book can be borrowed',default=10)