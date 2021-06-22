import unittest
import unittest.mock
from unittest.mock import patch
import app


class TestEmployee(unittest.TestCase):
    def test_employee_setEmployees(self):
        manager = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': 2,
                'salary': 130000
            })
        employee = app.Employee({
                'id': 2,
                'first_name': 'brian',
                'manager': 1,
                'salary': 130000
            })
        manager.setEmployees([employee])
        self.assertIn(employee, manager.employees, "Should contain the employee")

    def test_employee_isOwner(self):
        employee = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': None,
                'salary': 130000
            })
        employee2 = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': 1,
                'salary': 130000
            })
        self.assertTrue(employee.isOwner(), "Employee should be an owner")
        self.assertFalse(employee2.isOwner(), "Employee should not be an owner")

    def test_employee_isManager(self):
        manager = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': 2,
                'salary': 130000
            })
        employee = app.Employee({
                'id': 2,
                'first_name': 'brian',
                'manager': 1,
                'salary': 130000
            })
        manager.setEmployees([employee])
        self.assertTrue(manager.isManager(), "Should be a manager")
        self.assertFalse(employee.isManager(), "Should not be a manager")

    def test_employee_reportsToId(self):
        employee = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': 2,
                'salary': 130000
            })
        self.assertTrue(employee.reportsToId(2), "Should report to the id")
        self.assertFalse(employee.reportsToId(1), "Should not report to the id")

class TestStaff(unittest.TestCase):
    def test_staff_totalSalary(self):
        employee = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': None,
                'salary': 130000
            })
        employee2 = app.Employee({
                'id': 2,
                'first_name': 'jacob',
                'manager': 1,
                'salary': 130000
            })
        staff = app.Staff([employee, employee2])
        self.assertEqual(staff.totalSalary(), 260000, "Should be 260000")

    def test_staff_hierarchy(self):
        employee = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': None,
                'salary': 130000
            })
        employee2 = app.Employee({
                'id': 2,
                'first_name': 'jacob',
                'manager': 1,
                'salary': 130000
            })
        employee3 = app.Employee({
                'id': 2,
                'first_name': 'a',
                'manager': 1,
                'salary': 130000
            })
        staff = app.Staff([employee, employee2, employee3])
        self.assertIn(employee,staff.hierarchy, "Top level of hierarchy should contain employee")
        self.assertIn(employee2, staff.hierarchy[0].employees, "Second level of hierarchy should contain employee2")
        self.assertEqual(employee3, staff.hierarchy[0].employees[0], "employees of a staff member should be sorted alphabetically")

    def test_staff_string(self):
        employee = app.Employee({
                'id': 1,
                'first_name': 'jacob',
                'manager': None,
                'salary': 130000
            })
        employee2 = app.Employee({
                'id': 2,
                'first_name': 'jacob',
                'manager': 1,
                'salary': 130000
            })
        employee3 = app.Employee({
                'id': 3,
                'first_name': 'a',
                'manager': 1,
                'salary': 130000
            })
        staff = app.Staff([employee, employee2, employee3])
        expectedString = "jacob\n  a\n  jacob\n"
        self.assertEqual(str(staff),expectedString)


if __name__ == '__main__':
    unittest.main()
