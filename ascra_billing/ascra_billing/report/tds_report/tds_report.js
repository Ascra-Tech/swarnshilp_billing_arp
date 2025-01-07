// Copyright (c) 2024, alokshukla994@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["TDS Report"] = {
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

function lock_unlock(invoice_number,status) {
	console.log("sdfsdf");
    frappe.call({
            method: 'ascra_billing.ascra_billing.doctype.invoice_tds.invoice_tds.update_data_lock_unlock',
            args: {
                invoice_number: invoice_number,
                status: status
            },
            callback: function(response) {
                if (response.message) {
                    // Show a success message
                    frappe.msgprint(__('Status updated to: ' + response.message.status));
                    // frm.reload_doc();  // Reload the form to reflect the changes
                }
            }
        });
}