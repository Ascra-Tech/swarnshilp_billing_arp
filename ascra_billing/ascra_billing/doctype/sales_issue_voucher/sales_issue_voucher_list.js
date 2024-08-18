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
// frappe.listview_settings['Sales Issue Voucher'] = {
//   get_indicator: function (doc) {
//         if (doc.delete_status === '1') {
//             return [__('Status1'), 'red', 'delete_status,=,1'];
//         }
//         if (doc.currently_updated === '1') {
//             return [__('Status2'), 'orange', 'currently_updated,=,Status2'];
//         }
//         // return [__('Other Status'), 'grey', 'custom_delete_status,=,Other'];
//     }
// };

// frappe.listview_settings['Sales Issue Voucher'] = {
//     onload: function (listview) {
//         listview.$wrapper.on('render-complete', function () {
//             listview.$wrapper.find('.list-row').each(function () {
//                 var $row = $(this);
//                 var doc = $row.data('data');

//                 if (doc.delete_status === '1') {
//                     $row.css('background-color', 'red');
//                 }else if (doc.currently_updated === '1') {
//                     $row.css('background-color', 'orange'); ;
//                 }
//             });
//         });
//     }
// };

// frappe.listview_settings['Sales Issue Voucher'] = {
//     onload: function (listview) {
//         listview.$wrapper.on('render-complete', function () {
//             // Add custom CSS directly
//             const style = `
//                 .row-status-pending { background-color: #f8d7da !important; }
//                 .row-status-approved { background-color: #d4edda !important; }
//                 .row-status-rejected { background-color: #f5c6cb !important; }
//             `;
//             $('<style>').prop('type', 'text/css').html(style).appendTo('head');
            
//             // Iterate over each row
//             listview.$wrapper.find('.list-row').each(function () {
//                 var $row = $(this);
//                 var doc = $row.data('data'); // Get the data for the row
                
//                 // Apply CSS classes based on field values
//                 if (doc.delete_status === '1') {
//                     $row.addClass('row-status-pending');
//                 } else if (doc.currently_updated === '1') {
//                     $row.addClass('row-status-approved');
//                 }
//             });
//         });
//     }
// };

// frappe.listview_settings['Sales Issue Voucher'] = {
//     onload: function (listview) {
//         // Wait for the DOM to be ready
//         frappe.after_ajax(function () {
//             // Iterate over each row in the list view
//             listview.$wrapper.find('.list-row').each(function () {
//                 var $row = $(this);
//                 var doc = $row.data('data'); // Get the data for the row

//                 // Apply CSS classes based on field values
//                 if (doc.delete_status === '1') {
//                     $(this).css('background-color', 'red'); // Light red
//                 } else if (doc.currently_updated === '1') {
//                     $(this).css('background-color', 'orange'); // Light green
//                 } 
//             });
//         });
//     }
// };

// frappe.listview_settings['Sales Issue '] = {
//     onload: function(listview) {
//         $(document).ready(function() {
//             $(listview.wrapper).on('render_complete', function() {
//                 $(listview.wrapper).find('.list-row').each(function() {
//                     var row = $(this);
//                     var data = row.data('data');
                    
//                     // Example condition: highlight if 'status' is 'Draft'
//                     if (data.status === 'Draft') {
//                         row.addClass('highlighted-row'); // Add a class to the row
//                     }
//                 });
//             });
//         });
//     }
// };

frappe.listview_settings['Sales Issue Voucher'] = {
    refresh: function(listview) {
         $(".list-row-container").each(function(i,onj){
            // if (i%2==0){
            //     $(this).css('background-color', 'green');
            // }
            var delete_status = $(this).find('.filterable[data-filter="delete_status,=,1"]').length > 0;
            if (delete_status) {
                $(this).css('background-color', 'red');
                $(this).css('color', 'white');
            }

            var currently_updated = $(this).find('.filterable[data-filter="currently_updated,=,1"]').length > 0;
            if (currently_updated) {
                $(this).css('background-color', 'orange');
                $(this).css('color', 'white');
            }
        })
        $(".delete_status").hide();
        $(".currently_updated").hide();
        listview.refresh();
         
    },
    onload: function(listview) {
        // Function to hide the delete_status column
        function hideDeleteStatusColumn() {
          console.log(listview);
            $(listview.wrapper).find('.list-table thead th').each(function(index) {
              console.log("jere1");
                var header = $(this);
                var headerText = header.text().trim();
                console.log(headerText)
                // Hide the column if header text matches 'Delete Status'
                if (headerText === 'Delete Status') {
                    header.hide();
                    $(listview.wrapper).find('.list-table tbody td:nth-child(' + (index + 1) + ')').hide();
                }
            });
        }

        // Call hideDeleteStatusColumn when the list view is fully rendered
        //listview.wrapper.on('render_complete', hideDeleteStatusColumn);
        hideDeleteStatusColumn();
        listview.refresh();
    }

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

