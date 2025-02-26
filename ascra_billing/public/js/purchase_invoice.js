

frappe.ui.form.on('Purchase Invoice', {
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
    validate: function (frm) {
        if (!frm.doc.supplier) return;

        frappe.db.get_value("Supplier", frm.doc.supplier, "tax_withholding_category", (supplierData) => {
            if (supplierData && supplierData.tax_withholding_category) {
                let tax_category = supplierData.tax_withholding_category;

                frappe.call({
                    method: "ascra_billing.ascra_billing.doc_events.purchase_invoice.get_tax_details",
                    args: {
                        tax_category: tax_category
                    },
                    callback: function (r) {

                        if (r.message && r.message.length > 0) {
                            let taxRates = r.message;
                            let tds_rate = taxRates.length ? taxRates[0].tax_withholding_rate : 1;


                            let tds_account = "TDS Payable - A";
                            let net_total = frm.doc.net_total || 0;
                            let tds_amount = (net_total * tds_rate) / 100;

                            let rounded_tds_amount = (tds_amount % 1) >= 0.5 
                                ? Math.ceil(tds_amount)  
                                : Math.floor(tds_amount); 

                            let tds_entry = frm.doc.taxes.find(tax => tax.account_head === tds_account);

                            if (!tds_entry) {
                                frm.add_child("taxes", {
                                    charge_type: "Actual",
                                    account_head: tds_account,
                                    rate: tds_rate,
                                    tax_amount: rounded_tds_amount,
                                });
                            } else {
                                tds_entry.rate = tds_rate;
                                tds_entry.tax_amount = rounded_tds_amount;
                            }

                            frm.refresh_field("taxes");
                        } else {
                            console.log("No Tax Withholding Rate found.");
                        }
                    }
                });
            }
        });
    }	
})

frappe.ui.form.on('Purchase Invoice Item', {
	custom_item: function (frm, cdt, cdn) {

		var row = locals[cdt][cdn];
    

		if (row.custom_item) {
            row.item_code = row.custom_item
			row.rate = frm.doc.custom_gold_rate
            frappe.call({
                method: "ascra_billing.ascra_billing.doctype.sales_receipt_voucher.sales_receipt_voucher.get_item_details",
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

// frappe.ui.form.on('Purchase Invoice', {
//     before_save: function(frm) {
//         if (frm.doc.custom_sales_type=="On Approval Receipt" || frm.doc.custom_sales_type=="Hallmark Receipt" || frm.doc.custom_sales_type=="Receipt Voucher" || frm.doc.custom_sales_type=="Order Memo") {
//             // Remove TCS related fields if the condition is not met
//             frm.doc.tcs_amount = 0;
//             frm.doc.tcs_rate = 0;
//             frm.refresh_fields(); // Refresh the form to apply changes
//         }
//     }
// });

frappe.ui.form.on('Purchase Invoice', {
    refresh: function(frm) {
    //     // Call the function when form is loaded
    //     remove_tds_tcs_rows();
        update_tcs_payable(frm);
    },

    validate : function(frm) {
        update_tcs_payable(frm);
    }
});

function update_tcs_payable(frm) {
    // Loop through the taxes and charges table
    // frappe.msgprint("oooo"+frm.doc.custom_sales_type);
    if (frm.doc.custom_sales_type=="On Approval Receipt" || frm.doc.custom_sales_type=="Hallmark Receipt" || frm.doc.custom_sales_type=="Receipt Voucher" || frm.doc.custom_sales_type=="Order Memo") {
        frm.doc.taxes.forEach(function(tax) {
            // Check if the tax entry is TCS Payable
            if (tax.account_head === 'TDS Payable - A') {  // Ensure this matches the exact account name
                // Set both rate and amount to 0
                frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
                frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
            }
            
            if (tax.account_head === 'TCS Payable - A') {  // Ensure this matches the exact account name
                // Set both rate and amount to 0
                frappe.model.set_value(tax.doctype, tax.name, 'rate', 0);
                frappe.model.set_value(tax.doctype, tax.name, 'amount', 0);
            }
        });
        // Refresh the field to reflect changes
        frm.refresh_field('taxes_and_charges');
    }
}

