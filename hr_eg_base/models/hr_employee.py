from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# Egyptian national ID (14 digits):
#   C YYMMDD GG SSSS K
#   C    century: 2 = 1900s, 3 = 2000s
#   GG   governorate code
#   SSSS sequence; its last digit is odd for males, even for females
#   K    check digit
CENTURY = {"2": 1900, "3": 2000}


def parse_national_id(value):
    """Return (birthday, gender) for a valid Egyptian national ID, else raise ValueError."""
    if not value or len(value) != 14 or not value.isdigit():
        raise ValueError("National ID must be exactly 14 digits.")
    if value[0] not in CENTURY:
        raise ValueError("National ID must start with 2 or 3.")
    year = CENTURY[value[0]] + int(value[1:3])
    birthday = date(year, int(value[3:5]), int(value[5:7]))  # raises ValueError on a bad date
    if birthday > date.today():
        raise ValueError("National ID birth date is in the future.")
    gender = "male" if int(value[12]) % 2 else "female"
    return birthday, gender


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    eg_national_id = fields.Char(
        string="National ID", size=14, groups="hr.group_hr_user", tracking=True, copy=False
    )
    eg_social_insurance_no = fields.Char(
        string="Social Insurance No.", groups="hr.group_hr_user", copy=False
    )
    eg_insurance_start_date = fields.Date(string="Insurance Start Date", groups="hr.group_hr_user")
    eg_currency_id = fields.Many2one(related="company_id.currency_id", string="Company Currency")
    eg_insured_salary = fields.Monetary(
        string="Insured Salary", currency_field="eg_currency_id", groups="hr.group_hr_user"
    )

    _sql_constraints = [
        (
            "eg_national_id_company_uniq",
            "unique(eg_national_id, company_id)",
            "This national ID is already used by another employee in this company.",
        ),
    ]

    @api.constrains("eg_national_id")
    def _check_eg_national_id(self):
        for employee in self:
            if not employee.eg_national_id:
                continue
            try:
                parse_national_id(employee.eg_national_id)
            except ValueError as err:
                raise ValidationError(_("Invalid national ID for %(name)s: %(error)s",
                                        name=employee.name, error=err)) from err

    @api.constrains("eg_insured_salary")
    def _check_eg_insured_salary(self):
        if any(employee.eg_insured_salary < 0 for employee in self):
            raise ValidationError(_("Insured salary cannot be negative."))

    @api.onchange("eg_national_id")
    def _onchange_eg_national_id(self):
        """Fill birthday and gender from the national ID when they are empty."""
        try:
            birthday, gender = parse_national_id(self.eg_national_id)
        except ValueError:
            return
        if not self.birthday:
            self.birthday = birthday
        if not self.gender:
            self.gender = gender
