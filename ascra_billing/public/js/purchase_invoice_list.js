frappe.listview_settings['Purchase Invoice'] = {
    refresh: function(listview) {
         $(".list-row-container").each(function(i,onj){
            var cancel = $(this).find('.filterable[data-filter="docstatus,=,2"]').length > 0;
            if (cancel) {
                $(this).css('background-color', '#FD8B8B');
            }
        })
        listview.refresh();
         
    },
};