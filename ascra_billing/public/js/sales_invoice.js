

frappe.ui.form.on('Sales Invoice', {
	refresh(frm, cdt, cdn) {

        var data = frm.doc.items
        data.forEach(function(e){
            // if (e.custom_item == "MakingCharges"){
            //     $("[data-idx='"+e.idx+"']").css('pointer-events','none');;	
            // }
        })

        frm.set_query("item_code", "items", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
                        custom_department: d.custom_department
                    },
			};
		});

        frm.set_query("custom_item", "items", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
                        custom_department: d.custom_department
                    },
			};
		});

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
