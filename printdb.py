import sys
import os
import persistence


def main():
    # should do the find methods.
    repo = persistence.repo
    # todo order by
    print("Activities")
    print_a_list(repo.activities.get_table())

    print("Coffee stands")
    print_a_list(repo.coffee_stands.get_table())

    print("Employees")
    print_a_list(repo.employees.get_table())

    print("Products")
    print_a_list(repo.products.get_table())

    print("Suppliers")
    print_a_list(repo.suppliers.get_table())
    print("\nEmployees report")
    for employee_report in repo.get_employees_report():
        print("{} {} {} {}".format(employee_report.name, employee_report.salary, employee_report.location,
                                   employee_report.sales))

    activityReport = repo.get_activity_report()
    if (len(activityReport) != 0):
        print("\nActivities")
        print_a_list(repo.get_activity_report())


def print_a_list(list_to_print):
    for item in list_to_print:
        print(item)


if __name__ == '__main__':
    main()
