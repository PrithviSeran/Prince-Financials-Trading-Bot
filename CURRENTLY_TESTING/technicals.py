import sys
sys.path.append("/Users/prithviseran/Documents/Forex_Trading_Bot_Server")

from Files_to_be_Imported.all_apis import Oanda_API
import plotly.graph_objects as go

Oanda_API_access = Oanda_API()
LOOK_THROUGH = 1


hour_data = Oanda_API_access.fetch_candlesticks(instrument = "EUR_USD",
                                                 candles_count = "300",
                                                 granularity = "H1")
fig = go.Figure(data=[
            go.Line(
            x = list(range(len(hour_data) - LOOK_THROUGH)),
            y = hour_data.BC[:-LOOK_THROUGH]
            )])


def highs(hour_data, look_through):

    closings = hour_data.BC.to_numpy()
    closing_highs = []
    index = []

    for i in range(look_through, len(hour_data) - look_through, 1):

        prev_closing = closings[i - 1]
        current_highest = closings[i]
        next_highest = closings[i + 1]

        max_on_interval = max(closings[i - look_through: i + look_through])

        if prev_closing < current_highest and next_highest < current_highest:

            if current_highest == max_on_interval:

                #fig.add_vline(x = i, line_width=3, line_dash="dash", line_color="red")

                closing_highs.append(current_highest)
                index.append(i)
        
            #all_highs.append(current_highest)
            #lower_highs_index.append(i)
    return (closing_highs, index)


def lows(hour_data, look_through):

    closings = hour_data.BC.to_numpy()
    closing_lows = []
    index = []

    for i in range(look_through, len(hour_data) - look_through, 1):

        prev_closing = closings[i - 1]
        current_highest = closings[i]
        next_highest = closings[i + 1]

        max_on_interval = min(closings[i - look_through: i + look_through])

        if prev_closing > current_highest and next_highest > current_highest:

            if current_highest == max_on_interval:

                #fig.add_vline(x = i, line_width=3, line_dash="dash", line_color="green")

                closing_lows.append(current_highest)
                index.append(i)
        
            #all_highs.append(current_highest)
            #lower_highs_index.append(i)
    return (closing_lows, index)


def break_of_structure_for_backtesting(hour_data, trend, backtesting):
    # True if up trend
    all_highs, high_indexes = highs(hour_data, 1)
    all_lows, low_indexes = lows(hour_data, 1)

    if backtesting:
        for i in range(1, len(all_highs) - 2, 1):
            if all_highs[i + 1] > all_highs[i] > all_highs[i - 1] and all_lows[i + 1] > all_lows[i] > all_lows[i - 1]: #not trend and 
                fig.add_vline(x = high_indexes[i], line_width=3, line_dash="dash", line_color="green")
                #trend = True
            #elif all_highs[i + 1] < all_highs[i] < all_highs[i - 1] and all_lows[i + 1] < all_lows[i] < all_lows[i - 1]:
               # fig.add_vline(x = low_indexes[i], line_width=3, line_dash="dash", line_color="red")
              #  trend = False

    else:
        current_high = all_highs[-1]
        prev_high = all_highs[-2]

        current_low = all_lows[-1]
        prev_low = all_lows[-2]

        if not trend and current_high > prev_high:
            return True 
        elif trend and prev_low < current_low:
            return False 
    
    return trend
    

def identify_trends_for_backtesting(all_highs, high_indexes, all_lows, low_indexes):

    trend = [] 

    #down trend
    for i in range(1, len(all_highs) - 1, 1):
        if all_highs[i - 1] < all_highs[i] < all_highs[i + 1]: #and trend:
            #fig.add_vline(x = high_indexes[i], line_width=3, line_dash="dash", line_color="green")
            trend.append((False, high_indexes[i]))

    #down trend
    for i in range(1, len(all_lows) - 1, 1):
        if all_lows[i - 1] > all_lows[i] > all_lows[i + 1]: #and not trend:
            #fig.add_vline(x = low_indexes[i], line_width=3, line_dash="dash", line_color="red")
            trend.append((True, low_indexes[i]))

    trend = sorted(trend, key=lambda x: x[1])

    i = 0
    while i < len(trend) - 1:
        if trend[i + 1][0] == trend[i][0]:
            trend.pop(i + 1)
        else:
            i = i + 1

    return trend


def identify_trend_for_trade(all_highs, all_lows):

    print(all_highs[-3], all_highs[-2], all_highs[-1])

    if all_highs[-3] < all_highs[-2] < all_highs[-1]:
        return "Buy!"
    
    if all_lows[-3] > all_lows[-2] > all_lows[-1]:
        return "Short!"
    
    return "Remain!"


"""
    create suport levels, 

"""


def graph_trend(trends):

    print(trends)

    for trend in trends:
        if trend[0]:
            fig.add_vline(x = trend[1], line_width=3, line_dash="dash", line_color="red")
        else:
            fig.add_vline(x = trend[1], line_width=3, line_dash="dash", line_color="green")



if __name__ == "__main__":

    all_highs, high_indexes = highs(hour_data, 1)
    all_lows, low_indexes = highs(hour_data, 1)

    print(identify_trend_for_trade(all_highs, all_lows))

    #trend = identify_trends_for_backtesting(all_highs, high_indexes, all_lows, low_indexes)

    #graph_trend(trend)

    #fig.show()