# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import frappe.utils
import requests
import json

class SalesIssueVoucher(Document):
	def before_insert(self):
		perform_calculations(self)
	# def before_submit(self):
	# 	frappe.throw("Submit Not Allowed Directly, Please Approve the Document to submit")
	def on_update(self):
		if self.workflow_state == "Approved":
			send_status(self, "Approved")
		elif self.workflow_state == "Rejected":
			send_status(self, "Rejected")

		


	def before_save(self):
		perform_calculations(self)

	def on_submit(self):
		perform_calculations(self)
		self.billing_status = 'approve'

def perform_calculations(self):
	# Fetch Customer
	self.customer = frappe.db.get_value("Customer", {"custom_account_code": self.account_code})
	# frappe.logger("utils").exception(self.voucher_billing_dept_cat_type.lower())
	if self.total_amt:
		total_amt = float(self.total_amt)
	else:
		total_amt = 0
	if self.tds_amount:
		tds_amount = float(self.tds_amount)
	else:
		tds_amount = 0

	if self.tcs_amount:
		tcs_amount = float(self.tcs_amount)
	else:
		tcs_amount = 0

	self.net_bill_amt = total_amt + tds_amount
	# Add Total Column.
	total_net_wt = 0
	total_pcs = 0
	total_fine = 0
	item_index = 0
	making_purity = 0
	voucher_billing_dept_cat_type = ""
	if self.item_details:

		total_row = self.item_details[-1]
		if total_row.get("category") == "Total":
			self.item_details.pop()

		for item in self.item_details:
			if item_index == 0:
				making_purity = item.melting
			total_net_wt += float(item.net_wt)
			total_pcs += float(item.pieces)
			total_fine += float(item.fine)
			item_index += int(item_index)

			
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
	if (self.voucher_billing_dept_cat_type).lower() == "labour bill":
		total_fine_amount = float(self.gold_rate_billing or 0) * float(self.gold_weight or 0)
	else :
		total_fine_amount = float(self.gold_rate_billing or 0) * float(total_fine)

	self.total_fine_amount = round(total_fine_amount)

	amount_tcs_tds = (
		total_fine_amount + 
		float(self.total_hallmark_amount or 0) + 
		float(self.total_logistic_amount or 0) + 
		float(self.total_other_charge or 0) +
		float(self.discount_amount or 0)
	)
	self.amount_tcs_tds = round(amount_tcs_tds)
	if (self.voucher_billing_dept_cat_type).lower() == "labour bill":
		amount_without_gst =(amount_tcs_tds/105)*100
	else:
		amount_without_gst =(amount_tcs_tds/103)*100

	self.amount_without_gst = amount_without_gst
	
	if (self.voucher_billing_dept_cat_type).lower() == "labour bill":
		billing_gold_rate = (
			amount_without_gst / total_net_wt
		)	
	else:
		billing_gold_rate = (
			amount_without_gst / total_net_wt
		)

	
	self.billing_gold_rate = billing_gold_rate
	
	if (self.voucher_billing_dept_cat_type).lower() == "labour bill":
		gst_amount = (5 / 100) * billing_gold_rate
	else:
		gst_amount = (3 / 100) * billing_gold_rate

	
	self.gold_rate_with_gst = billing_gold_rate + gst_amount

	# Making charge #
	rate_per_gram = float(amount_without_gst) / float(total_net_wt)

	rate_per_cut = 0
	rate_cut = 0
	making_charges = 0
	making_rate_per_gram = 0
	backup_making_rate_per_gram = 0
	backup_making_charges = 0

	if self.display_making_charges == 1:
		rate_per_cut = total_net_wt * (making_purity/100)
		rate_cut = total_fine - rate_per_cut
		gold_rate = self.gold_rate
		if float(self.gold_rate_purity or 0) == 99.500:
			gold_rate = (gold_rate/99.5)*100

		making_charges = rate_cut * gold_rate

		other_charges = (
			float(self.total_hallmark_amount or 0) + 
			float(self.total_logistic_amount or 0) + 
			float(self.total_other_charge or 0) +
			float(self.discount_amount or 0)
		)
		making_charges = float(making_charges) + float(other_charges)

		making_rate_per_gram = making_charges / total_net_wt

		billing_gold_rate = float(billing_gold_rate) - float(making_rate_per_gram)
		self.billing_gold_rate = billing_gold_rate
	
		rate_per_gram = rate_per_gram - making_rate_per_gram
		backup_making_rate_per_gram = making_rate_per_gram
		backup_making_charges = making_charges
	else:
		rate_per_cut = float(total_net_wt) * (float(making_purity)/100)
		rate_cut = float(total_fine) - rate_per_cut
		gold_rate = self.gold_rate
		if self.gold_rate_purity == 99.500:
			gold_rate = (gold_rate/99.5)*100

		making_charges = float(rate_cut) * float(gold_rate)
		other_charges = (float(self.total_hallmark_amount or 0) + float(self.total_logistic_amount or 0) + float(self.total_other_charge or 0) + float(self.discount_amount or 0))
		making_charges = (making_charges + other_charges)
		making_rate_per_gram = float(making_charges) / float(total_net_wt)
		backup_making_rate_per_gram = making_rate_per_gram
		backup_making_charges = float(total_net_wt) * making_rate_per_gram;

	self.making_charges = making_charges
	self.making_rate_per_gram = making_rate_per_gram
	self.backup_making_rate_per_gram = backup_making_rate_per_gram
	self.backup_making_charges = backup_making_charges

	# End of Making charge #

