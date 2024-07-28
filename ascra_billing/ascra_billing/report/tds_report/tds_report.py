# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	# columns, data = [], []
	columns = [
		{
			"fieldname" : "invoice_no",
			"label" : "Invoice No",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "posting_date",
			"label" : "Date",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "customer_code",
			"label" : "Account Code",
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
			"fieldname" : "pan",
			"label" : "Pan No.",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "tan",
			"label" : "Tan No.",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "hsn",
			"label" : "HSN",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "carat",
			"label" : "Carat",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "total_amt",
			"label" : "Total Amt",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "tds_amount",
			"label" : "TDS Amt",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "total_payable_amount",
			"label" : "Total Payable Amt",
			"fieldtype" : "Float",
			"width" : "250"
		}
	]
	query_append = ""
	if filters.from_posting_date :
		query_append = " posting_date>='"+filters.from_posting_date+"' and posting_date<='"+filters.to_posting_date+"'"

	# if filters.carat :
	# 	query_append += " and `tabSales Invoice Item`.`custom_department` like'%"+filters.carat+"%'"

	# if filters.account_name :
	# 	query_append += " and `tabSales Invoice`.customer_name like'%"+filters.account_name+"%'"
	
	# where "+issue_condition+"
	# ,`tabCustomer`.`pan` as pan,`tabSales Invoice Item`.`gst_hsn_code` as hsn

	# and `tabSales Taxes and Charges`.description='TDS Payable'
	
	data = frappe.db.sql("select `tabSales Invoice`.`name` as invoice_no,`tabSales Invoice`.`posting_date`,tabCustomer.custom_account_code as customer_code,`tabSales Invoice`.`customer_name`,`tabSales Invoice Item`.`item_name` as item_name,`tabSales Invoice Item`.custom_department as carat,`tabSales Invoice`.`customer_name` as account_name,tabCustomer.custom_tan as tan,`tabSales Invoice`.total as total_amt,`tabSales Taxes and Charges`.tax_amount as tds_amount,`tabSales Invoice`.grand_total as total_payable_amount from `tabSales Invoice Item` left join `tabSales Invoice` on `tabSales Invoice Item`.`parent`=`tabSales Invoice`.`name` join tabCustomer on `tabSales Invoice`.`customer`= tabCustomer.name left join `tabSales Taxes and Charges` on `tabSales Invoice`.name=`tabSales Taxes and Charges`.parent where "+query_append+"  group by `tabSales Invoice`.`name`",as_dict=1)
	# print("select `tabSales Invoice`.`name` as invoice_no,`tabSales Invoice`.`posting_date`,tabCustomer.custom_account_code as customer_code,`tabSales Invoice`.`customer_name`,`tabSales Invoice Item`.`item_name` as item_name,`tabSales Invoice Item`.custom_department as carat,`tabSales Invoice`.`customer_name` as account_name,tabCustomer.custom_tan as tan,`tabSales Invoice`.total as total_amt,`tabSales Taxes and Charges`.tax_amount as tcs_amount,`tabSales Invoice`.grand_total as total_payable_amount from `tabSales Invoice Item` left join `tabSales Invoice` on `tabSales Invoice Item`.`parent`=`tabSales Invoice`.`name` join tabCustomer on `tabSales Invoice`.`customer`= tabCustomer.name left join `tabSales Taxes and Charges` on `tabSales Invoice`.name=`tabSales Taxes and Charges`.parent where "+query_append+"  group by `tabSales Invoice`.`name`")
	
	return columns, data
