{
    'name' : 'Real Estate',
    'version' : '1.0',
    'author' : 'MR M',
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['sale_management','mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/estate_property_view.xml',
        'views/estate_owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/estate_building_view.xml',
        'views/estate_property_history_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {'web.assets_backend': ['estate/static/src/css/property.css']},
    'application': True,
}









