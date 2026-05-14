# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
<<<<<<< HEAD
<<<<<<< HEAD
from frappe.utils import flt, get_link_to_form
from frappe.utils.formatters import format_value
from frappe.utils.jinja import render_template
<<<<<<< HEAD
=======
from frappe.utils import flt
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
from frappe.utils import flt, get_link_to_form
>>>>>>> 687b2617 (feat: validate filters and ctc)
=======
>>>>>>> f992583c (feat: CTC summary card)

from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip


class SalaryBreakupReport:
	def __init__(self, employee, salary_structure_assignment):
		self.employee = employee
<<<<<<< HEAD
<<<<<<< HEAD
		self.salary_structure_assignment = salary_structure_assignment

		self.salary_structure, self.currency, self.assignment_date, self.income_tax_slab, self.ctc = (
			frappe.get_value(
				"Salary Structure Assignment",
				{"name": salary_structure_assignment, "employee": employee},
				["salary_structure", "currency", "from_date", "income_tax_slab", "ctc"],
			)
=======
		self.ctc = frappe.db.get_value("Employee", employee, "ctc")
		self.validate_ctc()

<<<<<<< HEAD
		self.salary_structure, self.currency = frappe.get_value(
			"Salary Structure Assignment", salary_structure_assignment, ["salary_structure", "currency"]
>>>>>>> 687b2617 (feat: validate filters and ctc)
=======
		self.salary_structure, self.currency, self.assignment_date, self.income_tax_slab = frappe.get_value(
			"Salary Structure Assignment",
			salary_structure_assignment,
			["salary_structure", "currency", "from_date", "income_tax_slab"],
>>>>>>> f992583c (feat: CTC summary card)
		)
		self.validate_ctc()
		self.salary_slip = make_salary_slip(
			self.salary_structure,
			employee=self.employee,
			for_preview=1,
			as_print=False,
			posting_date=frappe.flags.posting_date if frappe.flags.in_test else None,
		)
		self.net_pay = self.salary_slip.net_pay
		self.gross_pay = self.salary_slip.gross_pay
		self.payroll_frequency = self.salary_slip.payroll_frequency
		self.cycle_multiplier = {
			"Monthly": 12,
			"Fortnightly": 24,
			"Bimonthly": 6,
			"Weekly": 52,
			"Daily": 365,
		}.get(self.payroll_frequency)
=======
		self.ctc = frappe.db.get_value("Employee", employee, "ctc")
		self.salary_structure, self.currency = frappe.get_value(
			"Salary Structure Assignment", salary_structure_assignment, ["salary_structure", "currency"]
		)
		self.salary_slip = make_salary_slip(
			self.salary_structure, employee=self.employee, for_preview=1, as_print=False
		)
		self.net_pay = self.salary_slip.net_pay
		self.gross_pay = self.salary_slip.gross_pay
<<<<<<< HEAD

>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
		self.payroll_frequency = self.salary_slip.payroll_frequency
		self.cycle_multiplier = {
			"Monthly": 12,
			"Fortnightly": 24,
			"Bimonthly": 6,
			"Weekly": 52,
			"Daily": 365,
		}.get(self.payroll_frequency)
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
		self.salary_components = []
		self.earning_components = []
		self.deduction_components = []
		self.tax_components = []
		self.total_net_earnings = []
		self.total_gross_earnings = []

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 687b2617 (feat: validate filters and ctc)
	def validate_ctc(self):
		if not self.ctc:
			frappe.throw(
				_("Please set cost to company(CTC) for employee {0} in the {1}").format(
					frappe.bold(self.employee),
<<<<<<< HEAD
					get_link_to_form(
						"Salary Structure Assignment",
						self.salary_structure_assignment,
						"Salary Structure Assignment",
					),
=======
					get_link_to_form("Employee", self.employee + "#salary_information", "employee master."),
>>>>>>> 687b2617 (feat: validate filters and ctc)
				),
				title=_("CTC Missing for Employee"),
			)

<<<<<<< HEAD
=======
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
>>>>>>> 687b2617 (feat: validate filters and ctc)
	def get_data(self):
		self.set_salary_component_details()
		self.calculate_yearly_amounts_and_percent_of_ctc()
		self.indent_salary_components()
		self.separate_salary_components_by_type()
		self.set_type_and_formula()
		self.set_totals_row_for_component_types()
		self.set_net_and_gross_earning_rows()

		return (
			self.earning_components
			+ self.deduction_components
			+ self.tax_components
			+ self.total_net_earnings
			+ self.total_gross_earnings
		)

	def set_salary_component_details(self):
		salary_component_details = frappe.db.get_all(
			"Salary Detail",
			filters={"parent": self.salary_structure},
			fields=["salary_component", "amount_based_on_formula", "formula"],
		)

		self.salary_components = [
			{
				"salary_component": component.salary_component,
<<<<<<< HEAD
<<<<<<< HEAD
				"per_cycle": component.amount,
=======
				"monthly": component.amount,
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"per_cycle": component.amount,
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
				"abbr": component.abbr,
				"is_tax_component": component.variable_based_on_taxable_salary,
				"component_type": component.parentfield,
			}
			for component in self.salary_slip.earnings + self.salary_slip.deductions
		]

		for component in self.salary_components:
			component_details = next(
				(
					detail
					for detail in salary_component_details
					if component.get("salary_component") == detail.salary_component
				),
				{},
			)
			component.update(component_details)

	def calculate_yearly_amounts_and_percent_of_ctc(self):
		for component in self.salary_components:
<<<<<<< HEAD
<<<<<<< HEAD
			annual_amount = component.get("per_cycle", 0) * self.cycle_multiplier
=======
			annual_amount = component.get("monthly", 0) * 12
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
			annual_amount = component.get("per_cycle", 0) * self.cycle_multiplier
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
			component.update(
				{
					"annual": flt(annual_amount, 2),
					"percent_of_ctc": self.calculate_percent_of_ctc(annual_amount),
				}
			)

	def separate_salary_components_by_type(self):
		self.earning_components = [
			component for component in self.salary_components if component.get("component_type") == "earnings"
		]
		self.deduction_components = [
			component
			for component in self.salary_components
			if component.get("component_type") == "deductions" and not component.get("is_tax_component")
		]
		self.tax_components = [
			component for component in self.salary_components if component.get("is_tax_component")
		]

	def set_type_and_formula(self):
		for component in self.earning_components + self.deduction_components:
			component["type"] = "Formula" if component.get("amount_based_on_formula") else "Fixed"
			component["formula"] = (
				component.get("formula") or "-"
				if component.get("amount_based_on_formula")
<<<<<<< HEAD
<<<<<<< HEAD
				else component.get("per_cycle") or "-"
=======
				else component.get("monthly") or "-"
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				else component.get("per_cycle") or "-"
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
			)

	def set_totals_row_for_component_types(self):
		def calculate_total(period, components):
			total = 0
			for component in components:
				total += component.get(period)
			return total

		def set_totals_row(component_type):
			components = {
				"Earnings": self.earning_components,
				"Deductions": self.deduction_components,
				"Tax Deductions": self.tax_components,
			}.get(component_type)
			totals_row = {
				"salary_component": component_type,
				"type": "",
				"formula": "",
				"bold": True,
<<<<<<< HEAD
<<<<<<< HEAD
				"per_cycle": calculate_total("per_cycle", components),
=======
				"monthly": calculate_total("monthly", components),
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"per_cycle": calculate_total("per_cycle", components),
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
				"annual": calculate_total("annual", components),
				"percent_of_ctc": self.calculate_percent_of_ctc(calculate_total("annual", components)),
			}
			components.insert(0, totals_row)

		for component_type in ("Earnings", "Deductions", "Tax Deductions"):
			set_totals_row(component_type)

	def set_net_and_gross_earning_rows(self):
		self.total_net_earnings = [
			{
				"salary_component": "Total Net Earnings",
				"type": "",
				"formula": "",
<<<<<<< HEAD
<<<<<<< HEAD
				"per_cycle": self.net_pay,
				"annual": self.net_pay * self.cycle_multiplier,
				"percent_of_ctc": self.calculate_percent_of_ctc(self.net_pay * self.cycle_multiplier),
=======
				"monthly": self.net_pay,
				"annual": self.net_pay * 12,
				"percent_of_ctc": self.calculate_percent_of_ctc(self.net_pay),
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"per_cycle": self.net_pay,
				"annual": self.net_pay * self.cycle_multiplier,
				"percent_of_ctc": self.calculate_percent_of_ctc(self.net_pay * self.cycle_multiplier),
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
				"bold": True,
			}
		]
		self.total_gross_earnings = [
			{
				"salary_component": "Total Gross Earnings",
				"type": "",
				"formula": "",
<<<<<<< HEAD
<<<<<<< HEAD
				"per_cycle": self.gross_pay,
				"annual": self.gross_pay * self.cycle_multiplier,
				"percent_of_ctc": self.calculate_percent_of_ctc(self.gross_pay * self.cycle_multiplier),
=======
				"monthly": self.gross_pay,
				"annual": self.gross_pay * 12,
				"percent_of_ctc": self.calculate_percent_of_ctc(self.gross_pay),
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"per_cycle": self.gross_pay,
				"annual": self.gross_pay * self.cycle_multiplier,
				"percent_of_ctc": self.calculate_percent_of_ctc(self.gross_pay * self.cycle_multiplier),
>>>>>>> 93076125 (feat: support for all available payroll frequencies)
				"bold": True,
			}
		]

	def calculate_percent_of_ctc(self, amount):
		return flt(amount * 100 / self.ctc, 2)

<<<<<<< HEAD
	def get_per_cycle_ctc(self):
		return flt(self.ctc / self.cycle_multiplier, 2)

=======
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
	def indent_salary_components(self):
		for component in self.salary_components:
			component["indent"] = 1

<<<<<<< HEAD
<<<<<<< HEAD
	def format_currency(self, amount):
		return format_value(amount, currency=self.currency)
=======
=======
	def format_currency(self, amount):
		return format_value(amount, currency=self.currency)

>>>>>>> f992583c (feat: CTC summary card)
	def get_summary(self):
		per_cycle_ctc = flt(self.ctc / self.cycle_multiplier, 2)
		return [
			{"value": self.ctc, "label": _("Annual CTC"), "datatype": "Currency", "currency": self.currency},
			{
				"value": per_cycle_ctc,
				"label": _(f"{self.payroll_frequency} CTC"),
				"datatype": "Currency",
				"currency": self.currency,
			},
			{
				"value": self.gross_pay,
				"label": _(f"{self.payroll_frequency} Gross Pay"),
				"datatype": "Currency",
				"currency": self.currency,
			},
			{
				"value": self.net_pay,
				"label": _(f"{self.payroll_frequency} Net Pay"),
				"datatype": "Currency",
				"currency": self.currency,
			},
		]
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)

	def get_columns(self) -> list[dict]:
		"""Return columns for the report.

		One field definition per column, just like a DocType field definition.
		"""
		return [
			{
				"label": _("Component"),
				"fieldname": "salary_component",
				"fieldtype": "Data",
				"width": 300,
<<<<<<< HEAD
<<<<<<< HEAD
				"fixed": 1,
=======
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"fixed": 1,
>>>>>>> f992583c (feat: CTC summary card)
			},
			{
				"label": _("Type"),
				"fieldname": "type",
				"fieldtype": "Data",
<<<<<<< HEAD
<<<<<<< HEAD
				"width": 150,
				"fixed": 1,
=======
				"width": 200,
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"width": 150,
				"fixed": 1,
>>>>>>> f992583c (feat: CTC summary card)
			},
			{
				"label": _("Formula/Amount"),
				"fieldname": "formula",
				"fieldtype": "Data",
<<<<<<< HEAD
<<<<<<< HEAD
				"width": 250,
				"fixed": 1,
			},
			{
				"label": _(self.payroll_frequency),
				"fieldname": "per_cycle",
				"fieldtype": "Currency",
				"width": 250,
				"options": "currency",
				"fixed": 1,
=======
				"width": 200,
=======
				"width": 250,
				"fixed": 1,
>>>>>>> f992583c (feat: CTC summary card)
			},
			{
				"label": _(self.payroll_frequency),
				"fieldname": "per_cycle",
				"fieldtype": "Currency",
				"width": 250,
				"options": "currency",
<<<<<<< HEAD
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"fixed": 1,
>>>>>>> f992583c (feat: CTC summary card)
			},
			{
				"label": _("Annual"),
				"fieldname": "annual",
				"fieldtype": "Currency",
<<<<<<< HEAD
<<<<<<< HEAD
				"width": 250,
				"options": "currency",
				"fixed": 1,
=======
				"width": 200,
				"options": "currency",
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"width": 250,
				"options": "currency",
				"fixed": 1,
>>>>>>> f992583c (feat: CTC summary card)
			},
			{
				"label": _("Percent of CTC (%)"),
				"fieldname": "percent_of_ctc",
				"fieldtype": "Percent",
				"width": 200,
<<<<<<< HEAD
<<<<<<< HEAD
				"fixed": 1,
=======
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
				"fixed": 1,
>>>>>>> f992583c (feat: CTC summary card)
			},
			{
				"fieldname": "currency",
				"label": _("Currency"),
				"fieldtype": "Link",
				"options": "Currency",
				"hidden": 1,
				"value": self.currency,
			},
		]

<<<<<<< HEAD
<<<<<<< HEAD
	def get_message(self):
		path = "hrms/payroll/report/employee_ctc_break_up/employee_profile_card.html"
		context = dict(
			{
				"employee_name": frappe.get_value("Employee", self.employee, "employee_name"),
				"designation": frappe.get_value("Employee", self.employee, "designation"),
				"salary_structure": self.salary_structure,
				"per_cycle": self.payroll_frequency,
				"annual_ctc": self.format_currency(self.ctc),
				"per_cycle_ctc": self.format_currency(self.get_per_cycle_ctc()),
=======
	def get_message(self):
		path = "hrms/payroll/report/employee_ctc_break_up/employee_profile_card.html"
		context = frappe.get_doc("Employee", self.employee).as_dict()
		context.update(
			{
				"salary_structure": self.salary_structure,
				"per_cycle": self.payroll_frequency,
				"annual_ctc": self.format_currency(self.ctc),
				"per_cycle_ctc": self.format_currency(flt(self.ctc / self.cycle_multiplier, 2)),
>>>>>>> f992583c (feat: CTC summary card)
				"per_cycle_gross_pay": self.format_currency(self.gross_pay),
				"per_cycle_net_pay": self.format_currency(self.net_pay),
				"assignment_date": frappe.utils.global_date_format(self.assignment_date, "long"),
				"income_tax_slab": self.income_tax_slab,
			}
		)
<<<<<<< HEAD
		# nosemgrep: frappe-semgrep-rules.rules.security.frappe-ssti
		employee_profile_card = render_template(path, context=context, is_path=True)
		return employee_profile_card

=======
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
		employee_profile_card = render_template(path, context=context, is_path=True)
		return employee_profile_card

>>>>>>> f992583c (feat: CTC summary card)

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
<<<<<<< HEAD
<<<<<<< HEAD
	employee = filters.get("employee")
	salary_structure_assignment = filters.get("salary_structure_assignment")

	missing_filter = (
		"Employee"
		if not employee
		else "Salary Structure Assignment"
		if not salary_structure_assignment
		else None
	)
	if missing_filter:
		frappe.throw(
			_("Please set {0} to get CTC report").format(frappe.bold(missing_filter)),
			title=_("Missing value for filters"),
		)

	salary_breakup_report = SalaryBreakupReport(employee, salary_structure_assignment)

	data = salary_breakup_report.get_data()
	columns = salary_breakup_report.get_columns()
	message = salary_breakup_report.get_message()
	return columns, data, message, None, None
=======

	salary_structure_assignment = filters.get("salary_structure_assignment")
=======
>>>>>>> 687b2617 (feat: validate filters and ctc)
	employee = filters.get("employee")
	salary_structure_assignment = filters.get("salary_structure_assignment")

	missing_filter = (
		"Employee"
		if not employee
		else "Salary Structure Assignment"
		if not salary_structure_assignment
		else None
	)
	if missing_filter:
		frappe.throw(
			_("Please set {0} to get CTC report").format(frappe.bold(missing_filter)),
			title=_("Missing value for filters"),
		)

	salary_breakup_report = SalaryBreakupReport(employee, salary_structure_assignment)

	data = salary_breakup_report.get_data()
	columns = salary_breakup_report.get_columns()
<<<<<<< HEAD

	return columns, data, None, None, summary
>>>>>>> 211d83aa (feat: Employee CTC Breakup report)
=======
	message = salary_breakup_report.get_message()
	return columns, data, message, None, None
>>>>>>> f992583c (feat: CTC summary card)
