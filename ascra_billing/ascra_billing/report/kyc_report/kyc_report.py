# Copyright (c) 2024, alokshukla994@gmail.com and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	# columns, data = [], []
	columns = [
		{
			"fieldname" : "account_name",
			"label" : "Account Name",
			"fieldtype" : "Data",
			"width" : "250"
		},
		{
			"fieldname" : "customer_code",
			"label" : "Account Code",
			"fieldtype" : "Data",
			"width" : "150"
		},
		{
			"fieldname" : "sub_code",
			"label" : "Sub code",
			"fieldtype" : "Data",
			"width" : "150"
		},
		{
			"fieldname" : "city",
			"label" : "City",
			"fieldtype" : "Data",
			"width" : "150"
		},
		{
			"fieldname" : "custom_kyc_certificate",
			"label" : "KYC",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "custom_gst_certificate",
			"label" : "GST",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "custom_tdstcs_certificate",
			"label" : "TDS/TCS",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "custom_pan_card",
			"label" : "PAN",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "custom_hallmark_liacence",
			"label" : "HALLMARK",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "custom_aadhar_card",
			"label" : "AADHAR",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "bill_generated_date",
			"label" : "BILL GENERATED",
			"fieldtype" : "Data",
			"width" : "100"
		},
		{
			"fieldname" : "status",
			"label" : "Status",
			"fieldtype" : "Data",
			"width" : "100"
		}



	]
	query_append = ""
	if filters.account_name :
		query_append = " tabCustomer.customer_name='"+filters.account_name+"'"

	if query_append :
		query_append = "where " + query_append 

	# if filters.carat :
	# 	query_append += " and `tabSales Invoice Item`.`custom_department` like'%"+filters.carat+"%'"

	# if filters.account_name :
	# 	query_append += " and `tabSales Invoice`.customer_name like'%"+filters.account_name+"%'"
	
	# where "+issue_condition+"
	# ,`tabCustomer`.`pan` as pan,`tabSales Invoice Item`.`gst_hsn_code` as hsn

	# and `tabSales Taxes and Charges`.description='TDS Payable'

	data = frappe.db.sql("select tabCustomer.custom_account_code as customer_code,`tabCustomer`.`customer_name` as account_name,if(custom_kyc_certificate!='', 'YES', 'NO') as custom_kyc_certificate,if(custom_gst_certificate!='', 'YES', 'NO') as custom_gst_certificate,if(custom_tdstcs_certificate!='', 'YES', 'NO') as custom_tdstcs_certificate,if(custom_pan_card!='', 'YES', 'NO') as custom_pan_card,if(custom_hallmark_liacence!='', 'YES', 'NO') as custom_hallmark_liacence,if(custom_aadhar_card!='', 'YES', 'NO') as custom_aadhar_card,if((custom_kyc_certificate!='' and custom_gst_certificate!='' and custom_tdstcs_certificate!='' and custom_pan_card!='' and custom_hallmark_liacence!='' and custom_aadhar_card!=''),'Completed','Pending') as status,(select posting_date from `tabSales Invoice` where `tabSales Invoice`.customer_name=`tabCustomer`.customer_name and `tabSales Invoice`.einvoice_status='GENERATED' order by `tabSales Invoice`.posting_date,`tabSales Invoice`.posting_time limit 1) as bill_generated_date  from tabCustomer "+query_append+"",as_dict=1)
	return columns, data
