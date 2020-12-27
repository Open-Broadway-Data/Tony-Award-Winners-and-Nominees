from scrape_wikipedia.utils import get_number_from_str

def test_get_number_from_str_float():
    """Quick test that everything works"""

    x = get_number_from_str('1,000.009 employees\n hi 200', 'first', coerce_type='float')
    assert x == 1000.009


def test_get_number_from_str_int():
    """Quick test that everything works"""

    x = get_number_from_str('1,000.009 employees\n hi 200', 'first', coerce_type='int')
    assert x == 1000