@frappe.whitelist()
def submit_doc(doc):
	doc = json.loads(doc)
	doc.submit()

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

	def set_missing_values(source, target):
		# Example condition: Set customer field based on a field value
		if source.sub_account:
			target.customer = source.sub_account
		elif source.account_code:
			cust = frappe.db.get_value("Customer", {"custom_account_code": source.account_code})
			if cust:
				target.customer = cust

		if source.sub_account:
			add_filter = [["Dynamic Link", "link_name", "=", source.sub_account]]
			address = [i.get("name") for i in frappe.get_all("Address", add_filter, ['name'])]
			if address:
				target.customer_address = address[0]
		elif source.account_code:
			cust = frappe.db.get_value("Customer", {"custom_account_code": source.account_code,"custom_account_sub_code": None})
			if cust:
				add_filter = [["Dynamic Link", "link_name", "=", cust]]
				address = [i.get("name") for i in frappe.get_all("Address", add_filter, ['name'])]
				if address:
					target.customer_address = address[0]
		target.custom_other_department = source.item_details[0].get("department_name")
		target.custom_sales_type = source.voucher_billing_dept_cat_type

	def post_process(source, target):
		set_missing_values(source,target)
		print("----------1--------post process")
		target.posting_date = frappe.utils.now_datetime()

		source.item_details.pop() # Remove the last Total Element
		total_net_wt = 0
		total_pcs = 0
		total_fine = 0
		# for item in source.item_details:
		# 	target.custom_other_department = item.get('department_name')
		# 	break
		if source.generate_bill_type == 'items':
			for item in source.item_details:
				target.append("items", {
					"custom_department": item.get("department_name"),
					"rate": source.billing_gold_rate,
					"qty": item.net_wt,
					"custom_pieces": item.pieces
				})
				print("----------1--------item addditiin")

		else:
			department = source.item_details[0].get("department_name")
			target.custom_other_department = source.item_details[0].get("department_name")
			for item in source.item_details:
				total_net_wt += float(item.net_wt)
				total_pcs += float(item.pieces)

			target.append("items", {
					"custom_department": department,
					"qty": total_net_wt,
					"custom_pieces" : total_pcs,
					"rate": source.billing_gold_rate
				})
			print("--------2----------item addditiin")
		if source.display_making_charges:
			item_details = get_item_details(
				company=get_default_company(),
				item_code="MakingCharges"
			).get("message")
			target.append("items", {
					"qty": 1,
					"custom_pieces" : total_pcs,
					"rate": source.making_charges,
					"custom_item":"MakingCharges",
					"uom" : item_details.get("stock_uom"),
                    "income_account" : item_details.get("income_account"),
                    "item_name" : item_details.get("item_name"),
                    "cost_center" : item_details.get("cost_center"),
					"gst_hsn_code": "12345678"
				})

	doclist = get_mapped_doc(
		"Sales Issue Voucher",
		source_name,
		{
			"Sales Issue Voucher": {"doctype": "Sales Invoice",
			"field_map": {
					"billing_gold_rate": "custom_gold_rate",
					"gold_rate_with_gst": "custom_gold_rate__with_gst",
					"shipping_to_address": "shipping_address_name",
					"name": "custom_sales_issue_voucher"
				}},
		},
		target_doc,
		post_process
	)

	return doclist

