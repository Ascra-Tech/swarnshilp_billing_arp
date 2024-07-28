# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt
import frappe
import requests


def execute(filters=''):
	# columns, data = [], []
	columns = [
		{
			"fieldname" : "item_name",
			"label" : "Product",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "account_name",
			"label" : "Account Name",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "credit_weight",
			"label" : "Credit Net Weight",
			"fieldtype" : "Float",
			"width" : "250"
		},
		{
			"fieldname" : "debit_weight",
			"label" : "Debit Net Weight",
			"fieldtype" : "Float",
			"width" : "250"
		}
	]

	receipt_condition = ""
	issue_condition =""
	if filters.from_posting_date :
		receipt_condition = " posting_date>='"+filters.from_posting_date+"' and posting_date<='"+filters.to_posting_date+"'"
		issue_condition = " posting_date>='"+filters.from_posting_date+"' and posting_date<='"+filters.to_posting_date+"'"

	# try:
	# 	filters.item_name = filters.item_name
	# except NameError:
	# 	filters.item_name = ""
	# 	print("exceiption")
	
	if filters.item_name :
		issue_condition += "and `tabSales Invoice Item`.`item_name` like '%"+filters.item_name+"%'"

	if filters.item_name :
		receipt_condition += "and `tabPurchase Invoice Item`.`item_name` like '%"+filters.item_name+"%'"

	data = frappe.db.sql("select `tabSales Invoice Item`.`item_name` as item_name,`tabSales Invoice`.`customer_name` as account_name,sum(`tabSales Invoice Item`.`qty`) as debit_weight from `tabSales Invoice Item` left join `tabSales Invoice` on `tabSales Invoice Item`.`parent`=`tabSales Invoice`.`name` where "+issue_condition+" group by `tabSales Invoice`.`name` UNION select `tabPurchase Invoice Item`.`item_name` as item_name,`tabPurchase Invoice`.`supplier_name` as account_name,sum(`tabPurchase Invoice Item`.`qty`) as credit_weight from `tabPurchase Invoice Item` left join `tabPurchase Invoice` on `tabPurchase Invoice Item`.`parent`=`tabPurchase Invoice`.`name` where "+receipt_condition+" group by `tabPurchase Invoice`.`name`",as_dict=1)
	# print(data)
	return columns, data
