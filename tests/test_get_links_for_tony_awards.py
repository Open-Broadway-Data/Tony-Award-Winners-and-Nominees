import pytest
from itertools import groupby
from scrape_wikipedia import methods
from scrape_wikipedia import WikiScraper, base_url


def all_equal(iterable):
    """A very fast way of comparing if all objects in an iterable are equal"""
    g = groupby(iterable)
    return next(g, True) and not next(g, False)




def test_from_method():

    all_links = methods.get_links_for_tony_awards()

    # Assert the list is not empty
    assert len(all_links)>0
    # Assert there are > 40 links
    assert len(all_links)>40
    # Assert the list contains string values
    assert isinstance(all_links[-1], str)

    return all_links


def test_from_object():
    all_links = WikiScraper.get_links_for_tony_awards()

    # Assert the list is not empty
    assert len(all_links)>0
    # Assert there are > 40 links
    assert len(all_links)>40
    # Assert the list contains string values
    assert isinstance(all_links[-1], str)

    return all_links


def test_from_initialized_object():
    ws = WikiScraper(base_url)

    all_links = ws.get_links_for_tony_awards()

    # Assert the list is not empty
    assert len(all_links)>0
    # Assert there are > 40 links
    assert len(all_links)>40
    # Assert the list contains string values
    assert isinstance(all_links[-1], str)

    return all_links



def test_all_equal(*lists):
    val = all_equal(lists)
    assert val







# ------------------------------------------------------

if __name__ == '__main__':

    # test the method directly
    x1 = test_from_method()

    # test the method on the scraper object
    x2 = test_from_object()

    # test the method on an initialized scraper object
    x3 = test_from_initialized_object()


    test_all_equal(x1,x2,x3)



#
