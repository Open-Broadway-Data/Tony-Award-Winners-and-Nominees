from scrape_wikipedia import utils
import bs4


# Add assert type method in a bit
def get_data_from_table_alt(table:bs4.element.Tag):
    """
    returns a structured table for a beautiful soup table
    """
    new_table = table_to_2d(table)

    # Now, need to iterate through this table and parse values.
    return


def table_to_2d(table):
    """Convert a table into a 2d matrix"""
    rows = table("tr")
    cols = rows[0](["td", "th"])
    table = [[None] * len(cols) for _ in range(len(rows))]
    for row_i, row in enumerate(rows):
        for col_i, col in enumerate(row(["td", "th"])):
            insert_into_table(table, row_i, col_i, col)
    return table


def insert_into_table(table, row, col, element):
    """Insert values from a table into a 2d matrix"""
    if row >= len(table) or col >= len(table[row]):
        return
    if table[row][col] is None:
        # value = element.get_text().strip()
        value = element
        table[row][col] = value
        if element.has_attr("colspan"):
            span = int(element["colspan"])
            for i in range(1, span):
                table[row][col+i] = value
        if element.has_attr("rowspan"):
            span = int(element["rowspan"])
            for i in range(1, span):
                table[row+i][col] = value
    else:
        insert(table, row, col + 1, element)
