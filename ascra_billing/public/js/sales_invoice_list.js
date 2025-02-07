frappe.listview_settings['Sales Invoice'] = {
    button: {
        show: function(doc) {
            return true;
        },
        get_label: function() {
            return __(
                `<i class="fa fa-file-pdf-o" style="font-size:18px;color:red; cursor:pointer;" data-format="Test Issue Voucher(Delivery Challan)" onclick="download_pdf(this)"></i>
                 &nbsp;&nbsp;
                 <i class="fa fa-file-pdf-o" style="font-size:18px;color:blue; cursor:pointer;" data-format="Print Label Sample" onclick="download_pdf(this)"></i>
                 &nbsp;&nbsp;
                <i class="fa fa-file-pdf-o" style="font-size:18px;color:green; cursor:pointer;" data-format="Declaration" onclick="download_pdf(this)"></i>
                 &nbsp;&nbsp;
                 <i class="fa fa-pencil" style="font-size:18px;color:blue; cursor:pointer;" onclick="redirectToInvoice(this)"></i>`
            );

        },
        get_description: function(doc) {
            return __('Print {0}', [doc.name]);
        },
        action: function(doc) {
            // frappe.msgprint(__('Click on the respective icon to download the required print format.'));
        }
    },

    onload: function (listview) {

         // ✅ Export Button
        listview.page.add_inner_button(__("Export"), function() {
            frappe.set_route("Form", "Data Export").then(() => {
                frappe.after_ajax(() => {
                    // Set the Doctype field
                    frappe.model.set_value("Data Export", "Data Export", "reference_doctype", "Sales Invoice");

                    // Set the Export Format field
                    frappe.model.set_value("Data Export", "Data Export", "export_format", "Excel");

                });
            });


        });
        // ✅ Export Button

        // hide created by for other expect admin
        if (frappe.user.has_role("Administrator")){
            console.log('----------')
        } else {
            $(`.list-row-col:contains("Creator")`).hide();
            // Ensure listview.columns exists
            if (listview.columns && Array.isArray(listview.columns)) {
                listview.columns = listview.columns.filter(col => {
                    return col.df?.label !== "Creator" && col.df?.name !== "Sales Invoice-custom_creator";
                });
                
                listview.refresh();
            } else {
                console.warn("listview.columns is undefined or not an array.");
            }
        }
        
        // hide created by for other expect admin

        // ✅ Open in View-Only Mode
        listview.page.add_action_item(__('Open in View-Only'), function () {
            const selected = listview.get_checked_items();
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to open in view-only mode.'));
                return;
            }

            const docname = selected[0].name;
            frappe.set_route('Form', 'Sales Invoice', docname).then(() => {
                frappe.ui.form.on('Sales Invoice', 'refresh', function (frm) {
                    frm.set_read_only();
                    if (frm.fields_dict.items && frm.fields_dict.items.grid) {
                        frm.fields_dict.items.grid.make_read_only();
                    }
                    if (frm.fields_dict.taxes && frm.fields_dict.taxes.grid) {
                        frm.fields_dict.taxes.grid.make_read_only();
                    }
                });
            });
        });

        // ✅ Print Record Button
        listview.page.add_action_item(__('Print Record'), function () {
            const selected = listview.get_checked_items();
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to print.'));
                return;
            }

            const docname = selected[0].name;
            const print_url = `/app/print/Sales%20Invoice/${encodeURIComponent(docname)}`;
            const print_window = window.open(print_url, '_blank');

            if (!print_window) {
                frappe.msgprint(__('Please enable pop-ups in your browser to open the print view.'));
            }
        });

        // ✅ Download PDF Button
        listview.page.add_action_item(__('PDF'), function () {
            const selected = listview.get_checked_items();
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to generate PDF.'));
                return;
            }

            const docname = selected[0].name;
            const pdf_url = frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
                + "doctype=" + encodeURIComponent("Sales Invoice")
                + "&name=" + encodeURIComponent(docname)
                + "&trigger_print=0"
                + "&format=Test Issue Voucher(Delivery Challan)"
                + "&no_letterhead=0"
                + "&_lang=en"
            );

            const objWindowOpenResult = window.open(pdf_url);
            if (!objWindowOpenResult) {
                frappe.msgprint(__("Please set permission for pop-up windows in your browser!"));
            }
        });

        // ✅ Send WhatsApp Message
        listview.page.add_action_item(__('WhatsApp'), function () {
            const selected = listview.get_checked_items();
            if (selected.length !== 1) {
                frappe.msgprint(__('Please select exactly one record to send a WhatsApp message.'));
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

window.redirectToInvoice = function (element) {
    
    var parentButton = element.closest('button');
    
    var dataName = parentButton.getAttribute('data-name');
    if (dataName){
        window.location.href = `/app/sales-invoice/${dataName}`;
    }



};

window.download_pdf = function(element) {
    const format = element.getAttribute("data-format");

    var parentButton = element.closest('button');
    
    // Get the data-name attribute from the parent button
    var dataName = parentButton.getAttribute('data-name');

    // Get the selected document name dynamically from ListView
    frappe.db.get_list("Sales Invoice", {
        fields: ["name"],
        limit: 1
    }).then(response => {
        if (response && response.length > 0) {
            const docname = dataName;
            const pdf_url = frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
                + "doctype=Sales Invoice"
                + "&name=" + encodeURIComponent(docname)
                + "&trigger_print=0"
                + "&format=" + encodeURIComponent(format)
                + "&no_letterhead=0"
                + "&_lang=en"
            );

            const objWindowOpenResult = window.open(pdf_url);
            if (!objWindowOpenResult) {
                // frappe.msgprint(__("Please set permission for pop-up windows in your browser!"));
            }
        } else {
            frappe.msgprint(__("No document found."));
        }
    });
};
