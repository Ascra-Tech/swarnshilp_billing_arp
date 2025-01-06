import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


def before_save(self, method):
	pass

# ascra_billing.ascra_billing.doc_events.sales_invoice.make_delivery_note

@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		# target.posting_date = frappe.utils.now_datetime()
		frappe.logger("utils").exception(check_labor_bill(source))
		frappe.logger("utils").exception(source.custom_sales_issue_voucher)
		if not check_labor_bill(source): return
		if not source.custom_sales_issue_voucher: return

		# target_doc.items = []
		sales_issue_voucher_doc = frappe.get_doc("Sales Issue Voucher", source.custom_sales_issue_voucher)
		sales_issue_voucher_doc.item_details.pop() # Remove the last Total Element
		total_net_wt = 0
		total_pcs = 0
		total_fine = 0

		if sales_issue_voucher_doc.generate_bill_type == 'items':
			for item in sales_issue_voucher_doc.item_details:
				target.append("items", {
					"custom_department": item.get("department_name"),
					"rate": sales_issue_voucher_doc.billing_gold_rate,
					"qty": item.net_wt,
					"custom_pieces": item.pieces
				})
		else:
			department = sales_issue_voucher_doc.item_details[0].get("department_name")
			for item in sales_issue_voucher_doc.item_details:
				total_net_wt += float(item.net_wt)
				total_pcs += float(item.pieces)

			target.append("items", {
					"custom_department": department,
					"qty": total_net_wt,
					"custom_pieces" : total_pcs,
					"rate": sales_issue_voucher_doc.billing_gold_rate
				})

		if sales_issue_voucher_doc.display_making_charges:
			item_details = get_item_details(
				company=get_default_company(),
				item_code="MakingCharges"
			).get("message")
			target.append("items", {
					"qty": 1,
					"custom_pieces" : total_pcs,
					"rate": sales_issue_voucher_doc.making_charges,
					"custom_item":"MakingCharges",
					"uom" : item_details.get("stock_uom"),
					"income_account" : item_details.get("income_account"),
					"item_name" : item_details.get("item_name"),
					"cost_center" : item_details.get("cost_center"),
					"gst_hsn_code": "12345678"
				})
			

	def update_item(source_doc, target_doc, source_parent):		
		target_doc.qty = flt(source_doc.qty) - flt(source_doc.delivered_qty)
		target_doc.stock_qty = target_doc.qty * flt(source_doc.conversion_factor)

		target_doc.base_amount = target_doc.qty * flt(source_doc.base_rate)
		target_doc.amount = target_doc.qty * flt(source_doc.rate)
	
		
	si_doc = frappe.get_doc("Sales Invoice", source_name)
	if not check_labor_bill(si_doc):
		doclist = get_mapped_doc(
			"Sales Invoice",
			source_name,
			{
				"Sales Invoice": {"doctype": "Delivery Note", "validation": {"docstatus": ["=", 1]}},
				"Sales Invoice Item": {
					"doctype": "Delivery Note Item",
					# "field_map": {},
					"postprocess": update_item,
					"condition": lambda doc: doc.delivered_by_supplier != 1,
				},
				"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
				"Sales Team": {
					"doctype": "Sales Team",
					"field_map": {"incentives": "incentives"},
					"add_if_empty": True,
				},
			},
			target_doc,
			set_missing_values,
		)
	else:
		doclist = get_mapped_doc(
			"Sales Invoice",
			source_name,
			{
				"Sales Invoice": {"doctype": "Delivery Note", "validation": {"docstatus": ["=", 1]}},
				"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
				"Sales Team": {
					"doctype": "Sales Team",
					"field_map": {"incentives": "incentives"},
					"add_if_empty": True,
				},
			},
			target_doc,
			set_missing_values,
		)
	

	return doclist


def check_labor_bill(source):
	sales_issue_voucher = source.custom_sales_issue_voucher
	if sales_issue_voucher:
		bill_type = (
					frappe.db.get_value("Sales Issue Voucher", sales_issue_voucher, "gst_name")
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
    customer = doc.customer
    
    if customer:
        customer_doc = frappe.get_doc("Customer", customer)
        if customer_doc.custom_block_account :
            frappe.throw(f"Cannot save Sales Invoice. Customer '{customer}' is blocked ('{customer_doc.custom_reason}')")

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def filter_items_by_department(doctype, txt, searchfield, start, page_len, filters):
    department = filters.get("department")
    if not department:
        return []

    print("dddddddeeeeeeeeeee",department)
    # Query to check if the department exists in the Table MultiSelect field
    return frappe.db.sql("""
        SELECT name
        FROM `tabItem`
        WHERE EXISTS (
            SELECT 1 FROM `tabItem Other Department` 
            WHERE `tabItem Other Department`.parent = `tabItem`.name
            AND `tabItem Other Department`.other_department = %s
        )
        AND name LIKE %s
        LIMIT %s, %s
    """, (department, f"%{txt}%", start, page_len))
