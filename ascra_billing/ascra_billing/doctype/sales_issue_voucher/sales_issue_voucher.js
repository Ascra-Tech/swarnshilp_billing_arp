// Copyright (c) 2024, alokshukla994@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Issue Voucher', {
	refresh(frm) {
        setStatusPill(frm)
	    setQueryFilter(frm);
        if(frm.doc.docstatus == 1){
            addSIButton(frm);
        }
        else{
            addActionButton(frm);
        }
	},
	
	account_code(frm) {
        // On change of Account Code Set Query FIlter Again
	    setQueryFilter(frm);
	},
    on_update(frm){
        console.log("Hey")
    }

})

function setStatusPill(frm){
        if(document.getElementById('doc-status')){
            document.getElementById('doc-status').remove();
        }
        let title_element = $(`h3[title="${frm.doc.name}"]`).parent();
        title_element = title_element[0];
        const pillspan = document.createElement('span');
        pillspan.setAttribute('class', 'indicator-pill whitespace-nowrap');

        let color = 'grey';  // Default color is grey
        let status = 'Pending'
        if (frm.doc.billing_status === 'approve') {
            color = 'green';
            status = 'Approved'
        } else if (frm.doc.billing_status === 'reject') {
            color = 'red';
            status = 'Rejected'
        }

        pillspan.classList.add(
            color
        );
        pillspan.setAttribute('id', 'doc-status');
        pillspan.style.marginLeft = 'var(--margin-sm)';
        const textspan = document.createElement('span');
        textspan.innerHTML = status;
        pillspan.appendChild(textspan);

        title_element.appendChild(pillspan);
  }


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
        frm.page.actions.find('[data-label="Reject"],[data-label="Approve"]').parent().parent().remove()
        
        frappe.call({
            method: "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.submit_doc",
             args: {
                doc: frm.doc
             },
             callback: (r)=> {
                
                // window.location.reload();
    
             }
         });


        frappe.model.open_mapped_doc({
			method: "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.make_sales_invoice",
			frm: frm,
		})

    });

    frm.page.add_action_item(__("Reject"), function() {
        if(frm.doc.docstatus == 1){
            frappe.throw("Document Already Approved")
        }
        frappe.msgprint("Rejected");
        // frm.doc.billing_status = 'reject'
        // frm.set_value("billing_status", "reject")

        frappe.call({
            method: "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.set_status",
             args: {
                docname: frm.doc.name,
                status : 'reject'
             },
             callback: (r)=> {
                
                window.location.reload();
    
             }
         });


        refresh_field("billing_status")
    });
}