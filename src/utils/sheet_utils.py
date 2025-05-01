def get_category(particular,category_map):
    '''

    :param particular: spend entry in the particulars column on the balance sheet
    :param category_map: mapping of spend particulars with a category
        for eg: "market", "cart" falls under the category "Shopping"
    :return:
    '''
    category_class = "Unknown"
    for category in category_map["categories"]:
        presence = False
        for cat_string in category_map["categories"][category]:
            if cat_string in particular.lower():
                category_class = category
                presence = True
                break

        if presence:
            break

    return category_class.capitalize()