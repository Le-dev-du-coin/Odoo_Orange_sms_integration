from odoo import models, fields, api

class SmsBalance(models.TransientModel):
    _name = 'sms.balance'
    _description = 'Solde SMS'

    balance_info = fields.Text(string='Informations Solde SMS')

    @api.model
    def default_get(self, fields):
        res = super(SmsBalance, self).default_get(fields)
        balance_data = self.env['sms.orange'].check_sms_balance()  
        res['balance_info'] = str(balance_data)  # Stocker la réponse API dans un champ Text
        return res
