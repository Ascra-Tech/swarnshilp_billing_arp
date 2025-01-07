// Copyright (c) 2024, alokshukla994@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["KYC Report"] = {
	"filters": [
		{
			fieldname:"account_name",
			label: __("Customer"),
			fieldtype: "Data",
			default: "",
		},
		{
			fieldname:"days",
			label: __("No. Day Inactive Customer"),
			fieldtype: "Data",
			default: "",
		},
	]
};
