from odoo import models, fields, api, exceptions , tools
from odoo.addons import decimal_precision as dp
from datetime import timedelta
from openerp.exceptions import ValidationError, UserError
from odoo.tools.translate import _
import requests 
import logging

logger = logging.getLogger(__name__)

class LibraryBook(models.Model):
    # translatable,name,required,related_sudo,compute_sudo
    # To combine two recordset : r=r1+r2, r=r1 | r2 (no duplicate data), r=r1 & r2
    _name           =   'library.book'
    _inherit        =   ['base.archive']
    _description    =   'Library Book'
    _order          =   'date_release desc,name'
    # _columns        =   {'custom_title': fields.function(name_names, type='text', string='New Title')}

    _rec_name       =   'short_name'
    _log_access     =   False
    _sql_constraints=   [('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'),('positive_page','CHECK(pages>0)','No of pages must be positive')]

    name            =   fields.Char     ('Title', required=True)
    custom_name     =   fields.Char     ('Custom Title',compute='_compute_age',store=True)
    short_name      =   fields.Char     ('Short Titlerrrtg',translate=True,index=True)
    notes           =   fields.Text     ('Internal Notes')
    state           =   fields.Selection([('draft','Unavailable'),('available','Available'),('borrowed','Borrowed'),('lost','Lost')],'State',default='draft')
    description     =   fields.Html     ('Description',sanitize=True,strip_style=False)
    cover           =   fields.Binary   ('Book Cover')
    out_of_print    =   fields.Boolean  ('Out of Print?')
    date_release    =   fields.Date     ('Release Date')
    date_updated    =   fields.Datetime ('Last Updated')
    pages           =   fields.Integer  ('Number of Pages',groups='base.group_user',states={'lost':[('readonly',True)]},help='Total book page count',company_dependent=False)
    reader_rating   =   fields.Float    ('Reader Average Rating',digits=(14,4))
    author_ids      =   fields.Many2many('res.partner', string='Authors')
    otm_ids         =   fields.One2many ('res.partner','book_id', string='O2M')
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
    manager_remarks =   fields.Text('Manager Remarks')
    isbn            =   fields.Char('ISBN')
    old_edition     =   fields.Many2one('library.book',string="Old Edition")

    def name_names(self, cr, uid, ids, name, args, context=None):
        logger.info("-----------------------Jol Name------------------------------")
        res = {}
        for _obj in self.browse(cr, uid, ids, context=None):
            logger.info("-----------------------Obj------------------------------ {}".format(_obj))
            res[_obj.id] = _obj

        return res

    class ResPartner(models.Model):
        _inherit            =   'res.partner'
        _order              =   'display_name'
        
        book_id             =   fields.Many2one ('library.book',string="Yol Hay")
        published_book_ids  =   fields.One2many('library.book','publisher_id',string='Published Books')
        authored_book_ids   =   fields.Many2many('library.book',string='Authored Books',#relation='library_book_res_partner_rel' #optional
                                                )
        # count_books         =   fields.Integer('Number of Authored Books',compute='_compute_count_books',store=True)

        # @api.depends('authored_book_ids')
        # def _compute_count_books(self):
        #     for r in self:
        #         r.count_books=len(r.authored_book_ids)

    class BaseArchive(models.AbstractModel):
        _name               =   'base.archive'
        active              =   fields.Boolean('Base Active',default=True)

        def do_archive(self):
            for record in self:
                record.active=not record.active

    class LibraryMember(models.Model):
        _name               =   'library.member'
        _inherits           =   {'res.partner' : 'partner_id'}

        partner_id          =   fields.Many2one('res.partner',ondelete='casecade',#delegate=True ba dak deletegate not need inherits
                                )
        date_start          =   fields.Date('Member Since')
        date_end            =   fields.Date('Termination Date')
        member_number       =   fields.Char()
        date_of_birth       =   fields.Date('Date of birth')

        @api.model
        def get_all_library_member(self):
            library_member_model=self.env['library.member']
            return library_member_model.search([])

    @api.model
    def is_allowed_transition(self,old_state,new_state):
        allowed             =   [
            ('draft','available'),
            ('available','borrowed'),
            ('available','lost'),
            ('borrowed','lost'),
            ('borrowed','available'),
            ('lost','available')]
        return (old_state,new_state) in allowed
        
    @api.model
    def create(self,values):
        if not self.user_has_groups('my_library.group_librarian'):
            if 'manager_remarks' in values:
                raise UserError('Create: You are not allowed to modify manager_remarks')
        return super(LibraryBook,self).create(values)

    @api.multi
    def write(self,values):
        if not self.user_has_groups('my_library.group_librarian'):
            if 'manager_remarks' in values:
                del values['manager_remarks']
                # raise UserError('Write: You are not allowed to modify manager_remarks')
        return super(LibraryBook,self).write(values)

    @api.multi
    def name_get(self):
        result=[]
        for book in self:
            logger.info("---------------Context--------------{}".format(self.env.context.get('custom_search')))
            if self.env.context.get('custom_search', False):
                authors=book.author_ids.mapped('name')
                name='{} ({})'.format(book.name,', '.join(authors))
                result.append((book.id,name))
                logger.info("------------------------Parent Name Get If----------------------------")
            else:
                logger.info("------------------------Parent Name Get Else----------------------------")
                result.append((book.id,book.name))
        return result

    @api.model
    def _name_search(self,name='',args=None,operator='ilike',limit=100,name_get_uid=None):
        args=[] if args is None else args.copy()
        if not (name=='' and operator=='ilike'):
            args+=['|','|',('name',operator,name),('isbn',operator,name),('author_ids.name',operator,name)]
        return super(LibraryBook,self)._name_search(name=name,args=args,operator=operator,limit=limit,name_get_uid=name_get_uid)

    @api.model
    def _get_average_cost(self):
        grouped_result  =   self.read_group(
            [('cost_price','!=',False)],
            ['category_id','cost_price:avg'],
            ['category_id']
        )
        logger.info("----------Average Cost----------- {}".format(grouped_result))
        return grouped_result

    @api.model
    def update_book_price(self):
        logger.info('----------update_book_price called-----------')
        all_books =self.search([])
        for book in all_books:
            book.cost_price+=10

    # Update Data have 2 recipe like below :

    @api.multi
    def change_update_date_recipe_1(self):
        self.ensure_one()
        self.date_updated=fields.Datetime.now()

    @api.multi
    def change_update_date_recipe_2(self):
        self.ensure_one()
        self.update({
            'date_updated'  :   fields.Datetime.now(),
            'name'          :   'updated'
        })

    # End ------ Update Data have 2 recipe ------

    @api.multi
    def find_book(self):
        domain  =   ['|',
            '&',('name','like','Book Name'),
            ('category_id.name','ilike','Category Name'),
            '&',('name','ilike','Book Name 2'),
            ('category_id.name','ilike','Category Name 2')
        ]
        books=self.search(domain)
        logger.info('Books found: %s', books)
        return True

    @api.multi
    def find_partner(self):
        PartnerObj  =   self.env['res.partner']
        domain      =   ['&',('name','ilike','Parth Gajjar'),('company_id.name','=','Odoo')]
        partner     =   PartnerObj.search(domain)
        logger.info('Find Parner Execute found: %s', partner)

    @api.multi
    def return_all_books(self):
        self.ensure_one()
        wizard = self.env['library.return.wizard']
        values = {
            'borrower_id': self.env.user.partner_id.id,
        }
        specs = wizard._onchange_spec()
        updates = wizard.onchange(values, ['borrower_id'], specs)
        value = updates.get('value', {})
        for name, val in value.items():
            if isinstance(val, tuple):
                value[name] = val[0]
        values.update(value)
        wiz = wizard.create(values)
        return wiz.sudo().books_returns()

    @api.multi
    def change_state(self,new_state):
        for book in self:
            if book.is_allowed_transition(book.state,new_state):
                book.state=new_state
            else:
                msg = _('Moving from {} to {} is not allowed'.format(book.state,new_state))
                raise UserError(msg)
                
    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'
        if not self.env.context.get('avoid_deactivate'):
            self.active = False

    def post_to_webservice(self,data):
        try:
            req = requests.post('http://my-test-service.com',data=data,timeout=10)
            content = req.json()
        except IOError:
            error_msg=_("Something went wrong during data submission")
            raise UserError(error_msg)
        return content

    def average_book_occupation(self):
        sql_query = """
            SELECT
                lb.name,
                avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
            FROM
                library_book_rent AS lbr
            JOIN
                library_book as lb ON lb.id = lbr.book_id
            WHERE lbr.state = 'returned'
            GROUP BY lb.name;"""
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        logger.info("Average book occupation: %s", result)

    @api.onchange('date_release','custom_name')
    def _compute_age_onchange(self):
        logger.info("------------------------Onchange Execute DEPO-------------------------------")
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            delta = today - book.date_release
            book.age_days = delta.days
            # book.name=book.name+" Depo1"

    @api.multi
    @api.depends('name')
    def _compute_age(self):
        logger.info("------------------------Depends Execute DEPO-------------------------------")
        for book in self:
            book.custom_name="PoPo"

    # This reverse method of _compute_age. Used to make age_days field editable
    # It is optional if you don't want to make compute field editable then you can remove this
    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    # This used to enable search on compute fields
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
    
    # def name_get(self):
    #     result=[]
    #     for record in self:
    #         rec_name="{} ({})".format(record.name,record.date_release)
    #         result.append((record.id,rec_name))
    #     return result

    def mapped_book(self):
        all_books=self.search([])
        book_authors=self.get_author_names(all_books)
        logger.info('All Books : {}'.format(all_books))
        logger.info('Books Author: {}'.format(book_authors))

    def sort_book(self):
        all_books=self.search([])
        sort=self.sort_books_by_date(all_books)
        logger.info('Sort Books : {}'.format(sort))

    def book_rent(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError(_('Book is not avaible for renting'))
        rent_as_superuser = self.env['library.book.rent'].sudo()
        rent_as_superuser.create({
            'book_id': self.id,
            'borrower_id': self.env.user.partner_id.id,
        })

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    @api.model
    def _referencable_models(self):
        models=self.env['ir.model'].search([('field_id.name','=','message_id')])
        return [(x.model,x.name) for x in models]

    @api.model
    def get_author_names(self, books):
        return books.mapped('author_ids.name')

    @api.model
    def sort_books_by_date(self,books):
        return books.sorted(key='date_release',reverse=True)

    @api.model
    def books_with_multiple_authors(self,all_books):
        def predicate(book):
            if len(book.author_ids) > 1:
                return True
            return False
        return all_books.filter(predicate)

    # @api.model
    # def books_with_multiple_authors(self,all_books):
    #     return all_books.filter(lambda b: len(b.author_ids) > 1)