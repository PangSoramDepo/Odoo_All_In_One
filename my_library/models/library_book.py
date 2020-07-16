from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from datetime import timedelta

class LibraryBook(models.Model):
    # translatable,name,required,related_sudo,compute_sudo
    _name           =   'library.book'
    _description    =   'Library Book'
    _order          =   'date_release desc,name'

    _rec_name       =   'short_name'
    _log_access     =   False

    name            =   fields.Char     ('Title', required=True)
    short_name      =   fields.Char     ('Short Title',translate=True,index=True)
    notes           =   fields.Text     ('Internal Notes')
    state           =   fields.Selection([('draft','Not Available'),('available','Available'),('lost','Lost')],'State',default='draft')
    description     =   fields.Html     ('Description',sanitize=True,strip_style=False)
    cover           =   fields.Binary   ('Book Cover')
    out_of_print    =   fields.Boolean  ('Out of Print?')
    date_release    =   fields.Date     ('Release Date')
    date_updated    =   fields.Datetime ('Last Updated')
    pages           =   fields.Integer  ('Number of Pages',groups='base.group_user',states={'lost':[('readonly',True)]},help='Total book page count',company_dependent=False)
    reader_rating   =   fields.Float    ('Reader Average Rating',digits=(14,4))
    author_ids      =   fields.Many2many('res.partner', string='Authors')
    active          =   fields.Boolean  ('Active',default=True)
    cost_price      =   fields.Float    ('Book Cost',dp.get_precision('Book Price'))
    currency_id     =   fields.Many2one ('res.currency',String="Currency")
    currency_price  =   fields.Monetary ('Retail Price')
    publisher_id    =   fields.Many2one ('res.partner',string="Publisher" #optional ondelete='set null' context={}, domain=[],
                                        )
    publisher_city  =   fields.Char     ('Publisher City',related='publisher_id.city',readonly=True)
    category_id     =   fields.Many2one ('library.book.category')
    age_days        =   fields.Float    (
                                            string='Days Since Release',
                                            compute='_compute_age', inverse='_inverse_age', search='_search_age',
                                            store=False,
                                            compute_sudo=False,)
    ref_doc_id      =   fields.Reference(selection='_referencable_models',string='Reference Document')

    class ResPartner(models.Model):
        _inherit            =   'res.partner'
        
        published_book_ids  =   fields.One2many('library.book','publisher_id',string='Published Books')
        authored_book_ids   =   fields.Many2many('library.book',string='Authored Books',#relation='library_book_res_partner_rel' #optional
                                                )

    _sql_constraints        =   [('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),('positive_page','CHECK(pages>0)','No of pages must be positive')]

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            delta = today - book.date_release
            book.age_days = delta.days

    # This reverse method of _compute_age. Used to make age_days field editable
    # It is optional if you don't want to make compute field editable then you can remove this
    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    # This used to enable search on copute fields
    # It is optional if you don't want to make enable search then you can remove this
    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]
    
    def name_get(self):
        result=[]
        for record in self:
            rec_name="{} ({})".format(record.name,record.date_release)
            result.append((record.id,rec_name))
        return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    @api.model
    def _referencable_models(self):
        models=self.env['ir.model'].search([('field_id.name','=','message_ids')])
        return [(x.model,x.name) for x in models]