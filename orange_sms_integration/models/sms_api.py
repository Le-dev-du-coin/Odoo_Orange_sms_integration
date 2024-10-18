import requests
import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SmsApiOrangeBase(models.AbstractModel):
    _name = 'sms.api.orange.base'
    _inherit = 'sms.api' 
    _description = 'Base Orange SMS API Integration'

    def validate_number(self, number):
       
        if not isinstance(number, str) or not re.match(r"^\d{1,3}\d{9,12}$", number):
            raise UserError(_("Le numéro de téléphone doit être une chaîne de caractères et inclure un indicatif valide (par exemple : 223XXXXXXXX)."))


        # Vérification pour s'assurer que le numéro est compris entre 10 et 15 chiffres
        if not (9 <= len(number) <= 15):
            raise UserError(_("Le numéro de téléphone doit être entre 9 et 15 caracteres."))

    def _send_sms(self, number, message):
        """Redéfinition de la méthode _send_sms pour envoyer un SMS via l'API Orange."""
        
        # Validation des numéros avant envoi
        number =  str(number)
        self.validate_number(number)

        access_token = self.get_access_token()


        url = f"https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{str(self.sender_number)}/requests"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Ajout de l'indicatif téléphonique pour l'API si nécessaire
        payload = {
            "outboundSMSMessageRequest": {
                "address": f"tel:+{str(number)}", 
                "senderAddress": f"tel:+{str(self.sender_number)}",
                #"senderName": self.sender_name,
                "outboundSMSTextMessage": {
                    "message": str(message)
                },
                "deliveryReceiptRequest": "true",
                "notifyURL": "https://extranet-phoenixpharma.com//orange/smsdr"  # URL où l'API enverra l'accusé
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 201:
            # Utilisation de messages d'erreur plus spécifiques
            error_message = response.json().get('error_description', response.text)
            raise UserError(f"Erreur lors de l'envoi du SMS : {error_message}")
            print('Reponse:', response.json())
        
        return response.json()

    def _send_sms_batch(self, messages):
        """Redéfinition de la méthode _send_sms_batch pour envoyer des SMS en mode batch."""
        access_token = self.get_access_token()
        
        url = f"https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{self.sender_number}/requests"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Validation de tous les numéros avant envoi
        for msg in messages:
            self.validate_number(str(msg['number']))

        payload = {
            "outboundSMSMessageRequest": [
                {
                    "address": f"tel:+{str(msg['number'])}",
                    "senderAddress": f"tel:+{str(self.sender_number)}",
                    #"senderName": self.sender_name,
                    "outboundSMSTextMessage": {
                        "message": msg['content']
                    }
                } for msg in messages
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 201:
            # Utilisation de messages d'erreur plus spécifiques
            error_message = response.json().get('error_description', response.text)
            raise UserError(f"Erreur lors de l'envoi des SMS : {error_message}")
        
        sms_id = response.json().get('id')
        return sms_id
    
    def check_sms_balance(self):
        """
        Méthode pour vérifier le solde de SMS disponible via l'API Orange.
        """
        try:
            self._logger.info("Début de la vérification du solde SMS.")
            
            access_token = self.get_access_token()
            

            url = "https://api.orange.com/sms/admin/v1/contracts"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
            self._logger.info(f"Requête envoyée à l'URL : {url} avec les headers : {headers}")
            response = requests.get(url, headers=headers)
            self._logger.info(f"Réponse API : {response.status_code} - {response.text}")


            if response.status_code == 200:
                balance_data = response.json()
                self._logger.info(f"Données du solde reçues : {balance_data}")
                return balance_data
            else:
                error_message = response.json().get('error_description', response.text)
                self._logger.error(f"Erreur lors de la vérification du solde SMS : {error_message}")
                raise UserError(f"Erreur lors de la vérification du solde SMS : {response.text}")
            
        except Exception as e:
            self._logger.error(f"Exception lors de la vérification du solde SMS : {str(e)}")
            raise UserError(f"Erreur lors de la vérification du solde SMS : {str(e)}")
        
    def _get_sms_api_error_messages(self):
        """Messages d'erreurs personnalisés pour l'API Orange"""
        return {
            'insufficient_credit': _("Vous n'avez pas assez de crédits pour envoyer des SMS."),
            'wrong_number_format': _("Le format du numéro de téléphone est incorrect."),
            'expired_contract': _("Votre contrat est expiré, veuillez acheter un nouveau forfait."),
        }
