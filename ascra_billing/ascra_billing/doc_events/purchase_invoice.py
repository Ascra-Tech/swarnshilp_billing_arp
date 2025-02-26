import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt
import requests


# def before_save(self, method):
# 	pass
def before_save(self, method):
	if self.custom_roundup_total == 1 :
		self.rounded_total = round(self.rounded_total)
	if self.custom_roundup_total == 1 :
		self.grand_total = round(self.grand_total)

# ascra_billing.ascra_billing.doc_events.sales_invoice.make_delivery_note

# @frappe.whitelist()
# def make_delivery_note(source_name, target_doc=None):
# 	def set_missing_values(source, target):
# 		target.run_method("set_missing_values")
# 		target.run_method("set_po_nos")
# 		target.run_method("calculate_taxes_and_totals")

# 		# target.posting_date = frappe.utils.now_datetime()
# 		frappe.logger("utils").exception(check_labor_bill(source))
# 		frappe.logger("utils").exception(source.custom_sales_issue_voucher)
# 		if not check_labor_bill(source): return
# 		if not source.custom_sales_issue_voucher: return

# 		# target_doc.items = []
# 		sales_issue_voucher_doc = frappe.get_doc("Sales Issue Voucher", source.custom_sales_issue_voucher)
# 		sales_issue_voucher_doc.item_details.pop() # Remove the last Total Element
# 		total_net_wt = 0
# 		total_pcs = 0
# 		total_fine = 0

# 		if sales_issue_voucher_doc.generate_bill_type == 'items':
# 			for item in sales_issue_voucher_doc.item_details:
# 				target.append("items", {
# 					"custom_department": item.get("department_name"),
# 					"rate": sales_issue_voucher_doc.billing_gold_rate,
# 					"qty": item.net_wt,
# 					"custom_pieces": item.pieces
# 				})
# 		else:
# 			department = sales_issue_voucher_doc.item_details[0].get("department_name")
# 			for item in sales_issue_voucher_doc.item_details:
# 				total_net_wt += float(item.net_wt)
# 				total_pcs += float(item.pieces)

# 			target.append("items", {
# 					"custom_department": department,
# 					"qty": total_net_wt,
# 					"custom_pieces" : total_pcs,
# 					"rate": sales_issue_voucher_doc.billing_gold_rate
# 				})

# 		if sales_issue_voucher_doc.display_making_charges:
# 			item_details = get_item_details(
# 				company=get_default_company(),
# 				item_code="MakingCharges"
# 			).get("message")
# 			target.append("items", {
# 					"qty": 1,
# 					"custom_pieces" : total_pcs,
# 					"rate": sales_issue_voucher_doc.making_charges,
# 					"custom_item":"MakingCharges",
# 					"uom" : item_details.get("stock_uom"),
# 					"income_account" : item_details.get("income_account"),
# 					"item_name" : item_details.get("item_name"),
# 					"cost_center" : item_details.get("cost_center"),
# 					"gst_hsn_code": "12345678"
# 				})
			

# 	def update_item(source_doc, target_doc, source_parent):		
# 		target_doc.qty = flt(source_doc.qty) - flt(source_doc.delivered_qty)
# 		target_doc.stock_qty = target_doc.qty * flt(source_doc.conversion_factor)

# 		target_doc.base_amount = target_doc.qty * flt(source_doc.base_rate)
# 		target_doc.amount = target_doc.qty * flt(source_doc.rate)
	
		
# 	si_doc = frappe.get_doc("Sales Invoice", source_name)
# 	if not check_labor_bill(si_doc):
# 		doclist = get_mapped_doc(
# 			"Sales Invoice",
# 			source_name,
# 			{
# 				"Sales Invoice": {"doctype": "Delivery Note", "validation": {"docstatus": ["=", 1]}},
# 				"Sales Invoice Item": {
# 					"doctype": "Delivery Note Item",
# 					# "field_map": {},
# 					"postprocess": update_item,
# 					"condition": lambda doc: doc.delivered_by_supplier != 1,
# 				},
# 				"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
# 				"Sales Team": {
# 					"doctype": "Sales Team",
# 					"field_map": {"incentives": "incentives"},
# 					"add_if_empty": True,
# 				},
# 			},
# 			target_doc,
# 			set_missing_values,
# 		)
# 	else:
# 		doclist = get_mapped_doc(
# 			"Sales Invoice",
# 			source_name,
# 			{
# 				"Sales Invoice": {"doctype": "Delivery Note", "validation": {"docstatus": ["=", 1]}},
# 				"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
# 				"Sales Team": {
# 					"doctype": "Sales Team",
# 					"field_map": {"incentives": "incentives"},
# 					"add_if_empty": True,
# 				},
# 			},
# 			target_doc,
# 			set_missing_values,
# 		)
	

# 	return doclist


def check_labor_bill(source):
	sales_issue_voucher = source.custom_sales_issue_voucher
	if sales_issue_voucher:
		bill_type = (
					frappe.db.get_value("Sales Receipt Voucher", sales_issue_voucher, "gst_name")
				)
		labor_bill = "labour" in bill_type.lower()
		return labor_bill
	return False



def get_default_company():
    user = frappe.session.user
    default_company = frappe.defaults.get_user_default("Company", user)
    return default_company

@frappe.whitelist()
def get_item_details(company=None, item_code = None):
	company = frappe.form_dict.company or company
	item_code = frappe.form_dict.item_code or item_code
	item_details = frappe.get_value("Item", item_code, "*", as_dict=True)
	frappe.logger("utils").exception(item_details)
	company = frappe.get_value("Company", company, "*", as_dict=True)
	item_details_dict = {
		"stock_uom": item_details.get("stock_uom"),
		"item_name": item_details.get("item_name"),
		"income_account": company.get("default_income_account"),
		"cost_center": company.get("cost_center")
	}
	frappe.response['message'] = item_details_dict

	return {
		"message": item_details_dict
	}

@frappe.whitelist()
def validate_account_block_status(doc, method):
    supplier = doc.supplier
    
    if supplier:
        supplier_doc = frappe.get_doc("Supplier", supplier)
        if supplier_doc.custom_block_account :
            frappe.throw(f"Cannot save Purchase Invoice. Customer '{supplier}' is blocked ('{supplier_doc.custom_reason}')")

@frappe.whitelist()
def fetch_bill_types():
	url = "https://staging-swarnshilp-accounting.ascratech.com/GST_api"  # Replace with your URL
	headers = {"Content-Type": "application/json"}

	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		data = response.json()

		if "bill_type" in data:
			bill_types = data["bill_type"]

			# Create or update Bill Type records
			for bill in bill_types:
				bill_name = bill.get("name")

				if bill_name:
					# Update the User doctype to add these Bill Types as options
					# In a real scenario, you can either create a new Bill Type Doctype or use an existing one
					bill_type_doc = frappe.get_doc({
						"doctype": "Bill Type",  # Assuming 'Bill Type' is a Doctype
						"bill_type": bill_name
					})
					bill_type_doc.insert()

			frappe.db.commit()
		else:
			frappe.throw("Bill types not found in the response.")
	else:
		frappe.throw(f"Failed to fetch data from the URL. Status Code: {response.status_code}")




@frappe.whitelist()
def get_tax_details(tax_category):
    return frappe.db.sql('''
        SELECT tax_withholding_rate 
        FROM `tabTax Withholding Rate` 
        WHERE parent = %s
    ''', (tax_category,), as_dict=True)
