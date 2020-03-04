# file: action.py
import sys

import persistence
import printdb


def main(args):
    repo = persistence.repo
    inputfilename = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            arguments = line.split(',')
            if len(arguments) == 4:
                add_sale([int(arguments[0].strip()), int(arguments[1].strip()), int(arguments[2].strip()), int(arguments[3].strip())])
    printdb.main()


def add_sale(list):
    # by date???
    product = persistence.repo.products.get_product(list[0])
    # print(list)

    if product.quantity+int(list[1]) >= 0:
        product.quantity = product.quantity + list[1]
        persistence.repo.products.update_quantity(product.id, product.quantity)
        # persistence.Products.add_action(persistence.Activities(list))
        activity = persistence.Activities(*list)
        persistence.repo.activities.add_activity(activity)


if __name__ == '__main__':
    main(sys.argv)
