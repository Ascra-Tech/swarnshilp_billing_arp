// frappe.listview_settings['Sales Invoice'] = {
//     // add fields to fetch
//     add_fields: ['title', 'public'],
//     // set default filters
//     filters: [
//         ['public', '=', 1]
//     ],
//     hide_name_column: true, // hide the last column which shows the `name`
//     hide_name_filter: true, // hide the default filter field for the name column
//     onload(listview) {
//         // triggers once before the list is loaded
//     },
//     before_render() {
//         // triggers before every render of list records
//     },

//     // set this to true to apply indicator function on draft documents too
//     has_indicator_for_draft: false,

//     get_indicator(doc) {
//         console.log("herer")
//         print(doc)
//         // customize indicator color
//         if (doc.public) {
//             return [__("Public"), "green", "public,=,Yes"];
//         } else {
//             return [__("Private"), "darkgrey", "public,=,No"];
//         }
//     },
//     primary_action() {
//         // triggers when the primary action is clicked
//     },
//     get_form_link(doc) {
//         // override the form route for this doc
//     },
//     // add a custom button for each row
//     button: {
//         show(doc) {
//             return doc.reference_name;
//         },
//         get_label() {
//             return 'View';
//         },
//         get_description(doc) {
//             return __('View {0}', [`${doc.reference_type} ${doc.reference_name}`])
//         },
//         action(doc) {
//             frappe.set_route('Form', doc.reference_type, doc.reference_name);
//         }
//     },
//     // format how a field value is shown
//     formatters: {
//         title(val) {
//             print(val)
//             if(val=="Grand Total") 
//                 return val.bold();
//         },
//         public(val) {
//             return val ? 'Yes' : 'No';
//         }
//     }
// }

frappe.listview_settings['Sales Invoice'] = {
    refresh: function(listview) {
         $(".list-row-container").each(function(i,onj){
            // if (i%2==0){
            //     $(this).css('background-color', 'green');
            // }
            var cancel = $(this).find('.filterable[data-filter="docstatus,=,2"]').length > 0;
            if (cancel) {
                // $(this).css('background-color', 'red');
                // $(this).css('background-color', '#b52a2a');
                $(this).css('background-color', '#FD8B8B');
                // $(this).css('color', 'white');
            }
        })
        listview.refresh();

    },
};