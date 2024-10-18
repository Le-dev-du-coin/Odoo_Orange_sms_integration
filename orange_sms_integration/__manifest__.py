{
    'name': 'Orange SMS Integration',
    'version': '17.0.0',
    'category': 'Extra tools',
    'summary': 'Orange\'s SMS API Integration',
    'description': """
                SMS module for sending sms with Orange\'s SMS API
                """,
    'author': 'Social360',
    'website': 'www.social360mali.com',
    'license': 'AGPL-3',
    'depends': ['base', 'sms'],
    "data": [
        "views/sms_config_settings_views.xml",
        "security/ir.model.access.csv",
        "views/sms_sender_views.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}