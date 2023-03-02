import numpy as np
import pandas as pd
import pandas_ta as ta
from ta.momentum import PercentagePriceOscillator
from symbol import SymbolData


def calculate_trend(values):
    if len(values) == 0:
        return 0, 0

    x = np.arange(1, len(values) + 1, 1)
    y = np.array(values)
    #  Handle nan values
    x_new = x[~np.isnan(y)]
    y_new = y[~np.isnan(y)]
    m, c = np.polyfit(x_new, y_new, 1)
    return m, c


def calculate_ppo_hist_slope(df):
    df["PPO_HIST_SLOPE"] = 0

    for i, row in df.iterrows():
        # for index in range(0, len(df)):
        index = df.index.get_loc(i)
        if index <= 2:
            continue
        ppo_hist_lb = df["PPO_HIST"].values[index - 3 : index]
        check_nan = np.isnan(ppo_hist_lb)
        if True in check_nan:
            continue
        m, c = calculate_trend(ppo_hist_lb)
        i = df.index[index]
        df.at[i, "PPO_HIST_SLOPE"] = m

    # my func
    # df.A - df.A.shift(1)
    # use apply for calc trend using shift to get last 3

    return df


def calculate_indicators(df):
    #  Long-term
    df["EMA_200"] = ta.ema(df["Close"], length=200)
    df["EMA_200_CLOSE_PC"] = (df["Close"] / df["EMA_200"]) * 100
    df["ROC_125"] = ta.momentum.roc(close=df["Close"], window=125)
    #  Mid-term
    df["EMA_50"] = ta.ema(df["Close"], length=50)
    df["EMA_50_CLOSE_PC"] = (df["Close"] / df["EMA_50"]) * 100
    df["ROC_20"] = ta.momentum.roc(close=df["Close"], window=20)
    # Short-term
    ppo_ind = PercentagePriceOscillator(
        close=df["Close"], window_slow=26, window_fast=12, window_sign=9
    )
    df["PPO"] = ppo_ind.ppo()
    df["PPO_EMA_9"] = ta.ema(df["PPO"], length=9)
    df["PPO_HIST"] = df["Close"] - df["PPO_EMA_9"]
    #  Calculate PPO histogram slope
    df = calculate_ppo_hist_slope(df)
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    return df


def calculate_weights(df):
    #  Long-term
    df["EMA_200_CLOSE_PC_WEIGHTED"] = df["EMA_200_CLOSE_PC"] * 0.3
    df["ROC_125_WEIGHTED"] = df["ROC_125"] * 0.3
    #  Mid-term
    df["EMA_50_CLOSE_PC_WEIGHTED"] = df["EMA_50_CLOSE_PC"] * 0.15
    df["ROC_20_WEIGHTED"] = df["ROC_20"] * 0.15
    #  Short-term
    df["RSI_WEIGHTED"] = df["RSI"] * 0.05
    df["PPO_HIST_SLOPE_WEIGHTED"] = 0
    df.loc[df["PPO_HIST_SLOPE"] < -1, "PPO_HIST_SLOPE_WEIGHTED"] = 0
    df.loc[df["PPO_HIST_SLOPE"] >= -1, "PPO_HIST_SLOPE_WEIGHTED"] = (
        (df["PPO_HIST_SLOPE"] + 1) * 50 * 0.05
    )
    df.loc[df["PPO_HIST_SLOPE"] > 1, "PPO_HIST_SLOPE_WEIGHTED"] = 5
    return df


def calculate_sctr(df):
    df["IND_SCORE"] = (
        df["EMA_200_CLOSE_PC_WEIGHTED"]
        + df["ROC_125_WEIGHTED"]
        + df["EMA_50_CLOSE_PC_WEIGHTED"]
        + df["ROC_20_WEIGHTED"]
        + df["RSI_WEIGHTED"]
        + df["PPO_HIST_SLOPE_WEIGHTED"]
    )
    return df


