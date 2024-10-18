from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import time
import requests
import logging

class SmsOrange(models.Model):
    _name = 'sms.orange'
    _description = 'Orange SMS API Config'
    _inherit = ['sms.api.orange.base']

    _logger = logging.getLogger(__name__)
    name = fields.Char(string='Nom')
    client_id = fields.Char(string='ID du client', required=True)
    client_secret = fields.Char(string='Client secret', required=True)
    sender_name = fields.Char(string='Nom Expediteur')
    sender_number = fields.Char(string='Numéro Expediteur')
    access_token = fields.Char(string='Access Token')
    token_expiration = fields.Float(string='Expiration du Token', help="Compteur pour expiration du Token")
    
    def get_access_token(self):
        """Obtenir un access token valide ou en générer un nouveau"""
        current_time = time.time()

        if not self.access_token or current_time >= self.token_expiration:
            # Encode les informations client_id et client_secret en base64
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_header = base64.b64encode(auth_string.encode()).decode()

            url = "https://api.orange.com/oauth/v3/token"
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            data = {
                "grant_type": "client_credentials"
            }
            response = requests.post(url, headers=headers, data=data)

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                self.token_expiration = time.time() + token_data.get('expires_in', 3600) - 60  # Expiration -1 min
            else:
                error_message = response.json().get('error_description', response.text)
                raise UserError(f"Erreur lors de la récupération du token : {response.text}")
        print('Token=', self.access_token)
        return self.access_token