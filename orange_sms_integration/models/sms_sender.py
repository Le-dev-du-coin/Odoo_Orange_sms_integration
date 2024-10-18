from odoo import models, fields


class SMSSender(models.Model):
    _name = 'sms.sender'
    _description = 'Historique des SMS envoyés'

    message_id = fields.Char(string="SMS ID", required=True)
    recipient_phone_number = fields.Char(string="Numéro de destinataire", required=True)
    message = fields.Text(string="Message", required=True)
    sent_at = fields.Datetime(string="Envoyé le", default=fields.Datetime.now)
