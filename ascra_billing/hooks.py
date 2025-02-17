app_name = "ascra_billing"
app_title = "Ascra Billing"
app_publisher = "alokshukla994@gmail.com"
app_description = "Custom App For AscraTech Billing"
app_email = "alokshukla994@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ascra_billing/css/ascra_billing.css"
# app_include_js = "/assets/ascra_billing/js/ascra_billing.js"

# include js, css files in header of web template
# web_include_css = "/assets/ascra_billing/css/ascra_billing.css"
# web_include_js = "/assets/ascra_billing/js/ascra_billing.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ascra_billing/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "Delivery Note": "public/js/delivery_note.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "User": "public/js/user.js"
}
doctype_list_js = {"Sales Invoice" : "public/js/sales_invoice_list.js",
                   "Purchase Invoice" : "public/js/purchase_invoice_list.js"}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ascra_billing/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ascra_billing.utils.jinja_methods",
# 	"filters": "ascra_billing.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ascra_billing.install.before_install"
# after_install = "ascra_billing.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ascra_billing.uninstall.before_uninstall"
# after_uninstall = "ascra_billing.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ascra_billing.utils.before_app_install"
# after_app_install = "ascra_billing.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ascra_billing.utils.before_app_uninstall"
# after_app_uninstall = "ascra_billing.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ascra_billing.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways
# permission_query_conditions = {
#     "Sales Issue Voucher": "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_permission_query_conditions",
#     "Sales Receipt Voucher": "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_permission_query_conditions"
# }
# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

permission_query_conditions = {
    "Sales Issue Voucher": "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_permission_query_conditions",
    "Sales Receipt Voucher": "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.get_permission_query_conditions"
}

# has_permission = {
#     "Sales Issue Voucher": "ascra_billing.ascra_billing.doctype.sales_issue_voucher.sales_issue_voucher.has_permission"
# }

# DocType Class
# ---------------
# Override standard doctype classes



# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Invoice": {
        "validate": "ascra_billing.ascra_billing.doc_events.sales_invoice.before_save",
        "before_save": "ascra_billing.ascra_billing.doc_events.sales_invoice.validate_account_block_status"
    },
    "Purchase Invoice": {
        "validate": "ascra_billing.ascra_billing.doc_events.purchase_invoice.validate_account_block_status",
        "before_save": "ascra_billing.ascra_billing.doc_events.purchase_invoice.before_save"
    },
    "Shipment": {
        "on_submit": "ascra_billing.ascra_billing.doc_events.shipment.send_sms_after_submit"
    },
    "Expense Claim": {
        "before_save": "ascra_billing.ascra_billing.doc_events.expense_claim.before_save"
    },
    # "Delivery Note": {
    #   "before_save": "ascra_billing.ascra_billing.doc_events.delivery_note.before_save"
    # }
    "Customer": {
      "before_save": "ascra_billing.ascra_billing.doc_events.customer.before_save"
    },
    "Supplier": {
      "before_save": "ascra_billing.ascra_billing.doc_events.supplier.before_save"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"ascra_billing.tasks.all"
	# ],
	#"daily": [
	#	"ascra_billing.ascra_billing.doc_events.cron_mark_attendance.cron_mark_attendance_today_date"
	#],
	# "hourly": [
	# 	"ascra_billing.tasks.hourly"
	# ],
	# "weekly": [
	# 	"ascra_billing.tasks.weekly"
	# ],
	# "monthly": [
	# 	"ascra_billing.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "ascra_billing.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "erpnext.accounts.doctype.sales_invoice.sales_invoice.make_delivery_note": "ascra_billing.ascra_billing.doc_events.sales_invoice.make_delivery_note"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ascra_billing.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ascra_billing.utils.before_request"]
# after_request = ["ascra_billing.utils.after_request"]

# Job Events
# ----------
# before_job = ["ascra_billing.utils.before_job"]
# after_job = ["ascra_billing.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ascra_billing.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"doctype": "Expense Claim", "filters": [["name", "in", ["MakingCharges"]]]},
    "Custom Field",
    "Workspace",
    "Client Script",
    "Server Script",
    "Custom DocPerm",
    # {"doctype": "Property Setter", "filters": [["module", "in", ["Ascra Billing"]]]},
    {"doctype": "Item", "filters": [["name", "in", ["MakingCharges"]]]},
    {"doctype": "GST HSN Code", "filters": [["name", "in", ["12345678"]]]},
]
