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
		billing_gold_rate = (
			amount_without_gst / total_net_wt
		)
		self.billing_gold_rate = billing_gold_rate
		gst_amount = (3 / 100) * billing_gold_rate
		self.gold_rate_with_gst = billing_gold_rate + gst_amount


		
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
					"gold_rate_with_gst": "custom_gold_rate__with_gst",
					"sub_account":"customer_address",
					"shipping_to_address": "shipping_address_name"
				}},
		},
		target_doc,
		post_process,
	)

	return doclist


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
