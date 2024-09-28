import requests
import base64
import time
from odoo import models, fields, api
from odoo.exceptions import UserError

class SMSApi(models.Model):
    _inherit = 'sms.api'

    _name = 'sms.orange'
    _description = 'Orange SMS API Integration'

    name = fields.Char(string='Nom')
    client_id = fields.Char(string='ID du client', required=True)
    client_secret = fields.Char('Client secret', required=True)
    api_key = fields.Char('Clé API')
    sender_name = fields.Char('Nom Expediteur')
    sender_number = fields.Char('Numéro Expediteur')
    access_token = fields.Char('Access Token')
    token_expiration = fields.Float('Temps d\'expiration du Token', help="Compteur pour expiration du Token")

    def get_access_token(self):
        """
        Obtention du nouveau Token si le Token est manquant ou expiré.
        """
        current_time = time.time()
        if not self.access_token or current_time >= self.token_expiration:
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
                self.token_expiration = time.time() + token_data.get('expires_in', 3600) - 60  # Expiration moins 1 min
            else:
                raise UserError(f"Erreur lors de la récupération du token : {response.text}")

        return self.access_token

    def send_sms(self, recipient_phone_number, message):
        """
        Redéfinition de la méthode send_sms pour envoyer des SMS via l'API Orange.
        """
        self.ensure_one()
        access_token = self.get_access_token()  # S'assurer que le token existe et est valide

        url = f"https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{self.sender_number}/requests"

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "outboundSMSMessageRequest": {
                "address": f"tel:+{recipient_phone_number}",
                "senderAddress": f"tel:+{self.sender_number}",
                "senderName": self.sender_name,
                "outboundSMSTextMessage": {
                    "message": message
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 201:
            raise UserError(f"Erreur lors de l'envoi du SMS : {response.text}")
        return response.json()

    def check_sms_balance(self):
        """
        Méthode pour vérifier le solde de SMS disponible via l'API Orange.
        """
        access_token = self.get_access_token()  # S'assurer que le token est valide

        url = "https://api.orange.com/sms/admin/v1/contracts"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise UserError(f"Erreur lors de la vérification du solde SMS : {response.text}")
