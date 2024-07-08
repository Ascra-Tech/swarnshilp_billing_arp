function get_checked_items() {
  // return frappe.get_list_view().get_checked_items();
  let selected = [];
  for (let check of event.view.cur_list.$checks) {
    selected.push(check.dataset.name);
  }
  return selected[0];
  // selected.forEach(selectedId => {
  //   return selectedId
  //   // return get_docket_file_url(selected)
  //   // console.log("test " +selectedId)
  // })
}

function get_docket_file_url(id) {
  frappe.call({
    method: 'ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_docket_file_path',
    args: {
      id: id
    },
    callback: function(r) {
      if (r.message) {
        window.open (r.message, "_blank");
        // frappe.msgprint(r.message);
      }
      frappe.get_list_view().refresh();
    }
  });
}


function ButtonFunction(listview) {
    
    var selected_id = get_checked_items();
    let docket_file = get_docket_file_url(selected_id);
    console.log(docket_file);
    // window.open (docket_file, "_blank")
    // console.log(docket_file);
    // console.log("test" + selected_id);
    // if (items.length > 0) {
    //   let docket_file = get_docket_file_url(51267);
    // } else {
    //   frappe.msgprint('Please select some items first.');
    // }
    // let docket_file = get_docket_file_url(51267);
    // console.log(docket_file)
    // frappe.msgprint(docket_file)
     // window.open (docket_file, "_blank")
    //console.log(items);
    // frappe.msgprint(items)
}


 
frappe.listview_settings['Sales Issue Voucher'] = {
    refresh: function(listview) {
        listview.page.add_inner_button("View Docket No", function() {
            ButtonFunction(listview);
            // var items = get_checked_items();
            // console.log(items);
        });
    },
};
// frappe.listview_settings['Sales Issue Voucher'].onload = function(listview) {
//   listview.page.add_menu_item('View Docket No', function() {
//     // var items = get_checked_items();
//     // if (items.length > 0) {
//     //   //update_status(items);
//     // } else {
//     //   frappe.msgprint('Please select some items first.');
//     // }
//     var items = get_checked_items();
//     if (items.length > 0) {
//       //update_status(items);
//     } else {
//       frappe.msgprint('Please select some items first.');
//     }
//   });
// }

