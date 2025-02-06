

frappe.ui.form.on('Sales Invoice', {
	refresh(frm, cdt, cdn) {

        // paste will not allowed code
        let fields = [
        'custom_gold_rate__with_gst',
        'custom_total_pcs',
        'custom_hallmark_amount',
        'custom_logistic_amount',
        'custom_total_oc',
        'custom_gold_rate','custom_sales_issue_voucher','custom_gst_percentage','custom_gold_purity'
        ];

        fields.forEach(field => {
            frm.fields_dict[field].$wrapper.find('input').on('paste', function (e) {
                e.preventDefault();
                frappe.msgprint(__('Pasting is not allowed in this field.'));
            });
        });

        

        let restricted_fields = ["qty",'custom_gross_wt'];

        frm.fields_dict['items'].grid.wrapper.on('paste', 'input[data-fieldname]', function(e) {
            let fieldname = $(this).attr("data-fieldname");
            if (restricted_fields.includes(fieldname)) {
                e.preventDefault(); // Prevent pasting
                frappe.msgprint(__('Pasting is not allowed in this field.'));
            }
        });

        // paste will not allowed code
        
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

        if (frm.doc.custom_other_department){
            frm.fields_dict["items"].grid.get_field("custom_item").get_query = function(doc, cdt, cdn) {
                let row = locals[cdt][cdn];
                return {
                    query: "ascra_billing.ascra_billing.doc_events.sales_invoice.filter_items_by_department",
                    filters: {
                        department: frm.doc.custom_other_department
                    }
                };
            };
        }

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
    item_add: function (frm) {
        calculate_total_pcs(frm);
        calculate_totals(frm)
    },
    items_remove: function (frm) {
        calculate_total_pcs(frm);
        calculate_totals(frm)
    },
    validate : function(frm) {
        update_tcs_payable(frm);
        calculate_totals(frm)
    },
    before_save: function(frm){
        calculate_totals(frm)
    }
});

function calculate_total_pcs(frm) {
    let total_pieces = 0;

    // Iterate over child table items
    frm.doc.items.forEach(item => {
        total_pieces += item.custom_pieces || 0;
    });

    // Update the custom_total_pcs field in the parent doctype
    frm.set_value('custom_total_pcs', total_pieces);
}

function calculate_totals(frm) {
    const excluded_keywords = ["making charges", "makingcharges"]; // Keywords to identify excluded items
    let total_qty = 0;
    let total_amount = 0;
    let total_taxes = 0;

    // Loop through the items table
    frm.doc.items.forEach(item => {
        // Check if item_name contains any excluded keyword
        const is_excluded = excluded_keywords.some(keyword =>
            item.item_name.toLowerCase().includes(keyword)
        );

        if (!is_excluded) {
            total_qty += item.qty || 0; // Add to total_qty if not excluded
            total_amount += item.amount || 0; // Add to total_amount if not excluded
        }
    });

    // Calculate taxes excluding making charges
    frm.doc.taxes.forEach(tax => {
        let tax_amount = 0;

        frm.doc.items.forEach(item => {
            const is_excluded = excluded_keywords.some(keyword =>
                item.item_name.toLowerCase().includes(keyword)
            );

            if (!is_excluded) {
                const item_tax_amount = (item.amount || 0) * (tax.rate / 100);
                tax_amount += item_tax_amount;
            }
        });

        tax.tax_amount = tax_amount;
        total_taxes += tax_amount;
    });

    // Update the total_qty and total fields in the Sales Invoice
    frm.set_value("total_qty", total_qty);
    frm.set_value("total", total_amount);
    frm.set_value("total_taxes_and_charges", total_taxes);
    // Refresh fields to ensure the updated values are shown in the form
    frm.refresh_field("total_qty");
    frm.refresh_field("total");
    frm.refresh_field("total_taxes_and_charges");
}

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
            // frappe.db.get_value('Customer', customer_id, 'pan', (r) => {
            //     if (r && r.pan) {
            //         console.log(r.pan)
            //         if(r.pan=="AAPCS1960H") {
            //             frm.doc.taxes.forEach(function(tax) {
            //                 // Check if the tax entry is TCS Payable
            //                 if (tax.account_head === 'TDS Payable - ATL') {  // Ensure this matches the exact account name
            //                     // Set both rate and amount to 0
            //                     frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
            //                     frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
            //                 }
                            
            //                 if (tax.account_head === 'TCS Payable - ATL') {  // Ensure this matches the exact account name
            //                     // Set both rate and amount to 0
            //                     frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
            //                     frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
            //                 }
            //             });
            //             // Refresh the field to reflect changes
            //             frm.refresh_field('taxes_and_charges');
            //         }
            //     } 
            // });
        }

    }
}




