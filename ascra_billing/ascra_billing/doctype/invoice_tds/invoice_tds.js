
// frappe.ui.form.on("Invoice TDS", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Invoice TDS', {
    onload: function(frm) {
    	console.log("here");
    	frm.doc.invoice_number = 'ACC-SINV-2024-00012';
        if (frm.doc.invoice_number) {
            // Call server-side method to get data
            frappe.call({
                method: 'ascra_billing.ascra_billing.doctype.invoice_tds.invoice_tds.get_data_from_invoice',
                args: {
                    'invoice_number': frm.doc.invoice_number
                },
                callback: function(response) {
                    if (response.message) {
                        // Populate fields with the returned data
                        frm.set_value('account_name', response.message.customer_name);
                        frm.set_value('total_amount', response.message.total_amount);
                        frm.set_value('invoice_date', response.message.invoice_date);
                        frm.set_value('bill_type', 'ACCOUNTING_BILL');
                        frm.set_value('pan_no', response.message.pan_no);
                        frm.set_value('account_code', response.message.account_code);
                        frm.set_value('amount', response.message.amount);

                    }
                }
            });
        }
    },
    refresh: function(frm) {
        frm.add_custom_button(__('Lock'), function() {
            frappe.msgprint(__('Anchor tag clicked!'));
        });
    }

});

// function lock_unlock(invoice_number,status){
// 	frappe.call({
//             method: 'ascra_billing.ascra_billing.doctype.invoice_tds.invoice_tds.update_data_lock_unlock',
//             args: {
//                 'invoice_number': invoice_number,
//                 'status' : status
//             },
//             callback: function(response) {
//                 if (response.message) {
//                 	location.reload();
//                 }
//             }
//         });
// }



// frappe.ui.form.on('Invoice TDS', {
//     onload: function(frm) {

        // Add a custom button to update status
        // frm.add_custom_button(__('Update Status'), function() {
        //     // Define the new status you want to set
        //     let new_status = 'Closed';

        //     // Call the server-side method to update the status
        //     frappe.call({
        //         method: 'ascra_billing.ascra_billing.doctype.invoice_tds.invoice_tds.update_data_lock_unlock',
        //         args: {
        //             invoice_number: frm.doc.name,
        //             new_status: new_status
        //         },
        //         callback: function(response) {
        //             if (response.message) {
        //                 // Show a success message
        //                 frappe.msgprint(__('Status updated to: ' + response.message.status));
        //                 frm.reload_doc();  // Reload the form to reflect the changes
        //             }
        //         }
        //     });
        // });
//     }
// });

// frappe.ui.form.on('Invoice TDS', {
//     refresh: function(frm) {
//         // Add custom button to the form
//         frm.add_custom_button(__('Lock'), function() {
//             lock_unlock();
//         });
//     }
// });

// frappe.query_reports["Invoice TDS"] = {
//     // onload function executes when the report is loaded
//     onload: function(report) {
//         // Define your custom function
//         function lock_unlock() {
//             console.log("lock_unlock function called");
//             // Add your logic here
//         }

//         // Example of calling the function
//         lock_unlock();

//         // Optionally, you can add event listeners or interact with the report
//         document.querySelector("#my-custom-button").addEventListener("click", function() {
//             lock_unlock();
//         });
//     },
    
//     // Optionally, you can add other properties like filters
//     // filters: [
//     //     {
//     //         fieldname: 'date',
//     //         label: __('Date'),
//     //         fieldtype: 'Date',
//     //         default: frappe.datetime.get_today()
//     //     }
//     // ]

frappe.query_reports["Invoice TDS"] = {
    onload: function(report) {
        // Define custom function
        function showCustomMessage() {
            frappe.msgprint({
                message: 'Welcome to My Custom Report!',
                title: 'Greetings',
                indicator: 'blue'
            });
        }

        // Call the custom function
        showCustomMessage();
    }
};


