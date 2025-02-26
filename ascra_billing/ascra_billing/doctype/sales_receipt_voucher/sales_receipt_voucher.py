# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesReceiptVoucher(Document):
	def on_update(self):
		if self.workflow_state == "Approved":
			send_status(self, "Approved")
		elif self.workflow_state == "Rejected":
			send_status(self, "Rejected")

	def before_save(self):
		# Fetch Customer
		self.customer = frappe.db.get_value("Customer", {"custom_account_code": self.account_code})
		amount_tcs_tds = 0
		taxable_value = 0
		total_net_wt = 0
		total_pcs = 0
		total_fine = 0
		if self.total_amt:
			total_amt = float(self.total_amt)
		else:
			total_amt = 0
		if self.tds_amount:
			tds_amount = float(self.tds_amount)
		else:
			tds_amount = 0
		# self.net_bill_amt = total_amt + tds_amount

		if self.item_details:
			total_net_wt = 0
			for item in self.item_details:
				total_net_wt += float(item.net_wt)
				total_pcs += float(item.pieces)
				total_fine += float(item.fine)
				print(total_net_wt)

			total_row = self.item_details[-1]
			if total_row.get("category") == "Total":
				self.item_details.pop()
			

			self.append("item_details", {
				"category": "Total",
				"net_wt": total_net_wt,
				"pieces": float(total_pcs),
				"melting": '',
				"wastage": '',
				"fine": total_fine,
				"other_charges": ''
			})

		if self.tcs_amount !=0 and self.purc_sale_type == "":
			amount_tcs_tds = float(self.fine_amount or 0) + float(self.total_other_charge or 0) + float(self.gst_amount or 0) + float(self.discount_amount or 0) + float(self.total_logistic_amount or 0) + float(self.total_hallmark_amount or 0)
			print("amount_tcs_tds1")
			print(amount_tcs_tds)
		else :
			amount_tcs_tds = float(self.total_amt or 0)			

		# self.amount_tcs_tds = round(amount_tcs_tds)
		#amount_tcs_tds = self.total_amt

		if self.gst_name != "" and self.purc_sale_type == "":
			if (self.gst_name).lower() == 'sale bill':
				amount_tcs_tds = float(amount_tcs_tds)
				rate_per_gram = ((amount_tcs_tds/103)*100)/total_net_wt
			elif (self.gst_name).lower() == 'labour bill':
				amount_tcs_tds = float(amount_tcs_tds)
				rate_per_gram = ((amount_tcs_tds/105)*100)/total_net_wt
			else:
				rate_per_gram = float(amount_tcs_tds/total_net_wt or 0)
		else :
			rate_per_gram = float(amount_tcs_tds/total_net_wt)


		billing_gold_rate = 0
		self.billing_gold_rate = float(rate_per_gram or 0)
		taxable_value = float(total_net_wt) * float(rate_per_gram)
		self.total_fine_amount = round(taxable_value)

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
		
	cust = frappe.db.get_value("Supplier", {"custom_account_code": acc_code})

	if not cust:
		frappe.response['message'] = []
	else:
		add_filter = [["Dynamic Link","link_name","=",cust]]
		address = [i.get("name") for i in frappe.get_all("Address", add_filter, ['name'])]
		frappe.response['message'] = address


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc

	def set_missing_values(source, target):
		# Example condition: Set customer field based on a field value
		if source.sub_account:
			target.supplier = source.sub_account
		elif source.account_code:
			supp = frappe.db.get_value("Supplier", {"custom_account_code": source.account_code})
			if supp:
				target.supplier = supp

		if source.sub_account:
			add_filter = [["Dynamic Link", "link_name", "=", source.sub_account]]
			address = [i.get("name") for i in frappe.get_all("Address", add_filter, ['name'])]
			if address:
				target.customer_address = address[0]
		elif source.account_code:
			supp = frappe.db.get_value("Supplier", {"custom_account_code": source.account_code,"custom_account_sub_code": None})
			if supp:
				add_filter = [["Dynamic Link", "link_name", "=", supp]]
				address = [i.get("name") for i in frappe.get_all("Address", add_filter, ['name'])]
				if address:
					target.customer_address = address[0]

		# Fetch TDS and Tax Withholding Category
		if target.supplier:
			supplier_data = frappe.db.get_value(
				"Supplier", target.supplier, ["tax_withholding_category"], as_dict=True
			)

			if supplier_data:
				target.apply_tds = 1
				target.tax_withholding_category = supplier_data.get("tax_withholding_category")

		target.custom_other_department = source.item_details[0].get("department_name")
		# target.custom_bill_type = source.gst_name
		target.custom_sales_type = source.voucher_billing_dept_cat_type
		if target.custom_sales_type == "Purchase Bill":
			target.naming_series = "PB-."
		if target.custom_sales_type == "Receipt Voucher":
			target.naming_series = "RV-."
		if target.custom_sales_type == "Sales Return":
			target.naming_series = "SR-."
		if target.custom_sales_type == "On Approval Receipt":
			target.naming_series = "OAR-."
		if target.custom_sales_type == "Hallmark Receipt":
			target.naming_series = "HR-."
		if target.custom_sales_type == "Order Memo":
			target.naming_series = "OM-."
		if target.custom_sales_type == "Purchase Debit Note":
			target.naming_series = "PDN-."
		if target.custom_sales_type == "Purchase Credit Note":
			target.naming_series = "PCN-."

			

	def post_process(source, target):
		set_missing_values(source, target)
		target.posting_date = frappe.utils.now_datetime()
		target.custom_other_department = source.item_details[0].get("department_name")
		source.item_details.pop() # Remove the last Total Element
		total_net_wt = 0
		total_pcs = 0
		total_fine = 0

		if source.generate_bill_type == 'Items':
			for item in source.item_details:
				target.append("items", {
					"custom_department": item.get("department_name"),
					"rate": source.billing_gold_rate,
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

		if source.display_making_charges:
			item_details = get_item_details(
				company=get_default_company(),
				item_code="MakingCharges"
			).get("message")
			frappe.logger("utils").exception(item_details)
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
		"Sales Receipt Voucher",
		source_name,
		{
			"Sales Receipt Voucher": {"doctype": "Purchase Invoice",
			"field_map": {
					"billing_gold_rate": "custom_gold_rate",
					"gold_rate_with_gst": "custom_gold_rate__with_gst",
					"sub_account":"customer_address",
					"shipping_to_address": "shipping_address_name"
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
	frappe.db.set_value("Sales Receipt Voucher", docname, "billing_status", status)
	frappe.db.commit()
# @frappe.whitelist()
# def set_status(docname, status):
# 	frappe.db.set_value("Sales Issue Voucher", docname, "billing_status", status)
# 	frappe.db.commit()

# 	def send_status(self, status):
# 		try:
# 			settings_doc = frappe.get_single("Ascra Billing Settings")
# 			url = settings_doc.api_url
# 			if not url:
# 				frappe.logger("workflow_status_log").exception(f"Api URL Not Configured")
# 				return
# 			billing_status = 1 if status == "Approved" else 2
# 			frappe.logger("workflow_status_log").exception(billing_status)
# 			payload = {
# 				"id": self.name,
# 				"billing_notes": self.billing_notes,
# 				"billing_status": billing_status,
# 				"billing_status_reason_remark": "",
# 				"billing_status_feedback_remark": "", # TODO: Add Fields
# 				"billing_status_approved_reject_by": "", # TODO: Add Fields
# 				"voucher_billing_dept_cat_type": self.voucher_billing_dept_cat_type,
# 				"generate_bill_type": self.generate_bill_type,
# 				"sub_account_name": self.sub_account,
# 				"sub_account_id": 0, # TODO: Fetch this Field Via UI
# 				"display_making_charges": self.display_making_charges,
# 				"godown_bill": self.godown_bill
# 			}
# 			files=[

# 			]
# 			headers = {}

# 			response = requests.request("POST", url, headers=headers, data=payload, files=files)

# 			frappe.logger("workflow_status_log").exception(f"Id : {self.id}, {response.json()}")
# 		except Exception as e:
# 			frappe.logger("workflow_status_log").exception(f"Id : {self.id}, {e}")
