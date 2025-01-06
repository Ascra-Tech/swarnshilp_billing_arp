# Copyright (c) 2025, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AccountSubCode(Document):

	def before_save(self):
		existing_acc_sub_code = frappe.get_all(
			"Account Sub Code",
			filters={"account_code": self.account_code,"account_sub_code":self.account_sub_code}
		)
		if existing_acc_sub_code:
			frappe.throw("Account Code and Account Sub code Already Exist")

	def after_save(self):
		related_customer = frappe.get_all(
			"Customer",
			filters={"custom_account_code": self.account_code, "custom_account_sub_code": self.account_sub_code}
		)
		if related_customer:
			self.customer = related_customer[0]
