import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


def before_save(self, method):
    if self.custom_account_sub_code and self.custom_account_code:
        existing_acc_sub_code = frappe.get_all(
            "Supplier",
            filters={"custom_account_code": self.custom_account_code,
                     "custom_account_sub_code": self.custom_account_sub_code,
                     'name': ['!=', self.name]
                     }
        )
        if existing_acc_sub_code:
            frappe.throw("Account Code and Account Sub code Already Exist")
    elif not self.custom_account_sub_code and self.custom_account_code:
        existing_acc_code = frappe.get_all(
            "Supplier",
            filters={"custom_account_code": self.custom_account_code,
                     'custom_account_sub_code':['is','not set'],
                     'name': ['!=', self.name]
                     }
        )
        if existing_acc_code:
            frappe.throw("Account Code Already Exist")

