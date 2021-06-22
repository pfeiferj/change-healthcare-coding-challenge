from __future__ import annotations

import yaml
from functools import reduce
from jsonschema import validate
from typing import Any

class Employee:
    """
    A representation of an employee for a company.

    Attributes
    ----------
    id: int
        An id for the employee.
    first_name: str
        The first name of the employee.
    salary:
        The salary of the employee.
    manager:
        The id of the employee's manager.
    employees:
        A list of employees the this employee manages.

    Methods
    -------
    isOwner(): bool
        Checks the status of the employee to see whether they are an Owner/top
        level employee.
    isManager(): bool
        Checks the status of the employee to see whether they are a manager.
    reportsToId(id: int): bool
        Checks if the employee is managed by the given id.
    setEmployees(employees: list[Employee]): None
        Sets the list of employees that this employee manages.
    """

    def __init__(self, employee: dict[str, Any]):
        """
        Parameters
        ----------
        employee: dict[str, Any]
            A dictionary representation of the employee.
        """

        self.id: int = employee['id']
        self.first_name: str = employee['first_name']
        self.salary: int = employee['salary']
        self.manager: int = employee['manager']
        self.employees: list[Employee] = []

    def isOwner(self) -> bool:
        """
        Checks the status of the employee to see whether they are an Owner/top
        level employee.

        Returns
        -------
        bool
            True if the employee is an owner, false if not.

        """

        # If the employee does not have a manager they are the owner/top level
        # employee
        return self.manager == None

    def isManager(self) -> bool:
        """
        Checks the status of the employee to see whether they are a manager.

        Returns
        -------
        bool
            True if the employee is a manager, false if not.
        """

        # If the employee has their own employees they are a manager.
        return len(self.employees) > 0

    def reportsToId(self, id: int) -> bool:
        """
        Checks if the employee is managed by the given id.

        Parameters
        ----------
        id: int
            An id to check if this employee is managed by.

        Returns
        -------
        bool
            True if the employee is managed by the id, false if not.
        """

        # If the employees manager id matches the given id they are managed by
        # the given id.
        return self.manager == id

    def setEmployees(self, employees: list[Employee]):
        """
        Sets the list of employees that this employee manages in alphabetical
        order.

        Parameters
        ----------
        employees: list[Employee]
            A list of employees that this employee manages.
        """
        
        # sort the employees by first name
        employees.sort(key = lambda x: x.first_name)
        self.employees = employees

class Staff:
    """
    A representation of the employees in a company.

    Attributes
    ----------
    employees: list[Employee]
        A list of all of the employees on staff sorted by alphabetical order.
    hierarchy(): list[Employee]
        A hierarchy of staff with each manager's employees sorted by
        alphabetical order.
    
    Methods
    -------
    totalSalary: int
        Calculates a total of all of the staff members' salaries.
    """

    def __init__(self, employees: list[Employee]):
        """
        Parameters
        ----------
        employees: list[Employee]
            A list of the employees on staff.
        """

        # sort the employees by first name
        employees.sort(key = lambda x: x.first_name)

        self.employees = employees
        
        # Get the top owners/top level employees for generating the staff
        # hierarchy
        self.hierarchy = [x for x in self.employees if x.isOwner()];

        # Set all of the levels of the hierarchy
        self.__generateHierarchy(self.hierarchy)

    def __generateHierarchy(self, hierarchyLevel: list[Employee]):
        """
        Generates the staff hierarchy based off of a starting list of top level
        employees.

        Parameters
        ----------
        hierarchyLevel: list[Employee]
            The top level of employees to generate a hierarchy for.
        """
        for employee in hierarchyLevel:
            # Get all employees managed by this employee
            employees = [x for x in self.employees if x.reportsToId(employee.id)]

            if len(employees) > 0:
                # If we found employees set the employees under the current
                # employee
                employee.setEmployees(employees)

                # recurse through the next level of employees
                self.__generateHierarchy(employee.employees)



    def __generateHierarchyString(self, hierarchyLevel: list[Employee], depth: int = 0, tabWidth: int = 2) -> str:
        """
        Creates a string representation of the staff hierarchy.

        Parameters
        ----------
        hierarchyLevel: list[Employee]
            The current position in the hierarchy to generate a string for.
        depth: int
            The current depth in the hierarchy, defaults to 0.
        tabWidth: int
            How much to indent each level in the hierarchy, defaults to 2.

        Returns
        -------
        str
            The string representation of the hierarchy of staff.
        """

        # The string representing the hierarchy form the current level.
        hierarchyString = ''

        # The indentation of the current level in the hierarchy.
        prefix = ' ' * depth

        for employee in hierarchyLevel:
            # Add each employee in the level to the hierarchyString.
            hierarchyString += prefix + employee.first_name + '\n'

            if employee.isManager():
                # add the employees under the current employee to the
                # hierarchyString by recursing through them.
                hierarchyString += self.__generateHierarchyString(employee.employees, depth + tabWidth, tabWidth)


        # return the hierarchyString generated from the current hierarchyLevel.
        return hierarchyString


    def __repr__(self):
        """
        Generates a string representation of the staff in a hierarchy.

        Returns
        -------
        str
            The string representation of the staff.
        """

        return self.__generateHierarchyString(self.hierarchy)

    def totalSalary(self) -> int:
        """
        Calculates a total of all of the staff members' salaries.

        Returns
        -------
        int
            The total of the staff members' salaries.
        """

        # Get the salaries from all of the employees.
        salaries = map(lambda x: x.salary, self.employees)

        # Add the salaries together and return them.
        return reduce(lambda a, b: a + b, salaries)
        


def readEmployeeData():
    """
    Reads employee data from employees.yml.

    Returns
    -------
    list[dict[str,Any]]
        The employees as a list of dicts.
    """

    fEmployees = open('employees.yml')
    
    # Convert the yaml file to a list of dicts and return it.
    return yaml.safe_load(fEmployees);

def readEmployeeSchema():
    """
    Reads the employee json schema from employees-schema.yml.

    Returns
    -------
    dict
        The json schema representing the employee data as a dict.
    """

    fSchema = open('employees-schema.yml')

    # convert the yaml file into a dict and return it.
    return yaml.safe_load(fSchema)

def validateEmployeeData(data: list[dict[str, Any]]) -> list[Employee]:
    """
    Validates the employee data against a json schema and then returns the
    employees wrapped in the Employee class.

    Parameters
    ----------
    data: list[dict[str, Any]]
        The unvalidated employee data.

    Raises
    ------
    ValidationError
        An error indicating the employee data did not meet the json schema's
        requirements.

    Returns
    -------
    list[Employee]
        The employees wrapped in the Employee class.
    """

    # load the json schema
    schema = readEmployeeSchema()

    # validate the employee data against the employee json schema
    validate(data, schema)

    # Wrap the employees in the Employee class and return them.
    return [Employee(x) for x in data ]


def main():
    """
    The entry function of the application. Prints the hierarchy of staff and the
    total salary of the staff members.
    """

    # Read and validate the employee data
    employees = readEmployeeData()
    validatedEmployees = validateEmployeeData(employees)

    # Create a new instance of the Staff class representing the validated
    # employee data
    staff = Staff(validatedEmployees)

    # Print the staff hierarchy
    print(staff)
    # Print the total salary
    print("Total salary: " + str(staff.totalSalary()))
    



# Run the main function if this is being ran as the main script.
if __name__ == '__main__':
    main()
