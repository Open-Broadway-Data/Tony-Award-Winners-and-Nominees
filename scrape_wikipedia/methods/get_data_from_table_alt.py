from scrape_wikipedia import utils
import bs4


# Add assert type method in a bit
def get_data_from_table_alt(table:bs4.element.Tag):
    """
    returns a structured table for a beautiful soup table
    """
    new_table = table_to_2d(table, add_row_style_as_value=True)


    # Now, need to iterate through this table and parse values.
    col_names = [utils.get_text_from_tag(x).lower() for x in new_table.pop(0)]
    style_idx = col_names.index('style')

    # Instantiate a blank list
    records = []

    for row_idx, row in enumerate(new_table):

        # If all the values are equal, skip...
        if len(set(row)) <= 2:
            continue

        if col_names[0].lower()!='year':
            # we are only interested in tables which correspond with tony awards
            continue

        # If this is a null row, this is how you'll know..
        if not  row[0].select_one('a'):
            continue
        year = utils.get_number_from_str(row[0].text[:4])
        season = row[0].select_one('a').text
        season_link = row[0].select_one('a[href]')
        if season_link:
            season_link = season_link.get('href')

        # Are you a winner?
        if row[style_idx] and 'background:#B0C4DE' in row[style_idx]:
            winner = True
        else:
            winner = False

        rec = dict(
    		year=year,
    		season=season,
    		season_link=season_link,
            winner=winner,
        )

        # additional_data
        additional_data={}

        # Go through each of the cells and add the value
        for i, cell in enumerate(row[1:]):

            my_col = col_names[i+1]

            # If there's no value or style col
            if not cell or my_col=='style':
                continue

            # Otherwise
            additional_data[my_col] = cell.get_text(strip=True)
            # if there's a link, save it
            if cell.select_one('a[href]'):
                additional_data[my_col + '_link'] = 'https://en.wikipedia.org' + cell.select_one('a[href]').get('href')

        # Only store values when you have em'
        if additional_data:
            rec = {**rec, **additional_data}

            # Save your record
            records.append(rec)



    return records


def table_to_2d(table, add_row_style_as_value=True):
    """Convert a table into a 2d matrix"""
    rows = table("tr")
    if add_row_style_as_value:
        row_styles = [row.get('style') for i, row in enumerate(rows)]
        row_styles[0] = 'style'

    cols = rows[0](["td", "th"])
    table = [[None] * len(cols) for _ in range(len(rows))]
    for row_i, row in enumerate(rows):
        for col_i, col in enumerate(row(["td", "th"])):
            insert_into_table(table, row_i, col_i, col)

    # now add the style if we want them...
    # There's def a better way to do this....
    if row_styles:
        table = [row + [row_styles[i]] for i,row in enumerate(table)]
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
                # allow for incorrect colspans which "overspan" a table's width
                if col+i >= len(table[row]):
                    continue
                table[row][col+i] = value
        if element.has_attr("rowspan"):
            span = int(element["rowspan"])
            for i in range(1, span):
                # allow for incorrect rowspans which "overspan" a table's length
                # if row+1 >=len(table[col]):
                    # return
                # print(
                #     f'row={row+i}, n_rows={len(table)}, '
                #     f'col={col}, n_cols={len(table[row])}'
                #     )
                # This row is attempting to overwrite a row which doesn't exist
                if row+i>=len(table):
                    continue
                # print(table[row+1])
                table[row+i][col] = value
    else:
        insert_into_table(table, row, col + 1, element)
