import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


# def before_save(self, method):
# 	pass
def before_save(self, method):
	if self.roundup_total == 1 :
		self.grand_total = round(self.grand_total)
	if self.roundup_total == 1 :
		self.total_claimed_amount = round(self.total_claimed_amount)
	if self.roundup_total == 1 :
		self.total_sanctioned_amount = round(self.total_sanctioned_amount)
