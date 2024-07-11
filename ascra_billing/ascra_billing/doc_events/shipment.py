import frappe
import requests
from frappe.utils import get_url_to_form

def send_sms_after_submit(doc, method):
    try:
        # Ensure the SMS settings are loaded
        sms_settings = frappe.get_doc("SMS Settings")
        
        if not sms_settings:
            frappe.throw("Please configure SMS Settings first.")
        
        # Prepare the SMS details
        sms_gateway_url = sms_settings.sms_gateway_url
        message_parameter = sms_settings.message_parameter
        receiver_parameter = sms_settings.receiver_parameter
        
        parameters = {}
        for param in sms_settings.parameters:
            parameters[param.parameter] = param.value
        
        message = f"Hello from SwarnShilp Chains! Your ORDER has been dispatched. https://abc.com Please give us a minute and fill feedback- http://goo.gl/89hRFK."
        receiver = doc.delivery_contact.split('<br>')[-1]  # Assuming the mobile number is the last item in the delivery_contact field
        
        # Construct the payload with parameters
        payload = {receiver_parameter: receiver, message_parameter: message}
        for key, value in parameters.items():
            payload[key] = value
        
        # Log payload for debugging
        frappe.logger().info(f"SMS Payload: {payload}")
        
        # Send the SMS request
        response = requests.get(sms_gateway_url, params=payload)
        
        # Log response for debugging
        frappe.logger().info(f"SMS Response: {response.status_code} - {response.text}")
        
        if response.status_code != 200:
            frappe.throw(f"Failed to send SMS. Status Code: {response.status_code}")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "SMS Sending Error")
        frappe.throw(f"Failed to send SMS: {str(e)}")

