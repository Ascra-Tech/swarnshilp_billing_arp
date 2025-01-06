

frappe.ui.form.on('Sales Invoice', {
	refresh(frm, cdt, cdn) {

        var data = frm.doc.items
        data.forEach(function(e){
            // if (e.custom_item == "MakingCharges"){
            //     $("[data-idx='"+e.idx+"']").css('pointer-events','none');;	
            // }
        })

//        frm.set_query("item_code", "items", function (doc, cdt, cdn) {
//			let d = locals[cdt][cdn];
//			return {
//				filters: {
//                        custom_department: d.custom_department
//                    },
//			};
//		});
//
//        frm.set_query("custom_item", "items", function (doc, cdt, cdn) {
//			let d = locals[cdt][cdn];
//			return {
//				filters: {
//                        custom_department: d.custom_department
//                    },
//			};
//		});

		frm.fields_dict["items"].grid.get_field("custom_item").get_query = function(doc, cdt, cdn) {
            let row = locals[cdt][cdn];

            return {
                query: "ascra_billing.ascra_billing.doc_events.sales_invoice.filter_items_by_department",
                filters: {
                    department: frm.doc.custom_other_department
                }
            };
        };

	},
	
})

frappe.ui.form.on('Sales Invoice Item', {
	custom_item: function (frm, cdt, cdn) {

		var row = locals[cdt][cdn];
    

		if (row.custom_item) {
            row.item_code = row.custom_item
			row.rate = frm.doc.custom_gold_rate
            frappe.call({
                method: "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_item_details",
                 args: {
                     company : frm.doc.company,
                     item_code: row.custom_item
                 },
                 callback: (r)=> {
                    var data = r.message
                    row.uom = data.message.stock_uom
                    row.income_account = data.message.income_account
                    row.item_name = data.message.item_name
                    row.cost_center = data.message.cost_center
                    refresh_field("items")

                    frm.save('Save');
                 }
             });
            refresh_field("items")
		}

	},
})

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        update_tcs_payable(frm);
    },

    validate : function(frm) {
        update_tcs_payable(frm);
    }
});

function update_tcs_payable(frm) {
    // Loop through the taxes and charges table
    // frappe.msgprint("oooo"+frm.doc.voucher_billing_dept_cat_type);
    // frm.doc.voucher_billing_dept_cat_type=="Sale Bill" || 

    if (frm.doc.voucher_billing_dept_cat_type=="On Approval Issue" || frm.doc.voucher_billing_dept_cat_type=="Issue Voucher" || frm.doc.voucher_billing_dept_cat_type=="Hallmark Issue" || frm.doc.voucher_billing_dept_cat_type=="Delivery Challan") {
        frm.doc.taxes.forEach(function(tax) {
            // Check if the tax entry is TCS Payable
            if (tax.account_head === 'TDS Payable - ATL') {  // Ensure this matches the exact account name
                // Set both rate and amount to 0
                frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
                frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
            }
            
            if (tax.account_head === 'TCS Payable - ATL') {  // Ensure this matches the exact account name
                // Set both rate and amount to 0
                frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
                frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
            }
        });
        // Refresh the field to reflect changes
        frm.refresh_field('taxes_and_charges');
    }
    else {
        let customer_id = frm.doc.name; // Current customer record

        if (customer_id) {
            frappe.db.get_value('Customer', customer_id, 'pan', (r) => {
                if (r && r.pan) {
                    if(r.pan=="AAPCS1960H") {
                        frm.doc.taxes.forEach(function(tax) {
                            // Check if the tax entry is TCS Payable
                            if (tax.account_head === 'TDS Payable - ATL') {  // Ensure this matches the exact account name
                                // Set both rate and amount to 0
                                frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
                                frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
                            }
                            
                            if (tax.account_head === 'TCS Payable - ATL') {  // Ensure this matches the exact account name
                                // Set both rate and amount to 0
                                frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
                                frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
                            }
                        });
                        // Refresh the field to reflect changes
                        frm.refresh_field('taxes_and_charges');
                    }
                } 
            });
        }

    }
}