def get_default_company():
    user = frappe.session.user
    default_company = frappe.defaults.get_user_default("Company", user)
    return default_company

@frappe.whitelist()
def get_item_details(company=None, item_code = None, sales_issue_voucher=None):
	company = frappe.form_dict.company or company
	item_code = frappe.form_dict.item_code or item_code
	item_details = frappe.get_value("Item", item_code, "*", as_dict=True)
	frappe.logger("utils").exception(item_details)
	company = frappe.get_value("Company", company, "*", as_dict=True)
	rate = frappe.get_value("Sales Issue Voucher", sales_issue_voucher, 'billing_gold_rate')
	item_details_dict = {
		"stock_uom": item_details.get("stock_uom"),
		"item_name": item_details.get("item_name"),
		"income_account": company.get("default_income_account"),
		"cost_center": company.get("cost_center"),
		"rate": rate
	}
	frappe.response['message'] = item_details_dict

	return {
		"message": item_details_dict
	}


def send_status(self, status):
	try:
		settings_doc = frappe.get_single("Ascra Billing Settings")
		url = settings_doc.api_url
		if not url:
			frappe.logger("workflow_status_log").exception(f"Api URL Not Configured")
			return
		billing_status = 1 if status == "Approved" else 2
		frappe.logger("workflow_status_log").exception(billing_status)
		payload = {
			"id": self.name,
			"billing_notes": self.billing_notes,
			"billing_status": billing_status,
			"billing_status_reason_remark": "",
			"billing_status_feedback_remark": "", # TODO: Add Fields
			"billing_status_approved_reject_by": "", # TODO: Add Fields
			"voucher_billing_dept_cat_type": self.voucher_billing_dept_cat_type,
			"generate_bill_type": self.generate_bill_type,
			"sub_account_name": self.sub_account,
			"sub_account_id": 0, # TODO: Fetch this Field Via UI
			"display_making_charges": self.display_making_charges,
			"godown_bill": self.godown_bill
		}
		files=[

		]
		headers = {}

		response = requests.request("POST", url, headers=headers, data=payload, files=files)

		frappe.logger("workflow_status_log").exception(f"Id : {self.id}, {response.json()}")
	except Exception as e:
		frappe.logger("workflow_status_log").exception(f"Id : {self.id}, {e}")

@frappe.whitelist()
def set_status(docname, status):
	frappe.db.set_value("Sales Issue Voucher", docname, "billing_status", status)
	frappe.db.commit()

# ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_address_by_account_code
@frappe.whitelist()
def get_docket_file_path():
	voucher_id = frappe.form_dict.id
	if not frappe.form_dict.id:
		frappe.response['message'] = []
		
	get_delivery_note_data = frappe.db.get_value("Delivery Note", {"custom_sales_issue_voucher": voucher_id})
	
	get_file_url = frappe.db.get_value("File",{"attached_to_name":get_delivery_note_data},'file_url')

	if not get_file_url:
		frappe.response['message'] = []
	else:
		frappe.response['message'] = get_file_url