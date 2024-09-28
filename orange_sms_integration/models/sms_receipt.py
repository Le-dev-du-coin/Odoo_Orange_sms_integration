from odoo import models, fields


class SMSReceipt(models.Model):
    _name = 'sms.receipt'
    _description = 'Orange SMS Delivery Receipt'

    sms_id = fields.Char(string="SMS ID", required=True)
    recipient_phone_number = fields.Char(string="Numéro de destinataire", required=True)
    delivery_status = fields.Char(string="Statut de livraison", required=True)
    received_at = fields.Datetime(string="Reçu à", default=fields.Datetime.now)