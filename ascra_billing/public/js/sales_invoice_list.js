frappe.listview_settings['Sales Invoice'] = {
    button: {
        show: function(doc) {
            return true;
        },
        get_label: function() {
            return __('<i class="fa fa-file-pdf-o" style="font-size:18px;color:red"></i>');
        },
        get_description: function(doc) {
            return __('Print {0}', [doc.name])
        },
        action: function(doc) {
            //frappe.set_route("/app/print/Purchase Invoice/" + doc.name);

            var objWindowOpenResult = window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
              + "doctype=" + encodeURIComponent("Sales Invoice")
              + "&name=" + encodeURIComponent(doc.name)
              + "&trigger_print=0"
              + "&format=Test Issue Voucher(Delivery Challan)"
              + "&no_letterhead=0"
              + "&_lang=en"
            ));

            if(!objWindowOpenResult) {
              msgprint(__("Please set permission for pop-up windows in your browser!")); return;
            }
        }
    },

    onload: function (listview) {
        listview.page.add_action_item(__('Open in View-Only'), function () {
            // Get the selected records
            const selected = listview.get_checked_items();

            // Validate that exactly one record is selected
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to open in view-only mode.'));
                return;
            }

            const docname = selected[0].name;

            // Open the selected record in view-only mode
            frappe.set_route('Form', 'Sales Invoice', docname).then(() => {
                frappe.ui.form.on('Sales Invoice', 'refresh', function (frm) {
                    // Set the main form to read-only
                    frm.set_read_only();

                    // Make the 'items' child table read-only
                    if (frm.fields_dict.items && frm.fields_dict.items.grid) {
                        frm.fields_dict.items.grid.make_read_only();
                    }

                    // Make the 'taxes' child table read-only
                    if (frm.fields_dict.taxes && frm.fields_dict.taxes.grid) {
                        frm.fields_dict.taxes.grid.make_read_only();
                    }
                });
            });
        });

        // Add "Print Record" Button
        listview.page.add_action_item(__('Print Record'), function () {
            // Get the selected records
            const selected = listview.get_checked_items();

            // Validate that exactly one record is selected
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to print.'));
                return;
            }

            const docname = selected[0].name;

            // Construct the URL for printing
            const print_url = `/app/print/Sales%20Invoice/${encodeURIComponent(docname)}`;

            // Open the URL in a new tab
            const print_window = window.open(print_url, '_blank');

            // Validate pop-up blockers
            if (!print_window) {
                frappe.msgprint(__('Please enable pop-ups in your browser to open the print view.'));
            }
        });

        // Add "pdf Record" Button
        listview.page.add_action_item(__('Pdf'), function () {
            // Get the selected records
            const selected = listview.get_checked_items();

            // Validate that exactly one record is selected
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to PDF.'));
                return;
            }

            const docname = selected[0].name;

            var objWindowOpenResult = window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
              + "doctype=" + encodeURIComponent("Sales Invoice")
              + "&name=" + encodeURIComponent(docname)
              + "&trigger_print=0"
              + "&format=Test Issue Voucher(Delivery Challan)"
              + "&no_letterhead=0"
              + "&_lang=en"
            ));

            if(!objWindowOpenResult) {
              msgprint(__("Please set permission for pop-up windows in your browser!")); return;
            }
        });

        // Add "Whatsapp Record" Button
        listview.page.add_action_item(__('Whatsapp'), function () {
            // Get the selected records
            const selected = listview.get_checked_items();

            // Validate that exactly one record is selected
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to sen whatsapp messgae.'));
                return;
            }

            const docname = selected[0].name;

            frappe.call({
                        method: 'ascra_billing.ascra_billing.doc_events.sales_invoice.send_whatsapp_msg',
                        args: {
                            phone_number: '7775864688',
                            header_values: ["ASCRA TECHNOLOGIES"],
                            body_values: [docname],
                            button_values: ["256661"]
                        },
                        callback: function(r) {
                            if (r.message && r.message.success) {
                                frappe.msgprint(__('Message sent successfully.'));
                            } else {
                                frappe.msgprint(__('Failed to send message. Details: ') + r.message.error);
                            }
                        }
                    });
        });
    }
};

//frappe.listview_settings['Sales Invoice'] = {
//    refresh: function(listview) {
//         $(".list-row-container").each(function(i,onj){
//            // if (i%2==0){
//            //     $(this).css('background-color', 'green');
//            // }
//            var cancel = $(this).find('.filterable[data-filter="docstatus,=,2"]').length > 0;
//            if (cancel) {
//                // $(this).css('background-color', 'red');
//                // $(this).css('background-color', '#b52a2a');
//                $(this).css('background-color', '#FD8B8B');
//                // $(this).css('color', 'white');
//            }
//        })
//        listview.refresh();
//
//    },
//};