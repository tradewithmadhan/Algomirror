"""
OpenAlgo Expiry Date Extraction Example
----------------------------------------
Demonstrates how to extract current week, next week, current month,
and next month expiry dates using the OpenAlgo Python SDK.

Reference: AlgoMirror Strategy Executor implementation
"""

from openalgo import api
from datetime import datetime


def get_expiry_dates(api_key: str, symbol: str = "NIFTY", host: str = "http://127.0.0.1:5000"):
    """
    Fetch and categorize expiry dates from OpenAlgo API.

    Args:
        api_key: Your OpenAlgo API key
        symbol: Index symbol (NIFTY, BANKNIFTY, SENSEX, etc.)
        host: OpenAlgo host URL

    Returns:
        dict with current_week, next_week, current_month, next_month expiries
    """
    client = api(api_key=api_key, host=host)

    # Determine exchange based on symbol
    exchange = "BFO" if symbol == "SENSEX" else "NFO"

    # Fetch expiry dates from OpenAlgo
    response = client.expiry(symbol=symbol, exchange=exchange)

    if response.get("status") != "success":
        raise Exception(f"Failed to fetch expiries: {response.get('message')}")

    expiries = response.get("data", [])
    if not expiries:
        raise Exception(f"No expiries available for {symbol}")

    # Parse and sort expiries chronologically
    def parse_expiry(exp_str):
        """Parse expiry string to datetime"""
        formats = ["%d-%b-%y", "%d%b%y", "%d-%B-%y", "%d%B%y"]
        exp_upper = exp_str.upper().strip()
        for fmt in formats:
            try:
                return datetime.strptime(exp_upper, fmt)
            except ValueError:
                continue
        return datetime.max

    sorted_expiries = sorted(expiries, key=parse_expiry)

    # Extract expiry dates by category
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    next_month = (current_month % 12) + 1
    next_year = current_year + 1 if next_month == 1 else current_year

    result = {
        "current_week": None,
        "next_week": None,
        "current_month": None,
        "next_month": None,
        "all_expiries": sorted_expiries
    }

    # Current week = nearest expiry (index 0)
    if sorted_expiries:
        result["current_week"] = sorted_expiries[0]

    # Next week = second expiry (index 1)
    if len(sorted_expiries) > 1:
        result["next_week"] = sorted_expiries[1]

    # Current month = last expiry of current calendar month
    for exp_str in sorted_expiries:
        exp_date = parse_expiry(exp_str)
        if exp_date.month == current_month and exp_date.year == current_year:
            result["current_month"] = exp_str  # Keep updating to get the last one

    # Next month = last expiry of next calendar month
    for exp_str in sorted_expiries:
        exp_date = parse_expiry(exp_str)
        if exp_date.month == next_month and exp_date.year == next_year:
            result["next_month"] = exp_str  # Keep updating to get the last one

    return result


# Example usage
if __name__ == "__main__":
    API_KEY = "your_openalgo_api_key"

    # Get NIFTY expiries
    expiries = get_expiry_dates(API_KEY, symbol="NIFTY")

    print("NIFTY Expiry Dates:")
    print(f"  Current Week : {expiries['current_week']}")
    print(f"  Next Week    : {expiries['next_week']}")
    print(f"  Current Month: {expiries['current_month']}")
    print(f"  Next Month   : {expiries['next_month']}")
    print(f"\nAll Expiries: {expiries['all_expiries']}")
