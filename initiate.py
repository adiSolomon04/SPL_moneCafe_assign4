# file: initiate.py
import sys
import persistence
import os


def main(args):
    if os.path.isfile('moncafe.db'):
        os.remove('moncafe.db')
    repo = persistence.repo
    repo.__init__()
    repo.create_tables()
    inputfilename = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            arguments = line.split(',')
            if arguments[0] == 'E':
                repo.employees.insert(persistence.Employees(int(arguments[1].strip()),
                                                            arguments[2].strip(),
                                                            arguments[3].strip(),
                                                            int(arguments[4].strip())))
            elif arguments[0] == 'S':
                repo.suppliers.insert(persistence.Suppliers(int(arguments[1].strip()),
                                                            arguments[2].strip(),
                                                            arguments[3].strip()))

            elif arguments[0] == 'P':
                repo.products.insert(persistence.Products(int(arguments[1].strip()),
                                                          arguments[2].strip(),
                                                          arguments[3].strip(), 0))
            elif arguments[0] == 'C':
                repo.coffee_stands.insert(persistence.Coffee_stands(int(arguments[1].strip()),
                                                                    arguments[2].strip(),
                                                                    int(arguments[3].strip())))


if __name__ == '__main__':
    main(sys.argv)
