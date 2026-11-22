from odoo import models, fields


class Client(models.Model):
    _name = 'estate.client'
    _description = "Real Estate Client"
    _inherit = 'estate.owner'

