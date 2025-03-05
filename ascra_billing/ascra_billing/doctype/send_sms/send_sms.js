// Copyright (c) 2025, alokshukla994@gmail.com and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Send SMS", {
 	refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Send SMS'), function() {
                frappe.call({
                    method: "ascra_billing.ascra_billing.doctype.send_sms.send_sms.send_sms",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    freeze_msg: __("Sending SMS"),
                    callback: function(r) {
                        if (r.message === "success") {
                            // Clear the form by creating a new document
                            console.log("r message",r.message);
                            frm.set_value("mobile_number", "");
                            frm.set_value("account", "");
                            frm.set_value("message", "");
                            frm.set_value("template", "");
//                            frappe.msgprint(__('SMS Send'));
                            frm.save_or_update();
                            // Create a fresh document
//                            frappe.new_doc("Send SMS");
                        } else {
                            frappe.msgprint(__('Failed to send sms'));
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    },

    inactive_days: function(frm) {
        if (frm.doc.inactive_days) {
            frappe.call({
                method: "ascra_billing.ascra_billing.doctype.send_sms.send_sms.get_inactive_customers",
                freeze: true,  // Freezes the screen
                freeze_message: __("Fetching Inactive Customers..."),
                args: {
                    inactive_days: frm.doc.inactive_days,
                    exclude_cashhead: frm.doc.exclude_cashhead || 0  // Pass exclude_cashhead checkbox value
                },
                callback: function(r) {
                    if (r.message) {
                        let customer_names = r.message.map(row => row.customer);  // Extract customer names
                        frm.set_value("account", customer_names);  // Set MultiSelect field
                        frm.refresh_field("account");
                        frappe.msgprint(__('Inactive customers updated successfully.'));
                    } else {
                        frappe.msgprint(__('No inactive customers found.'));
                    }
                },
                error: function(error) {
                    frappe.msgprint(__('Failed to fetch inactive customers.'));
                    console.log("Error fetching inactive customers:", error);
                }
            });
        }
    }
 });
