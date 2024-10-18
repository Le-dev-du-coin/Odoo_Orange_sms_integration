from odoo import http
import json
import logging

_logger = logging.getLogger(__name__)  
class OrangeSMSController(http.Controller):  

   @http.route('/orange/smsdr', type='json', auth='public', methods=['POST'], csrf=False)
   def sms_delivery_receipt(self, **kwargs):
    try:
        # Récupérer les données JSON de la requête
        data = http.request.jsonrequest
        _logger.info(f"Accusé de réception reçu : {json.dumps(data)}")

        # Extraire les informations importantes
        delivery_info = data.get('deliveryInfoNotification', {}).get('deliveryInfo', {})
        phone_number = delivery_info.get('address', '')
        delivery_status = delivery_info.get('deliveryStatus', '')
        message_id = data.get('resourceURL', '').split('/')[-1]  # ID du message depuis l'URL

        if phone_number and delivery_status:
            # Créer un enregistrement dans le modèle 'sms.delivery.receipt'
            request.env['sms.delivery.receipt'].sudo().create({
                'phone_number': phone_number,
                'delivery_status': delivery_status,
                'message_id': message_id
            })
            _logger.info(f"Accusé de réception enregistré pour {phone_number} avec le statut {delivery_status}.")
            return {'status': 'success', 'message': 'Accusé de réception enregistré.'}
        else:
            _logger.error("Les informations de livraison sont manquantes ou invalides.")
            return {'status': 'error', 'message': 'Données invalides.'}
    
    except Exception as e:
        _logger.error(f"Erreur lors de la réception de l'accusé de réception : {str(e)}")
        return {'status': 'error', 'message': str(e)}

