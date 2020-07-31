from odoo import api, fields, models

class res_company(models.Model):
    _inherit = 'res.company'

    show_all_record   = fields.Boolean(string="Show All Record",readonly=False)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_self_borrow = fields.Boolean(string="Self borrow", implied_group='my_library.group_self_borrow')
    show_all_record   = fields.Boolean(string="Show All Record",related="company_id.show_all_record",readonly=False)