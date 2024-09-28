from odoo import models, fields
from odoo.exceptions import UserError

class SMSTest(models.Model):
    _name = 'sms.test'
    _description = 'Test de message SMS'

    phone_number = fields.Char(string="Numéro de téléphone", required=True)
    message = fields.Text(string="Message", required=True)

    def send_test_sms(self):
        """Méthode pour envoyer un SMS de test"""
        if not self.phone_number or not self.message:
            raise UserError("Le numéro de téléphone et le message sont obligatoires.")
        
        # Récupérer une configuration API pour l'envoi du SMS
        api_config = self.env['sms.orange'].search([], limit=1)
        if not api_config:
            raise UserError("Aucune configuration SMS Orange trouvée.")
        
        # Envoyer le SMS en utilisant la configuration
        try:
            api_config.send_sms(int(self.phone_number), self.message)
        except Exception as e:
            raise UserError(f"Erreur lors de l'envoi du SMS : {str(e)}")