def fetch_price_data(symbol: str):
    return SymbolData(symbol, "1d").bars


if __name__ == "__main__":
    # nasdaq_100_df = fetch_nasdaq_100_list().head(100)
    # symbols = nasdaq_100_df['Symbol'].unique()
    symbols = [
        "ABNB",
        "ADBE",
        "ADI",
        "ADP",
        "ADSK",
        "AEP",
        "ALGN",
        "AMAT",
        "AMD",
        "AMGN",
        "ANSS",
        "ASML",
        "ATVI",
        "AVGO",
        "AZN",
        "BIIB",
        "BKNG",
        "BKR",
        "CDNS",
        "CEG",
        "CHTR",
        "CMCSA",
        "COST",
        "CPRT",
        "CRWD",
        "CSCO",
        "CSGP",
        "CSX",
        "CTAS",
        "CTSH",
        "DDOG",
        "DLTR",
        "DXCM",
        "EA",
        "EBAY",
        "ENPH",
        "EXC",
        "FANG",
        "FAST",
        "FISV",
        "FTNT",
        "GFS",
        "GILD",
        "GOOG",
        "GOOGL",
        "HON",
        "IDXX",
        "ILMN",
        "INTC",
        "INTU",
        "ISRG",
        "JD",
        "KDP",
        "KHC",
        "KLAC",
        "LCID",
        "LRCX",
        "LULU",
        "MAR",
        "MCHP",
        "MDLZ",
        "MELI",
        "META",
        "MNST",
        "MRNA",
        "MRVL",
        "MSFT",
        "MU",
        "NFLX",
        "NVDA",
        "NXPI",
        "ODFL",
        "ORLY",
        "PANW",
        "PAYX",
        "PCAR",
        "PDD",
        "PEP",
        "PYPL",
        "QCOM",
        "REGN",
        "RIVN",
        "ROST",
        "SBUX",
        "SGEN",
        "SIRI",
        "SNPS",
        "TEAM",
        "TMUS",
        "TXN",
        "VRSK",
        "VRTX",
        "WBA",
        "WBD",
        "WDAY",
        "XEL",
        "ZM",
        "ZS",
    ]

    # symbols = [
    #    "ABNB",
    #    "ADBE",
    #    "ADI",
    #    "ADP",
    # ]

    # recent_sctr_df = pd.DataFrame({})
    if False:
        recent_sctr_df = pd.DataFrame(columns=["datetime", "symbol", "IND_SCORE"])
        price_data_dict = {}
        first = True
        prices = {}
        for symbol in symbols:
            this_price = fetch_price_data(symbol)
            if this_price is None or len(this_price) == 0:
                continue
            prices[symbol] = this_price
            print(f"Got data for {symbol}")

        # current = this_price.index[0]
        # last = this_price.index[-1]

        for this_date in this_price.index[200:]:
            for s, price_df in prices.items():
                #  Calculate indicators
                price_df = calculate_indicators(price_df)
                #  Calculate weights
                price_df = calculate_weights(price_df)
                #  Calculate indicator score
                price_df = calculate_sctr(price_df)
                price_data_dict[symbol] = price_df
                #  Store recent indicator score
                # row = pd.DataFrame(
                #    {"symbol": [symbol], "IND_SCORE": [price_df["IND_SCORE"].iloc[-1]]}
                # )
                # recent_sctr_df = pd.concat([recent_sctr_df, row], axis=0, ignore_index=True)

                row = pd.DataFrame(
                    {
                        "datetime": this_date,
                        "symbol": [s],
                        "IND_SCORE": [price_df["IND_SCORE"].loc[this_date]],
                        "rank": -1,
                    }
                )
                recent_sctr_df = pd.concat(
                    [recent_sctr_df, row], axis=0, ignore_index=True
                )
                """
                if first:
                    recent_sctr_df.loc[price_df.index[-1]] = [
                        symbol,
                        price_df["IND_SCORE"].iloc[-1],
                    ]
                    recent_sctr_df.index.name = "datetime"
                    recent_sctr_df = recent_sctr_df.set_index(["symbol"], append=True)
                    first = False
                else:
                    recent_sctr_df.loc[(price_df.index[-1], symbol)] = [
                        price_df["IND_SCORE"].iloc[-1],
                    ]
                """
                # print(f"Done {s}")
            print(f"Done {this_date}")
    else:
        prices = {}
        for symbol in symbols:
            this_price = fetch_price_data(symbol)
            if this_price is None or len(this_price) == 0:
                continue
            prices[symbol] = this_price
            print(f"Got data for {symbol}")
        recent_sctr_df = pd.read_csv("recent_sctr_df.csv", index_col=0)

    # create the index
    col_index = pd.MultiIndex.from_product(
        [symbols, ["sctr"]], names=["symbol", "sctr_col"]
    )

    # create the data frame structure
    ndf = pd.DataFrame(index=recent_sctr_df.datetime.unique(), columns=col_index)

    # populate the data frame structure - there's 100% a better way than this but whatevs
    for s in recent_sctr_df.symbol.unique():
        ndf.loc[:, (s, "sctr")] = (
            recent_sctr_df["IND_SCORE"].loc[recent_sctr_df.symbol == s].tolist()
        )
        ndf.loc[:, (s, "close")] = prices[s].Close[ndf.index]

    # used for selecting 2nd level columns
    idx = pd.IndexSlice
    ranks = ndf.loc[slice(None), idx[:, "sctr"]].rank(axis=1, ascending=False)
    ranks = ranks.rename(columns={"sctr": "rank"})
    nndf = ndf.join(ranks)
    """
    for s in recent_sctr_df.symbol.unique():
        nndf.loc[:, (s, "held")] = False
        nndf.loc[:, (s, "transactions")] = 0

        # buy in conditions
        a = nndf[s]["rank"].shift() > 25
        b = nndf[s]["rank"] <= 25
        c = a & b
        nndf.loc[:, (s, "transactions")].loc[c.index[c]] = (
            prices[s]["Close"][c.index[c]] * -1
        )
        nndf.loc[:, (s, "held")].loc[c.index[c]] = True

        # sell out conditions
        # d = nndf[s]["rank"].shift() <= 25
        # e = nndf[s]["rank"] > 25
        # f = nndf[s]["close"].loc[c.index[c]]
        # g = d & e & f
        # nndf.loc[:, (s, "transactions")].loc[g.index[g]] = prices[s]["Close"][
        #    g.index[g]
        # ]
"""
    nndf = nndf.reindex(sorted(nndf.columns), axis=1)

    """
             itm
        yes      no
              |
    yes  hodl |  hodl - bad day for everyone
              |
top25   --------------
              |
    no  sell  |  sell hard
              |      
    """
    import math

    top_quarter = math.floor(len(symbols) / 4)

    for s in recent_sctr_df.symbol.unique():
        nndf.loc[:, (s, "action")] = None
        nndf.loc[:, (s, "held")] = False
        nndf.loc[:, (s, "buy_in_cost")] = None
        nndf.loc[:, (s, "balance")] = 0
        for i, row in nndf[s].iterrows():
            row_index_pos = nndf.index.get_loc(row.name)
            prev_row_index = nndf.iloc[row_index_pos - 1].name
            prev_row = nndf[s].loc[prev_row_index]

            this_close = row.close
            last_close = prev_row.close

            this_top_25 = row["rank"] <= top_quarter
            last_top_25 = prev_row["rank"] <= top_quarter

            if prev_row["held"]:
                itm = this_close > prev_row["buy_in_cost"]
                take_profit = this_close > prev_row["buy_in_cost"] * 1.1
                if take_profit:
                    nndf.at[i, (s, "action")] = "sell - 5% profit"
                    nndf.at[i, (s, "balance")] = (
                        prev_row["balance"] + this_close - prev_row["buy_in_cost"]
                    )
                elif this_top_25 and itm:
                    # do nothing
                    nndf.at[i, (s, "action")] = "hodl - itm and ranked"
                    nndf.at[i, (s, "held")] = True
                    nndf.at[i, (s, "buy_in_cost")] = prev_row["buy_in_cost"]
                    nndf.at[i, (s, "balance")] = prev_row["balance"]
                elif this_top_25 and not itm:
                    # bad day for everyone
                    nndf.at[i, (s, "action")] = "hodl - just a bad day"
                    nndf.at[i, (s, "held")] = True
                    nndf.at[i, (s, "buy_in_cost")] = prev_row["buy_in_cost"]
                    nndf.at[i, (s, "balance")] = prev_row["balance"]
                elif not this_top_25 and itm:
                    # take the money and run
                    nndf.at[i, (s, "action")] = "sell - take profit"
                    nndf.at[i, (s, "balance")] = (
                        prev_row["balance"] + this_close - prev_row["buy_in_cost"]
                    )
                elif not this_top_25 and not itm:
                    # dog stock, bail out
                    nndf.at[i, (s, "action")] = "sell - stop loss"
                    nndf.at[i, (s, "balance")] = (
                        prev_row["balance"] + this_close - prev_row["buy_in_cost"]
                    )
            else:
                # determine if we want to buy in
                if this_top_25:
                    nndf.at[i, (s, "action")] = "buy in"
                    nndf.at[i, (s, "held")] = True
                    nndf.at[i, (s, "buy_in_cost")] = this_close
                nndf.at[i, (s, "balance")] = prev_row["balance"]

            # print(f"\tFinished backtesting {row.name}")
        print(f"Finished backtesting {s}")

    nndf = nndf.reindex(sorted(nndf.columns), axis=1)

    # nndf.loc[:, (slice(None), "balance")].tail(1).sum().rank()
    nndf.loc[:, (slice(None), "balance")].tail(1).sum().sum()
    nndf.loc[:, (slice(None), "balance")].tail(1).sum()

    print("a")

    # prices[s]["Close"][f.index[f]]

    # ndf.loc[slice(None), idx[:, 'sctr']]

    #
    #
    #

    recent_sctr_df["IND_SCORE"].loc[recent_sctr_df.symbol == "ABNB"].tolist()

    df = recent_sctr_df.set_index(["datetime", "symbol"]).sort_index()
    # df.IND_SCORE.loc[(pd.Timestamp('2023-02-23 00:00:00-0500', tz='America/New_York'), 'ADP')]
    # df.loc[(pd.Timestamp('2023-02-23 00:00:00-0500', tz='America/New_York'), slice(None))]

    # Sort by max indicator score
    for this_date in df.index.get_level_values(0):
        rank = 1
        sorted = df.loc[
            (
                this_date,
                slice(None),
            )
        ].sort_values(by="IND_SCORE", ascending=False)
        for i in sorted.index:
            df["rank"].loc[(this_date, i)] = rank
            rank += 1

    # so now you can iterate through finding where there's changes
    df["rank_diff"] = df["rank"] - df["rank"].shift(len(symbols))
    df.loc[df["rank_diff"] > 0]

    # recent_sctr_df.sort_values(by="IND_SCORE", ascending=True).reset_index(
    #    inplace=True, drop=True
    # )
    # sorted_sctr_df = sorted_sctr_df.sort_values(by="IND_SCORE", ascending=False)
    # sorted_sctr_df["SCTR"] = sorted_sctr_df.index
    print("banana")
    #  Store csv with results
    # path = os.path.join(RESULTS_DIR, 'sctr_df.csv')
    # sorted_sctr_df.to_csv(path)


"""
date    symbol      score       rank
1/1/1   amzn        50          99
2/1/1   amzn        49          90
ndf = pd.DataFrame(recent_sctr_df, index=recent_str_dr.datetime, columns=
"""
