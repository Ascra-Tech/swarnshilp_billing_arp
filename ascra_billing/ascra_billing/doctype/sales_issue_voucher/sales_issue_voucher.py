# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesIssueVoucher(Document):
	def before_save(self):
		if self.total_amt:
			total_amt = float(self.total_amt)
		else:
			total_amt = 0
		if self.tds_amount:
			tds_amount = float(self.tds_amount)
		else:
			tds_amount = 0
		self.net_bill_amt = total_amt + tds_amount

		total_net_wt = 0
		for item in self.item_details:
			total_net_wt = total_net_wt + float(item.net_wt)
			
		total_row = self.item_details[-1]
		if total_row.get("category") == "Total":
			self.item_details.pop()
			
		self.append("item_details", {
			"category": "Total",
			"net_wt": total_net_wt,
			"peices": '',
			"melting": '',
			"wastage": '',
			"fine": '',
			"other_charges": ''
		})



