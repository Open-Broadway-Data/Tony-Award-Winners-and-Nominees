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

    # If 'year' isn't in the table, skip
    if 'year' not in (x.lower() for x in my_columns):
        return []

    # get all values
    records = []
    rows = table.find_all('tr')

    # Default values as none...
    year = None; season=None; winner=None;

    # 2. Iterate through rows.
    for row in rows[1:]:

        # 3. get row indexes
        # get the year and season – then, get out of there...
        # index_col = row.find('td', {'rowspan':True})
        index_col = row.select_one(
            'td[align="center"],'
            'td[style*="text-align:center"],'
            'th[align="center"],'
            'th[style*="text-align:center"]',
            )

        if index_col:
            # Year is either bold or is the 1st link
            if index_col.find('b'):
                year = utils.get_number_from_str(index_col.find('b').text)
            else:
                year = utils.get_number_from_str(index_col.find('a').text)

            season = utils.get_text_from_tag(index_col.find('a',{'href':True, 'title':True}),'title')
            # continue

        # 4. Is this row a winner?
        # Figure out if they won the tony award or not...
        if row.get('style') and 'background:#B0C4DE' in row.get('style'):
            winner = True
        else:
            winner = False
        # winning_attrs={'style':'background:#B0C4DE'}
        # winner = utils.is_this_a_winner(row, winning_attrs)


        # 5. Initialize record
        # Begin the record....
        rec = {'year':year, 'season': season, 'winner':winner}


        # 6. Iterate through each row (get cell values)
        # i = 1 since index_col is i=0
        my_cells = row.select(
            f'td:not(.table-na)'
            f':not([colspan="{len(my_columns)}"])'
            f':not([colspan="{len(my_columns)+1}"])'
            f':not([align="center"])'
            f':not([style="text-align:center"])'
        )

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

            #how many cols does this cell span?
            n_cols = int(utils.remove_punctuation(cell.get("colspan", 1)))

            #how many rows does this cell span?
            n_rows = int(utils.remove_punctuation(cell.get("rowspan", 1)))
            # if n_rows>0:
            #     print(f'Do something here... Current column = {i}; current row = {len(records)}')
            #     print(len(my_cells), n_cols)

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
