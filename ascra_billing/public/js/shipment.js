frappe.ui.form.on('Shipment', {
	refresh:function(frm) {
		frm.add_custom_button(__("Follow Up"), () => {
			frappe.set_route("List", "Follow-Up", {"shipment": frm.doc.name})
		});
	}
});