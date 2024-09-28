from odoo import http
from odoo.http import request

class OrangeSMSController(http.Controller):

    @http.route('/orange/smsdr', type='json', auth='public', methods=['POST'], csrf=False)
    def sms_delivery_receipt(self, **kwargs):
        receipt_data = request.jsonrequest.get('deliveryInfoNotification', {})
        delivery_info = receipt_data.get('deliveryInfo', {})
        
        if delivery_info:
            request.env['sms.receipt'].sudo().create({
                'sms_id': receipt_data.get('callbackData'),
                'recipient_phone_number': delivery_info.get('address'),
                'delivery_status': delivery_info.get('deliveryStatus')
            })
        return "OK"
