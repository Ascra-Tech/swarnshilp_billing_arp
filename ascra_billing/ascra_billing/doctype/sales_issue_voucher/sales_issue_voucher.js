// Copyright (c) 2024, alokshukla994@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Issue Voucher', {
	refresh(frm) {
	    setQueryFilter(frm);
        if(frm.doc.docstatus == 1){
            addSIButton(frm);
        }
        else{
            // addActionButton(frm);
        }
	},
	
	account_code(frm) {
        // On change of Account Code Set Query FIlter Again
	    setQueryFilter(frm);
	},

})

function setQueryFilter(frm){
    frappe.call({
        method: "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_address_by_account_code",
         args: {
             account_code : frm.doc.account_code
         },
         callback: (r)=> {
         var address = r.message;
         frm.set_query("sub_account", function() {
             return {
                 filters: {
                         name: ["in", address],
                 },
             };
         });

         frm.set_query("shipping_to_address", function() {
            return {
                filters: {
                        name: ["in", address],
                },
            };
        });


         }
     });
}

function addSIButton(frm){
    frm.add_custom_button(__("Create Sales Invoice"), () =>
        frappe.model.open_mapped_doc({
			method: "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.make_sales_invoice",
			frm: frm,
		}),
    );
}

function addActionButton(frm){
    frm.page.add_action_item(__("Approve"), function() {
        frm.doc.billing_status = 'approve'
        // Submit Doc
        refresh_field("billing_status")
        frm.page.actions.find('[data-label="Edit"],[data-label="Approve"]').parent().parent().remove()
        frm.save('Submit');
    });

    // frm.page.add_action_item(__("Reject"), function() {
    //     if(frm.doc.docstatus == 1){
    //         frappe.throw("Document Already Approved")
    //     }
    //     frappe.msgprint("Rejected");
    //     frm.doc.billing_status = 'reject'
    //     refresh_field("billing_status")
    // });
}