import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Property(models.Model):
    _name = 'estate.property'
    _log_access = True
    _description = "Real Estate Property"
    _inherit = ['mail.thread','mail.activity.mixin']




    ref = fields.Char(default='Property', readonly=True, copy=False)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=True)
    expected_selling_date = fields.Date()
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ])


    building_id = fields.Many2one('estate.building')

    owner_id = fields.Many2one('estate.owner')

    tag_ids = fields.Many2many('estate.tag')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')


    state = fields.Selection([
        ('draft','Draft'),
        ('pending', 'Pending'),
        ('sold','Sold'),
        ('closed', 'Closed'),
    ], default='draft')


    _sql_constraints = [
        ('property_name_unique','unique("name")','This name already exists!'),
    ]

    line_ids = fields.One2many('estate.property.line', 'property_id')
    active = fields.Boolean(default=True)




    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price


    @api.onchange('expected_price', 'selling_price')
    def _onchange_expected_price(self):
        for rec in self:
            if(rec.expected_price < rec.selling_price):
                return{'warning': {'title': 'Warning', 'message': 'Selling price is higher than expected price!', 'type': 'notification'}}

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError('Please enter a valid number of bedrooms!')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'
    @api.model
    def check_expected_selling_date(self):
        today = fields.Date.today()

        late = self.search([
            ('expected_selling_date', '<', today),
            ('state', 'not in', ('sold', 'closed'))
        ])

        late.write({'is_late': True})

        not_late = self.search([
            ('is_late', '=', True),
            '|', '|',
            ('expected_selling_date', '>=', today),
            ('expected_selling_date', '=', False),
            ('state', 'in', ('sold', 'closed'))
        ])

        not_late.write({'is_late': False})

    def action(self):
        _logger.info(self.env.user.name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            if vals.get('bedrooms', 0) <= 0:
                raise ValidationError('Please enter a valid number of bedrooms!')


            if not vals.get('ref') or vals['ref'] == 'Property':
                vals['ref'] = self.env['ir.sequence'].next_by_code('property_seq')
        return super().create(vals_list)


    def create_history_record(self, old_state, new_state):
        for rec in self:
            rec.env['estate.property.history'].sudo().create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
            })



class PropertyLine(models.Model):
    _name = 'estate.property.line'
    _description = "Real Estate Property Line"


    property_id = fields.Many2one('estate.property')
    area = fields.Float()
    description = fields.Char()
