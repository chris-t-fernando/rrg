from symbol import Symbol
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from colour import Color
import numpy as np

_ddof = 1
_window = 50


# expects
def add_price_relative(df: pd.DataFrame, relative_to: str):
    for c in df.columns:
        if c != relative_to:
            column_name = f"{c}_PR"
            df[column_name] = 100 * (df[c] / df[relative_to])
    return df


# The JdK RS ratio is then calculated as follows:100 + ((relative - rolling_mean) / rolling_std)
def add_rs_ratio(df: pd.DataFrame, symbols: list[str]):
    for s in symbols:
        column_name = f"{s}_RS_RATIO"
        pr_col = f"{s}_PR"
        df[column_name] = 101 + (
            (df[pr_col] - df[pr_col].rolling(window=_window).mean())
            / df[pr_col].rolling(window=_window).std(ddof=_ddof)
        )

    return df


def rs_ratio(prices_df, benchmark, window=10):
    from numpy import mean, std

    for series in prices_df:
        rs = (prices_df[series].divide(benchmark)) * 100
        rs_ratio = rs.rolling(window).mean()
        rel_ratio = 100 + ((rs_ratio - rs_ratio.mean()) / rs_ratio.std() + 1)
        prices_df[series] = rel_ratio
    prices_df.dropna(axis=0, how="all", inplace=True)
    return prices_df


def add_roc(df: pd.DataFrame, symbols: list[str]):
    for s in symbols:
        column_name = f"{s}_ROC"
        rs_col = f"{s}_RS_RATIO"
        df[column_name] = 100 * (df[rs_col] / df[rs_col].shift(1) - 1)

    return df


# 100 + ((momentum - momentum_rolling_mean) / momentum_rolling_std)
def add_rm(df: pd.DataFrame, symbols: list[str]):
    for s in symbols:
        column_name = f"{s}_RM"
        roc_col = f"{s}_ROC"
        df[column_name] = 100 + (
            (df[roc_col] - df[roc_col].rolling(window=_window).mean())
            / df[roc_col].rolling(window=_window).std(ddof=_ddof)
        )
    return df


def rs_ratio(prices_df, benchmark, window=10):
    from numpy import mean, std

    for series in prices_df:
        rs = (prices_df[series].divide(benchmark)) * 100
        rs_ratio = rs.rolling(window)
        rel_ratio = 100 + ((rs - rs_ratio.mean()) / rs_ratio.std(ddof=0) + 1)
        #                    100 + ((JDK_RS_momentum[ticker] - JDK_RS_momentum[ticker].rolling(10).mean())/JDK_RS_momentum[ticker].rolling(10).std() + 1)
        prices_df[series] = rel_ratio
    prices_df.dropna(axis=0, how="all", inplace=True)
    return prices_df


"""
8   100.71
9   100.5
10  100.08
13  99.77
14  99.53
"""

"""
nifty = [
    9039.25,
    9136.85,
    9251.5,
    2859.9,
    9154.4,
    9266.75,
    9111.9,
    8083.8,
    8660.25,
    8745.45,
    9955.2,
    10989.45,
    11201.75,
    12080.85,
]

pharma = [
    9600.65,
    9093,
    9343.35,
    9327.1,
    9518.45,
    9157.75,
    8800.45,
    7361.6,
    6813.05,
    6951.9,
    7268,
    8018.3,
    7576.75,
    8364.35,
]
pharma.reverse()
nifty.reverse()

df = pd.DataFrame(list(zip(nifty, pharma)), columns=["nifty", "pharma"])

combined1 = add_price_relative(df, "nifty")
combined1 = add_rs_ratio(combined1, ["pharma"])
combined1 = add_roc(combined1, ["pharma"])
combined1 = add_rm(combined1, ["pharma"])
"""

# sp200 = Symbol(yf_symbol="^AXJO", interval="1d")
# xhj = Symbol(yf_symbol="^AXHJ", interval="1d")
# xij = Symbol(yf_symbol="^AXIJ", interval="1d")
# xre = Symbol(yf_symbol="^AXRE", interval="1d")

gspc = Symbol(yf_symbol="^GSPC", interval="1d")
# xly = Symbol(yf_symbol="XLY", interval="1d")
xly = Symbol(yf_symbol="^SP500-25", interval="1d")

symbols = ["xly"]
combined = pd.DataFrame()
combined["gspc"] = gspc.ohlc.bars.Close
combined["xly"] = xly.ohlc.bars.Close

prices_df = pd.DataFrame()
prices_df["xly"] = xly.ohlc.bars.Close
benchmark = gspc.ohlc.bars.Close
z = rs_ratio(prices_df, benchmark)

combined = add_price_relative(combined, "gspc")
combined = add_rs_ratio(combined, symbols)
combined = add_roc(combined, symbols)
combined = add_rm(combined, symbols)

"""
symbols = ["xhj", "xij", "xre"]
combined = pd.DataFrame()
combined["asx"] = sp200.ohlc.bars.Close
combined["xhj"] = xhj.ohlc.bars.Close
combined["xij"] = xij.ohlc.bars.Close
combined["xre"] = xre.ohlc.bars.Close

combined = add_price_relative(combined, "asx")
combined = add_rs_ratio(combined, symbols)
combined = add_roc(combined, symbols)
combined = add_rm(combined, symbols)
"""

print("banan")

# spline = make_interp_spline(combined.iloc[-15:-1].xhj_RS_RATIO, combined.iloc[-15:-1].xhj_RM)


ax1 = plt.axes()
# axis1.plot(combined.iloc[-15:-1].xhj_RS_RATIO, combined.iloc[-15:-1].xhj_RM, format="o")
# plt.show()

tail_len = 10
red = Color("maroon")
blue = Color("gray")
colours = list(red.range_to(blue, tail_len - 1))
hex_colours = [str(x) for x in colours]

x = combined.iloc[-tail_len:-1].xly_RS_RATIO
y = combined.iloc[-tail_len:-1].xly_RM
labels = combined.index[-tail_len:-1]

# ax1.plot(x, y, "C3", c=hex_colours, lw=1)
ax1.scatter(x, y, c=hex_colours, s=80)
ax1.axvline(c="grey", lw=1, x=100)
ax1.axhline(c="grey", lw=1, y=100)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

lc = LineCollection(segments, colors=hex_colours)
lc.set_array(np.linspace(0, 1, len(x)))
lc.set_linewidth(2)
line = ax1.add_collection(lc)

for i in range(0, tail_len - 1):
    label = str(labels[i].date())

    plt.annotate(
        label,  # this is the text
        (x.iloc[i], y.iloc[i]),  # these are the coordinates to position the label
        textcoords="offset points",  # how to position the text
        xytext=(0, 10),  # distance from text to points (x,y)
        ha="center",
    )  # horizontal alignment can be left, right or center


plt.show()
print("banana")
