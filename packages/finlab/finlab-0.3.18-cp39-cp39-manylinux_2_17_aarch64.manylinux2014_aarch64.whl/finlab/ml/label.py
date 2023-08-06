import pandas as pd
from collections.abc import Iterable
from finlab import ml
from finlab.market_info import MarketInfo, TWMarketInfo
from typing import Optional
from finlab.ml.utils import resampler

def pct_change(index: pd.Index, resample=None, period=1, market:Optional[MarketInfo]=TWMarketInfo(), **kwargs):

    if market is None:

        market = ml.market

    assert market is not None

    adj = market.get_price('close', adj=True).shift(-1)
    uadj = resampler(adj, resample, **kwargs)
    ret = (uadj.shift(-period) / uadj).unstack()
    ret = ret.swaplevel(0, 1).reindex(index)
    ret.index = ret.index.set_names(['datetime', 'instrument'])
    return ret - 1







