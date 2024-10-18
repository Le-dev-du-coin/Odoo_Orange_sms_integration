from odoo import models, fields, api
import json
from odoo.exceptions import UserError

class SMSReceipt(models.Model):
    _name = 'sms.delivery.receipt'
    _description = 'Accusé de réception SMS'

    recipient_phone_number = fields.Char(string="Numéro de téléphone", required=True)
    delivery_status = fields.Selection([
        ('DeliveredToTerminal', 'Livré au terminal'),
        ('DeliveryImpossible', 'Livraison impossible'),
        ('Pending', 'En attente')
    ], string="Statut de livraison", required=True)
    message_id = fields.Char(string="ID du message", required=True)
    date_received = fields.Datetime(string="Date de réception", default=fields.Datetime.now)
