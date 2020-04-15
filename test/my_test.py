

from app.robo_advisor import to_usd

def test_to_usd():
     #tests that to_usd() creates a string from a float that does the following:
     #         1) converts to two decimals
     #         2) includes commas for thousands place
     #         3) includes dollar sign
     price = 34903.727
     result = to_usd(price)
     assert result == "$34,903.73"