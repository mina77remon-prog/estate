from odoo import models, fields

class PropertyHistory(models.Model):
    _name = 'estate.property.history'
    _description = "Real Estate Property History"

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('estate.property', ondelete='cascade')
    old_state = fields.Char()
    new_state = fields.Char()


