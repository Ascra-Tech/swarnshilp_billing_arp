# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InvoiceTDS(Document):
	pass


@frappe.whitelist()
def get_data_from_invoice(invoice_number):
    # Fetch the Sales Invoice document
    invoice = frappe.get_doc('Sales Invoice', invoice_number)
    customer_doc = frappe.get_doc('Customer', invoice.customer)
    # Example of data to be copied
    data = {
        'customer_name': invoice.customer,
        'total_amount': invoice.grand_total,
        'invoice_date': invoice.posting_date,
        'pan_no' : '',
        'account_code' : customer_doc.account_code,
        'net_amount' : invoice.base_total
    }
    
    return data

@frappe.whitelist()
def update_data_lock_unlock(invoice_number,status):
    invoice = frappe.get_doc('Sales Invoice', invoice_number)
    
    if invoice.docstatus == 1:
        # Update status
        invoice.custom_lock_unlock = status
        invoice.save()
        frappe.db.commit()

    return {
        'status': invoice.status
    }


