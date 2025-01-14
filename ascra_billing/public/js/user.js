frappe.ui.form.on('User', {
    onload: function (frm) {
        if (!frm.doc.custom_bill_type || frm.doc.custom_bill_type.length === 0) {
            frappe.call({
                method: "ascra_billing.ascra_billing.doc_events.purchase_invoice.fetch_bill_types", // Adjust path as necessary
                callback: function (response) {
                    if (response.message) {
                        frappe.msgprint(__('Bill types updated successfully.'));
                    } else {
                        frappe.msgprint(__('No bill types found.'));
                    }
                }
            });
        }
    },
    validate: function(frm) {
        // Before saving, make sure the selected values are correctly assigned
        if (frm.doc.custom_bill_type) {
            let selected_values = frm.doc.custom_bill_type;  // This holds the selected records from the Table MultiSelect field

            // Log the selected values (for debugging)
            console.log('Selected Bill Types:', selected_values);

            // If needed, re-assign the values back to 'bill_type' field
            frm.set_value('custom_bill_type', selected_values);
        }
    },

    before_save: function(frm) {
        // Re-assign the selected values again before the actual save
        if (frm.doc.custom_bill_type) {
            let selected_values = frm.doc.custom_bill_type;

            // Log the values before saving (for debugging)
            console.log('Re-assigning Bill Types:', selected_values);

            frm.set_value('custom_bill_type', selected_values);
        }
    }
});