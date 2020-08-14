from odoo import api, fields, models
import logging

logger = logging.getLogger(__name__)

class test_book(models.Model):
    _name   =   "test.book"
    _description="Test ng eng"

    temp=None

    depo_id =   fields.Many2one('library.book',string="ManyPiOne")
    otm_id  =   fields.One2many('res.partner',compute='_compute_partner',string="Partner",inverse="_inverse_otm")

    @api.multi
    @api.onchange('depo_id')
    def _compute_partner(self):
        logger.info("------------------------Depends Test DEPO-------------------------------")
        if self.depo_id:
            logger.info("------------------------Depends Test DEPO 0 {}-------------------------------".format(self.depo_id))
            logger.info("------------------------Depends Test DEPO 1 {}-------------------------------".format(self.depo_id.otm_ids))
            self.temp=self.depo_id.otm_ids
            self.otm_id=self.depo_id.otm_ids
    def _inverse_otm(self):
        logger.info("------------------------Depends Inverse DEPO-------------------------------")
    @api.model
    def create(self, vals):
        rec=super(test_book,self).create(vals)
        logger.info("------------------------Depends create DEPO-------------------------------")
        logger.info("------------------------Depends Rec {}-------------------------------".format(rec))
        logger.info("------------------------Depends Rec 1 {}-------------------------------".format(rec.depo_id))
        logger.info("------------------------Depends Rec 2 {}-------------------------------".format(rec.otm_id))

        self.env['library.book'].browse(vals['depo_id']).update({'otm_ids':rec.otm_id})
        logger.info("------------------------Depends Test Temp {}-------------------------------".format(self.temp))
        logger.info("------------------------Depends Test DEPO 0 {}-------------------------------".format(self.otm_id))
        logger.info("------------------------Depends Test DEPO 1 {}-------------------------------".format(vals))
        logger.info("------------------------Depends Test DEPO 2 {}-------------------------------".format(self))
        logger.info("------------------------Depends Test DEPO 3 {}-------------------------------".format(self.depo_id))
        logger.info("------------------------Depends Test DEPO 4 {}-------------------------------".format(vals['depo_id']))
        logger.info("------------------------Depends Test DEPO 5 {}-------------------------------".format(self.browse(vals['depo_id'])))
        # logger.info("------------------------Depends Test DEPO 6 {}-------------------------------".format(self.browse(vals['depo_id']).otm_id))
        return rec

    @api.multi
    def write(self,vals):
        rec=super(test_book,self).write(vals)
        self.depo_id.update({'otm_ids':vals['otm_id']})
        logger.info("------------------------Depends write DEPO-------------------------------")
        logger.info("------------------------Depends self {}-------------------------------".format(self))
        logger.info("------------------------Depends id {}-------------------------------".format(self.depo_id))
        logger.info("------------------------Depends value {}-------------------------------".format(vals))
        logger.info("------------------------Depends rec {}-------------------------------".format(rec))
        # logger.info("------------------------Depends rec {}-------------------------------".format(rec.otm_id))
        return rec