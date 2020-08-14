from odoo import api, fields, models
import logging

logger = logging.getLogger(__name__)

class test_book(models.Model):
    _name   =   "test.book"
    _description="Test ng eng"

    depo_id =   fields.Many2one('library.book',string="ManyPiOne")
    otm_id  =   fields.One2many('res.partner',compute='_compute_partner',string="Partner",inverse="_inverse_otm")

    @api.multi
    @api.onchange('depo_id')
    def _compute_partner(self):
        if self.depo_id:
            self.otm_id=self.depo_id.otm_ids

    def _inverse_otm(self):
        logger.info("------------------------Depends Inverse DEPO-------------------------------")

    @api.model
    def create(self, vals):
        rec=super(test_book,self).create(vals)
        self.env['library.book'].browse(vals['depo_id']).update({'otm_ids':rec.otm_id})
        return rec

    @api.multi
    def write(self,vals):
        rec=super(test_book,self).write(vals)
        self.depo_id.update({'otm_ids':vals['otm_id']})
        return rec