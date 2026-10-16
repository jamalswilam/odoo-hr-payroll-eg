from datetime import date

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger

from ..models.hr_employee import parse_national_id


@tagged("post_install", "-at_install")
class TestNationalId(TransactionCase):
    def test_parse_valid_id(self):
        self.assertEqual(parse_national_id("29001011234567"), (date(1990, 1, 1), "female"))
        self.assertEqual(parse_national_id("30105150101153"), (date(2001, 5, 15), "male"))

    def test_parse_invalid_ids(self):
        for value in ("", "123", "2900101123456X", "19001011234567", "29013011234567"):
            with self.assertRaises(ValueError, msg=value):
                parse_national_id(value)

    def test_constraint_rejects_invalid_id(self):
        with self.assertRaises(ValidationError):
            self.env["hr.employee"].create({"name": "Bad ID", "eg_national_id": "12345678901234"})

    @mute_logger("odoo.sql_db")
    def test_unique_per_company(self):
        self.env["hr.employee"].create({"name": "A", "eg_national_id": "29001011234567"})
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            self.env["hr.employee"].create({"name": "B", "eg_national_id": "29001011234567"})

    def test_negative_insured_salary(self):
        with self.assertRaises(ValidationError):
            self.env["hr.employee"].create({"name": "C", "eg_insured_salary": -1})

    def test_onchange_fills_birthday_and_gender(self):
        form = Form(self.env["hr.employee"])
        form.name = "D"
        form.eg_national_id = "30105150101153"
        self.assertEqual(form.birthday, date(2001, 5, 15))
        self.assertEqual(form.gender, "male")
