# odoo-hr-payroll-eg

Egyptian HR and payroll localization for **Odoo 17 Community**, built as small, installable modules.
توطين الموارد البشرية والرواتب لمصر على أودو 17، على شكل موديولات صغيرة قابلة للتثبيت.

## Why

Egyptian companies on Odoo keep national IDs, social insurance numbers and insured salaries in spreadsheets or free-text fields. That breaks reporting, duplicates employees and causes insurance filing errors. This repo puts that data in the employee record, validated at entry.

## Modules

| Module | Status | What it does |
|---|---|---|
| [`hr_eg_base`](hr_eg_base) | ✅ v17.0.1.0.0 | National ID validation (14 digits, century, birth date), auto-fill birthday and gender, unique ID per company, social insurance number, insurance start date, insured salary. Fields restricted to HR officers. |
| `hr_eg_social_insurance` | 🔜 planned | Employee and employer insurance contributions, monthly insurance report |
| `hr_eg_payroll_tax` | 🔜 planned | Salary tax brackets and personal exemption, configurable per fiscal year |

Tax and insurance rates change by law. Planned modules will keep rates in configuration, never hard-coded.

## Install

```bash
git clone https://github.com/jamalswilam/odoo-hr-payroll-eg.git
# add the clone to addons_path, restart Odoo, then:
odoo -d <db> -i hr_eg_base --stop-after-init
```

Depends only on `hr` (Community). Works with the dev environment in [`kit-odoo-docker`](https://github.com/jamalswilam/kit-odoo-docker).

## Tests

```bash
odoo -d test_db -i hr_eg_base --test-enable --test-tags /hr_eg_base --stop-after-init
```

## License

LGPL-3.0. See [LICENSE](LICENSE).

---
Built by [Jamal Swilam](https://github.com/jamalswilam) · [I Solutions Technology](https://www.isolutions-technology.com)
