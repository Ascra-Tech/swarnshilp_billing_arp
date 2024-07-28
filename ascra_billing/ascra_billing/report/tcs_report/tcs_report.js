// Copyright (c) 2024, alokshukla994@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["TCS Report"] = {
	"filters": [
		{
			fieldname:"from_posting_date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname:"to_posting_date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname:"account_name",
			label: __("Customer"),
			fieldtype: "Data",
			default: "",
		},
		{
			fieldname:"carat",
			label: __("Carat"),
			fieldtype: "Data",
			default: "",
		}
	]
};