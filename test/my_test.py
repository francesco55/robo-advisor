

from app.robo_advisor import to_usd, hasNumbers

def test_to_usd():
     """
     tests that to_usd() creates a string from a float that does the following:
              1) converts to two decimals
              2) includes commas for thousands place
              3) includes a dollar sign
     """
     price = 34903.727
     result = to_usd(price)
     assert result == "$34,903.73"
    
def test_hasNumbers():
    """
    tests that hasNumbers() correctly returns a bool variable that yields true if a string has numbers and false if a string does not
    """
    bad_string = "we1r"
    good_string = "tsla"
    assert hasNumbers(bad_string) == True
    assert hasNumbers(good_string) == False
