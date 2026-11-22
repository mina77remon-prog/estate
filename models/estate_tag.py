from odoo import models, fields


class Tag(models.Model):
    _name = 'estate.tag'
    _description = "Real Estate Tags"

    name = fields.Char(required=True)



