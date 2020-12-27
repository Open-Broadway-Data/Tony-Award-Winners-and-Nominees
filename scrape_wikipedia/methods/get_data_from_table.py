from scrape_wikipedia import utils
import bs4

# Add assert type method in a bit
def get_data_from_table(table:bs4.element.Tag):
    """
    returns a structured table for a beautiful soup table
    """

    # ----------------------------------------------------------------------
    # 1. Get your column names
    my_columns = utils.get_column_names(table)
    # max_rowspan = 0

    # get all values
    records = []
    rows = table.find_all('tr')

    # Default values as none...
    year = None; season=None; winner=None;

    # This is used as a guard door which when closed, doesn;t allow addition of data...
    FOUND_INDEX_COL = False

    # 2. Iterate through rows.
    for row in rows[1:]:

        # 3. get row indexes
        # get the year and season – then, get out of there...
        # index_col = row.find('td', {'rowspan':True})
        index_col = row.select_one(
            'td[align="center"], \
            td[style="text-align:center"], \
            th[align="center"], \
            th[style="text-align:center"]'
            )
        # row.find('td', {'align':'center'})

        if index_col:
            FOUND_INDEX_COL = True
            # Year is either bold or is the 1st link
            if index_col.find('b'):
                year = utils.get_number_from_str(index_col.find('b').text)
            else:
                year = utils.get_number_from_str(index_col.find('a').text)

            season = utils.get_text_from_tag(index_col.find('a',{'href':True, 'title':True}),'title')
            # continue
            # n_rowspan = int(utils.remove_punctuation(index_col.get('rowspan')))
            # if n_rowspan >= max_rowspan:
            #     max_rowspan = n_rowspan
            #
            #     # Get the year and skip to the next item in the loop
            #     year = int(index_col.find('b').text)
            #     season = utils.get_text_from_tag(index_col.find('a',{'href':True, 'title':True}),'title')
            #     continue
            #
            # # Continue as normal
            # else:
            #     None

        # 4. Is this row a winner?
        # Figure out if they won the tony award or not...
        winning_attrs={'style':'background:#B0C4DE'}
        winner = utils.is_this_a_winner(row, winning_attrs)


        # 5. Initialize record
        # Begin the record....
        rec = {'year':year, 'season': season, 'winner':winner}


        # 6. Iterate through each row (get cell values)
        # i = 1 since index_col is i=0
        my_cells = row.select(f'td:not(.table-na):not([colspan="{len(my_columns)}"]):not([colspan="{len(my_columns)+1}"]):not([align="center"])')

        # If you haven't got any data, skip
        if not my_cells:
            continue
        # I'm not sure we should do this...
        # if len(my_cells)==1:
        #     continue

        # If you have the same number, remove the first cell
        if len(my_cells)==len(my_columns):
            del my_cells[0]

        i=1
        for cell in my_cells:

            #how many rows does this cell span?
            n_cols = int(utils.remove_punctuation(cell.get("colspan", 1)))

            for j in range(n_cols):

                col_name = my_columns[i]
                val = utils.get_text_from_tag(cell.text)

                # 7. Store your values
                rec.update({col_name: val})
                # get the text

                # 8. Augement values, if necessary
                # if there's a link, get the link
                if cell.find("a", {"href":True}):
                    href = cell.find("a").get("href")
                    href = 'https://en.wikipedia.org' + href
                    rec.update({col_name + "_link": href})


                # done iterating through this cell...
                i+=1

        # 9. save your row
        records.append(rec)


    # 10. All done!
    return records
