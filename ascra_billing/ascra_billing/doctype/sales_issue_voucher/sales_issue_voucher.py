# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import frappe.utils


class SalesIssueVoucher(Document):
	def before_save(self):
		# Fetch Customer
		self.customer = frappe.db.get_value("Customer", {"custom_account_code": self.account_code})
		
		if self.total_amt:
			total_amt = float(self.total_amt)
		else:
			total_amt = 0
		if self.tds_amount:
			tds_amount = float(self.tds_amount)
		else:
			tds_amount = 0
		self.net_bill_amt = total_amt + tds_amount
		# Add Total Column.
		total_net_wt = 0
		total_pcs = 0
		total_fine = 0
		if self.item_details:

			total_row = self.item_details[-1]
			if total_row.get("category") == "Total":
				self.item_details.pop()

			for item in self.item_details:
				total_net_wt += float(item.net_wt)
				total_pcs += float(item.pieces)
				total_fine += float(item.fine)

				
			self.append("item_details", {
				"category": "Total",
				"net_wt": total_net_wt,
				"pieces": float(total_pcs),
				"melting": '',
				"wastage": '',
				"fine": total_fine,
				"other_charges": ''
			})

		# Set Billing Account Fields
		
		total_fine_amount = float(self.gold_rate_billing or 0) * float(total_fine)
		self.total_fine_amount = total_fine_amount

		amount_tcs_tds = (
			total_fine_amount + 
			float(self.hallmark_amount or 0) + 
			float(self.logistic_amount or 0) + 
			float(self.total_other_charge or 0)
		)
		self.amount_tcs_tds = amount_tcs_tds
		amount_without_gst =(amount_tcs_tds/103)*100
		self.amount_without_gst = amount_without_gst
		self.billing_gold_rate = (
			amount_without_gst / total_net_wt
		)

		
	def on_submit(self):
		self.billing_status = 'approve'



# ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_address_by_account_code
@frappe.whitelist()
def get_address_by_account_code():
	acc_code = frappe.form_dict.account_code
	if not frappe.form_dict.account_code:
		frappe.response['message'] = []
		
	cust = frappe.db.get_value("Customer", {"custom_account_code": acc_code})

	if not cust:
		frappe.response['message'] = []
	else:
		add_filter = [["Dynamic Link","link_name","=",cust]]
		address = [i.get("name") for i in frappe.get_all("Address", add_filter, ['name'])]
		frappe.response['message'] = address



@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc

	def post_process(source, target):
		target.posting_date = frappe.utils.now_datetime()

		source.item_details.pop() # Remove the last Total Element
		total_net_wt = 0
		total_pcs = 0
		total_fine = 0

		if source.generate_bill_type == 'items':
			for item in source.item_details:
				target.append("items", {
					"custom_department": item.get("department_name"),
					"rate": source.billing_gold_rate, # Replace this by Perfectly Calculated Gold Rate
					"qty": item.net_wt,
					"custom_pieces": item.pieces
				})
		else:
			department = source.item_details[0].get("department_name")
			for item in source.item_details:
				total_net_wt += float(item.net_wt)
				total_pcs += float(item.pieces)

			target.append("items", {
					"custom_department": department,
					"qty": total_net_wt,
					"custom_pieces" : total_pcs,
					"rate": source.billing_gold_rate
				})

	doclist = get_mapped_doc(
		"Sales Issue Voucher",
		source_name,
		{
			"Sales Issue Voucher": {"doctype": "Sales Invoice",
						   "field_map": {
					"billing_gold_rate": "custom_gold_rate",
				}},
		},
		target_doc,
		post_process,
	)

	return doclist


# @frappe.whitelist()
# def make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
# 	def postprocess(source, target):
# 		set_missing_values(source, target)
# 		# Get the advance paid Journal Entries in Sales Invoice Advance
# 		if target.get("allocate_advances_automatically"):
# 			target.set_advances()

# 	def set_missing_values(source, target):
# 		target.flags.ignore_permissions = True
# 		target.run_method("set_missing_values")
# 		target.run_method("set_po_nos")
# 		target.run_method("calculate_taxes_and_totals")
# 		target.run_method("set_use_serial_batch_fields")

# 		if source.company_address:
# 			target.update({"company_address": source.company_address})
# 		else:
# 			# set company address
# 			target.update(get_company_address(target.company))

# 		if target.company_address:
# 			target.update(get_fetch_values("Sales Invoice", "company_address", target.company_address))

# 		# set the redeem loyalty points if provided via shopping cart
# 		if source.loyalty_points and source.order_type == "Shopping Cart":
# 			target.redeem_loyalty_points = 1

# 		target.debit_to = get_party_account("Customer", source.customer, source.company)

# 	def update_item(source, target, source_parent):
# 		target.amount = flt(source.amount) - flt(source.billed_amt)
# 		target.base_amount = target.amount * flt(source_parent.conversion_rate)
# 		target.qty = (
# 			target.amount / flt(source.rate)
# 			if (source.rate and source.billed_amt)
# 			else source.qty - source.returned_qty
# 		)

# 		if source_parent.project:
# 			target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center")
# 		if target.item_code:
# 			item = get_item_defaults(target.item_code, source_parent.company)
# 			item_group = get_item_group_defaults(target.item_code, source_parent.company)
# 			cost_center = item.get("selling_cost_center") or item_group.get("selling_cost_center")

# 			if cost_center:
# 				target.cost_center = cost_center

# 	doclist = get_mapped_doc(
# 		"Sales Order",
# 		source_name,
# 		{
# 			"Sales Order": {
# 				"doctype": "Sales Invoice",
# 				"field_map": {
# 					"party_account_currency": "party_account_currency",
# 					"payment_terms_template": "payment_terms_template",
# 				},
# 				"field_no_map": ["payment_terms_template"],
# 				"validation": {"docstatus": ["=", 1]},
# 			},
# 			"Sales Order Item": {
# 				"doctype": "Sales Invoice Item",
# 				"field_map": {
# 					"name": "so_detail",
# 					"parent": "sales_order",
# 				},
# 				"postprocess": update_item,
# 				"condition": lambda doc: doc.qty
# 				and (doc.base_amount == 0 or abs(doc.billed_amt) < abs(doc.amount)),
# 			},
# 			"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
# 			"Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
# 		},
# 		target_doc,
# 		postprocess,
# 		ignore_permissions=ignore_permissions,
# 	)

# 	automatically_fetch_payment_terms = cint(
# 		frappe.db.get_single_value("Accounts Settings", "automatically_fetch_payment_terms")
# 	)
# 	if automatically_fetch_payment_terms:
# 		doclist.set_payment_schedule()

# 	return doclist

@frappe.whitelist()
def get_item_details():
	company = frappe.form_dict.company
	item_code = frappe.form_dict.item_code
	item_details = frappe.get_value("Item", item_code, "*", as_dict=True)
	company = frappe.get_value("Company", company, "*", as_dict=True)
	frappe.response['message'] = {
		"stock_uom": item_details.get("stock_uom"),
		"item_name": item_details.get("item_name"),
		"income_account": company.get("default_income_account"),
		"cost_center": company.get("cost_center")
	}
