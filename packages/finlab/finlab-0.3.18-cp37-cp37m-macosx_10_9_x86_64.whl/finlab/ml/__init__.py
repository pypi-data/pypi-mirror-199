from finlab.market_info import TWMarketInfo


market = TWMarketInfo()

def set_market(new_market):

    global market

    if isinstance(new_market, type):
        market = new_market()
    else:
        market = new_market

def reset_market():
    global market
    market = TWMarketInfo()
