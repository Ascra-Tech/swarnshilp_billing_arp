# Copyright (c) 2025, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import requests

class SendSMS(Document):
	pass


@frappe.whitelist()
def get_inactive_customers(inactive_days, exclude_cashhead=0):
	if not inactive_days:
		return []

	# Get customers who have at least one payment entry
	customers_with_payments = frappe.db.sql("""
        SELECT DISTINCT party
        FROM `tabPayment Entry`
        WHERE docstatus = 1 AND party_type = 'Customer'
    """, as_dict=True)

	if not customers_with_payments:
		return []

	customer_list = [customer["party"] for customer in customers_with_payments]

	# Get customers who have NOT had any payment in the last N days
	thirty_days_ago = datetime.today() - timedelta(days=int(inactive_days))

	inactive_customers = frappe.db.sql("""
        SELECT DISTINCT party
        FROM `tabPayment Entry`
        WHERE docstatus = 1 AND party_type = 'Customer' 
        AND posting_date >= %s
    """, (thirty_days_ago,), as_dict=True)

	recent_customers = {customer["party"] for customer in inactive_customers}
	customers_no_recent_payment = [cust for cust in customer_list if cust not in recent_customers]

	# Exclude customers where cashhead is checked if exclude_cashhead is true
	if int(exclude_cashhead) == 1:
		customers_no_recent_payment = frappe.db.sql("""
            SELECT name
            FROM `tabCustomer`
            WHERE name IN %s AND IFNULL(cashhead, 0) = 0
        """, (tuple(customers_no_recent_payment) or ('',),), as_list=True)

		customers_no_recent_payment = [cust[0] for cust in customers_no_recent_payment]

	# Fetch primary contact numbers for inactive customers
	customer_contact_map = {}

	for customer in customers_no_recent_payment:
		contact = frappe.db.sql("""
            SELECT phone, mobile_no
            FROM `tabContact`
            WHERE EXISTS (
                SELECT 1 FROM `tabDynamic Link`
                WHERE `tabDynamic Link`.parent = `tabContact`.name
                AND `tabDynamic Link`.link_doctype = 'Customer'
                AND `tabDynamic Link`.link_name = %s
            )
            ORDER BY is_primary_contact DESC, modified DESC
            LIMIT 1
        """, (customer,), as_dict=True)

		if contact:
			customer_contact_map[customer] = contact[0].get("mobile_no") or contact[0].get("phone")

	return customer_contact_map


@frappe.whitelist()
def send_sms(docname):
	doc = frappe.get_doc("Send SMS", docname)

	phone_numbers = []

	# If manual phone numbers are provided, use them
	if doc.mobile_number:
		phone_numbers = [num.strip() for num in doc.mobile_number.split(",")]

	# If no manual phone numbers, fetch from selected customers
	elif doc.account:
		customers = frappe.db.sql("""
		        SELECT customer FROM `tabSend SMS Child`
		        WHERE parent = %s
		    """, (doc.name,), as_dict=True)

		for customer_name in customers:
			contact = frappe.db.sql("""
	            SELECT phone, mobile_no FROM `tabContact`
	            WHERE EXISTS (
	                SELECT 1 FROM `tabDynamic Link`
	                WHERE `tabDynamic Link`.parent = `tabContact`.name
	                AND `tabDynamic Link`.link_doctype = 'Customer'
	                AND `tabDynamic Link`.link_name = %s
	            )
	            ORDER BY is_primary_contact DESC, modified DESC
	            LIMIT 1
	        """, (customer_name.customer,), as_dict=True)
			print("---------------------customer name",customer_name.customer)

			if contact:
				print("if conatct------------------",contact)
				phone_number = contact[0].get("mobile_no") or contact[0].get("phone")
				if phone_number:
					phone_numbers.append(phone_number)

	if not phone_numbers:
		frappe.throw("No phone numbers found to send SMS.")

	# Loop through phone numbers and send SMS
	for phone in phone_numbers:
		sender_name = frappe.get_value("SMS Template", doc.template, 'sender_name')

		sms_resp = send_api(phone,doc.message,sender_name)  # Call the API function
		slog = frappe.new_doc("SMS Logs")  # Create new Send SMS document
		slog.mobile_number = phone  # Set default values (empty)
		slog.sms_message = doc.message
		slog.sender_name = sender_name
		slog.response = sms_resp
		slog.insert(ignore_permissions=True)
		# frappe.msgprint(f"SMS sent to {phone}")
	return "success"

def send_api(phone_number, message, send):
	"""Send SMS to a given phone number with a custom message."""
	url = "https://prpsms.co.in/API/SendMsg.aspx"

	payload = {
		'uname': '20171960',
		'pass': 'nina1977',
		'msg': message,
		'dest': phone_number,
		'send': send,
		'priority': '1'
	}

	headers = {
		'Cookie': 'ASP.NET_SessionId=iuuu42fl4rt0efsturbb2wtk'
	}

	try:
		response = requests.post(url, data=payload, headers=headers)

		# Log response for debugging
		frappe.logger().info(f"SMS Response: {response.text}")

		return response.text  # Return API response
	except requests.RequestException as e:
		frappe.throw(f"Failed to send SMS: {str(e)}")

