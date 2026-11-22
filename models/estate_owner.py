from odoo import models, fields


class Owner(models.Model):
    _name = 'estate.owner'
    _description = "Real Estate Owner"

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Char()

    property_ids = fields.One2many('estate.property','owner_id')

