import pandas as pd
import numpy as np
import plotly.graph_objects as go
from all_apis import alpha_vantage_API, Oanda_API
import datetime
import defs
import base64



class data_information():

    def __init__(self):

        pass


    def change_dataset(self, dataset):

        self.dataset = dataset


    def create_graph(self):
        self.fig = go.Figure(data=[
            go.Line(
            x = list(range(len(self.dataset[14:]))),
            y = self.dataset.BC[14:]
            )])
        

    def add_indicator(self, index, color):
        self.fig.add_vline(x=index, line_width=3, line_dash="dash", line_color=color)


    # --- Taken from Henul in StackOverflow ---
    def __ema(self, arr, periods=14, weight=1, init=None):
        leading_na = np.where(~np.isnan(arr))[0][0]
        arr = arr[leading_na:]
        alpha = weight / (periods + (weight-1))
        alpha_rev = 1 - alpha
        n = arr.shape[0]
        pows = alpha_rev**(np.arange(n+1))
        out1 = np.array([])
        if 0 in pows:
            out1 = self.__ema(arr[:int(len(arr)/2)], periods)
            arr = arr[int(len(arr)/2) - 1:]
            init = out1[-1]
            n = arr.shape[0]
            pows = alpha_rev**(np.arange(n+1))
        scale_arr = 1/pows[:-1]
        if init:
            offset = init * pows[1:]
        else:
            offset = arr[0]*pows[1:]
        pw0 = alpha*alpha_rev**(n-1)
        mult = arr*pw0*scale_arr
        cumsums = mult.cumsum()
        out = offset + cumsums*scale_arr[::-1]
        out = out[1:] if len(out1) > 0 else out
        out = np.concatenate([out1, out])
        out[:periods] = np.nan
        out = np.concatenate(([np.nan]*leading_na, out))
        return out


    def __atr(self, highs, lows, closes, periods=14, ema_weight=1):
        hi = np.array(highs)
        lo = np.array(lows)
        c = np.array(closes)
        tr = np.vstack([np.abs(hi[1:]-c[:-1]),
                        np.abs(lo[1:]-c[:-1]),
                        (hi-lo)[1:]]).max(axis=0)
        atr = self.__ema(tr, periods=periods, weight=ema_weight)
        atr = np.concatenate([[np.nan], atr])
        return atr


    def adx(self, periods=14):
        highs = self.dataset.BH.to_numpy()
        lows = self.dataset.BL.to_numpy()
        closes = self.dataset.BC.to_numpy()
        up = highs[1:] - highs[:-1]
        down = lows[:-1] - lows[1:]
        up_idx = up > down
        down_idx = down > up
        updm = np.zeros(len(up))
        updm[up_idx] = up[up_idx]
        updm[updm < 0] = 0
        downdm = np.zeros(len(down))
        downdm[down_idx] = down[down_idx]
        downdm[downdm < 0] = 0
        _atr = self.__atr(highs, lows, closes, periods)[1:]
        updi = 100 * self.__ema(updm, periods) / _atr
        downdi = 100 * self.__ema(downdm, periods) / _atr
        zeros = (updi + downdi == 0)
        downdi[zeros] = .0000001
        adx = 100 * np.abs(updi - downdi) / (updi + downdi)
        adx = self.__ema(np.concatenate([[np.nan], adx]), periods)

        return adx, updi, downdi
    # ------------

    def aroon (self, period = 14):
        data = np.array(self.dataset[["BH", "BL"]])
        size = len(data)
        out_up = np.zeros(size)
        out_down = np.zeros(size)
        for i in range(period - 1, size):
            window = np.flip(data[i + 1 - period:i + 1],axis=0)
            out_up[i] = ((period - window[:,0].argmax()) / period)
            out_down[i] = ((period - window[:,1].argmin()) / period)
        
        return out_up, out_down


    # Taken from Lukas Zbinden -------
    def relative_strength_index(self, period = 14, round_rsi = True):
        """ Implements the RSI indicator as defined by TradingView on March 15, 2021.
            The TradingView code is as follows:
            //@version=4
            study(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, resolution="")
            len = input(14, minval=1, title="Length")
            src = input(close, "Source", type = input.source)
            up = rma(max(change(src), 0), len)
            down = rma(-min(change(src), 0), len)
            rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
            plot(rsi, "RSI", color=#8E1599)
            band1 = hline(70, "Upper Band", color=#C0C0C0)
            band0 = hline(30, "Lower Band", color=#C0C0C0)
            fill(band1, band0, color=#9915FF, transp=90, title="Background")

        :param ohlc:
        :param period:
        :param round_rsi:
        :return: an array with the RSI indicator values
        """

        delta = self.dataset["BC"].diff()

        up = delta.copy()
        up[up < 0] = 0
        up = pd.Series.ewm(up, alpha=1/period).mean()

        down = delta.copy()
        down[down > 0] = 0
        down *= -1
        down = pd.Series.ewm(down, alpha=1/period).mean()

        rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

        return np.round(rsi, 2) if round_rsi else rsi
    # --------------
    
    # Taken from Lukas Zbinden -------
    def stochastic_oscillator(self):
        array_close = np.array(self.dataset['BC'])
        array_open = np.array(self.dataset['BO'])
        array_high = np.array(self.dataset['BH'])
        array_low = np.array(self.dataset['BL'])
        y=0
        z=0
        #kperiods are 14 array start from 0 index
        kperiods=13
        array_highest=[]
        for x in range(0,array_high.size-kperiods):
            z=array_high[y]
            for j in range(0,kperiods):
                if(z<array_high[y+1]):
                    z=array_high[y+1]
                y=y+1
            # creating list highest of k periods
            array_highest.append(z)
            y=y-(kperiods-1)
        #print("Highest array size",len(array_highest))
        #print(array_highest)
        y=0
        z=0
        array_lowest=[]
        for x in range(0,array_low.size-kperiods):
            z=array_low[y]
            for j in range(0,kperiods):
                if(z>array_low[y+1]):
                    z=array_low[y+1]
                y=y+1
            # creating list lowest of k periods
            array_lowest.append(z)
            y=y-(kperiods-1)
        #print(len(array_lowest))
        #print(array_lowest)

        #KDJ (K line, D line, J line)
        Kvalue=[]
        for x in range(kperiods,array_close.size):
            k = ((array_close[x]-array_lowest[x-kperiods])*100/(array_highest[x-kperiods]-array_lowest[x-kperiods]))
            Kvalue.append(k)

        y=0
        # dperiods for calculate d values
        dperiods=3
        Dvalue=[None,None]
        mean=0
        for x in range(0,len(Kvalue)-dperiods+1):
            sum=0
            for j in range(0,dperiods):
                sum=Kvalue[y]+sum
                y=y+1
            mean=sum/dperiods
            # d values for %d line
            Dvalue.append(mean)
            y=y-(dperiods-1)

        return (Kvalue, Dvalue)
    # --------------

    def make_analysis_dataframe(self):

        average_directional_index = np.array(self.adx()[0][14:])
        updi = np.array(self.adx()[1][13:])
        downdi = np.array(self.adx()[2][13:])

        arron_up = np.array(self.aroon()[0][14:])
        arron_down = np.array(self.aroon()[1][14:])

        rsi = np.array(self.relative_strength_index()[14:])

        k_line = np.array(self.stochastic_oscillator()[0][1:])
        d_line = np.array(self.stochastic_oscillator()[1][1:])

        technical_analyis_data = {'adx': average_directional_index, 
                                    'aroon_up': arron_up,
                                    'aroon_down': arron_down, 
                                    'RSI': rsi, 
                                    'K_line': k_line, 
                                    'D_line': d_line, 
                                    'plus_di': updi, 
                                    'negative_di': downdi}

        technical_dataframe = pd.DataFrame(data=technical_analyis_data)

        return technical_dataframe


class indicators():

    def __init__(self):
        self.buy_or_sell = False


    def enter_new_data(self, directional_index, adx_indicator, aroon, stochastic_oscilator, RSI):
        self.directional_index = directional_index
        self.adx_indicator = adx_indicator
        self.aroon = aroon
        self.stochastic_oscilator = stochastic_oscilator
        self.RSI = RSI
        self.indication = {}


    def RSI_signal(self):

        if self.RSI < 30:
            self.indication["RSI"] = 1
        elif self.RSI > 70:
            self.indication["RSI"] = -1
        else:
            self.indication["RSI"] = 0


    def aroon_signal(self):

        aroon_up = self.aroon[:,0]
        aroon_down = self.aroon[:,1]
        if aroon_up[0] < aroon_down[0] and aroon_up[1] > aroon_down[1]:
            self.indication["Aroon"] = 1
        elif aroon_up[0] > aroon_down[0] and aroon_up[1] < aroon_down[1]:
            self.indication["Aroon"] = -1
        else:
            self.indication["Aroon"] = 0


    def average_directional_index_signal(self):

        di_plus = self.directional_index[:,0]
        di_negative = self.directional_index[:,1]

        if di_plus[0] < di_negative[0] and di_plus[1] > di_negative[1] and self.adx_indicator > 20:
            self.indication["ADX"] = 1
        elif di_plus[0] > di_negative[0] and di_plus[1] < di_negative[1] and self.adx_indicator > 20:
            self.indication["ADX"] = -1
        else:
            self.indication["ADX"] = 0


    def stochastic_oscillator_indactor(self):

        K_line = self.stochastic_oscilator[0]
        D_line = self.stochastic_oscilator[1]

        if K_line and D_line < 25:
            self.indication["Stochastic"] = 1

        elif K_line and D_line  > 80:
            self.indication["Stochastic"] = -1

        else:
            self.indication["Stochastic"] = 0


    def get_trade_action(self, threshold_buy, threshold_sell):

        self.RSI_signal()
        self.aroon_signal()
        self.average_directional_index_signal()
        self.stochastic_oscillator_indactor()


        if np.sum(list(self.indication.values())) >= threshold_buy and self.buy_or_sell == False:

            # fig.add_vline(x=i, line_width=3, line_dash="dash", line_color="green")

            self.buy_or_sell = True

            return "Buy!"


        elif np.sum(list(self.indication.values())) <= threshold_sell and self.buy_or_sell == True:

            # fig.add_vline(x=i, line_width=3, line_dash="dash", line_color="red")


            self.buy_or_sell = False

            return "Sell!"
        

        return "Remain!"


def main():

    data_info = data_information()
    market_entry = indicators()
    market_buy_test = Oanda_API()
    dataset = market_buy_test.fetch_candlesticks('EUR_USD', '100', 'H1')
    data_info.change_dataset(dataset)
    #data_info.create_graph()

    #for i in range(1, len(dataset) - 14, 1):
    dataset = market_buy_test.fetch_candlesticks('EUR_USD', '100', 'H1')

    data_info.change_dataset(dataset)

    technical_dataframe = data_info.make_analysis_dataframe()

    market_entry.enter_new_data(
        directional_index = technical_dataframe[["plus_di", "negative_di"]].to_numpy()[-2:],
        adx_indicator = technical_dataframe.adx.to_numpy()[-1],
        aroon = technical_dataframe[["aroon_up", "aroon_down"]].to_numpy()[-2:],
        stochastic_oscilator = technical_dataframe[["K_line", "D_line"]].to_numpy()[-1],
        RSI = technical_dataframe.RSI.to_numpy()[-1]
        )
    
    buy_or_sell = market_entry.get_trade_action(2, -2)

    if buy_or_sell == "Buy!":

        _, trade_id = market_buy_test.place_trade("100")

        if defs.ORDERCANCELLATION in list(trade_id.keys()):
            print("Sorry! Order Got Cancelled Due To " + trade_id[defs.ORDERCANCELLATION]['reason'])

        #data_info.add_indicator(i, "green")

        trade_id = trade_id['orderCreateTransaction']["id"]

    elif buy_or_sell == "Sell!":

        #data_info.add_indicator(i, "red")

        market_buy_test.close_trade(trade_id)

        if defs.ORDERCANCELLATION in list(trade_id.keys()):
            print("Sorry! Order Got Cancelled Due To " + trade_id[defs.ORDERCANCELLATION]['reason'])

    print(buy_or_sell)
    return buy_or_sell

    #data_info.fig.show()
    #print(buy_or_sell)

"""
def stochastic_oscillator(dataset):
    array_close = np.array(dataset['BC'])
    array_open = np.array(dataset['BO'])
    array_high = np.array(dataset['BH'])
    array_low = np.array(dataset['BL'])

    # Calculate array_highest using numpy maximum.reduceat
    idx = np.arange(array_high.size)
    array_highest = np.maximum.reduceat(array_high, idx[:-13], axis=0)[13:]

    # Calculate array_lowest using numpy minimum.reduceat
    array_lowest = np.minimum.reduceat(array_low, idx[:-13], axis=0)[13:]

    print(array_lowest)

    # KDJ (K line, D line, J line)
    Kvalue = ((array_close[13:] - array_lowest) * 100 / (array_highest - array_lowest))

    # dperiods for calculate d values
    dperiods = 3
    # Use numpy cumsum to calculate the sum efficiently
    cumsum_Kvalue = np.cumsum(Kvalue)
    Dvalue = np.concatenate([np.full(dperiods - 1, None), (cumsum_Kvalue[dperiods - 1:] - cumsum_Kvalue[:-dperiods + 1]) / dperiods])

    return Kvalue, Dvalue

"""

def princetrading(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    main()

if __name__ == "__main__":


    main()

    
    #dataset = pd.read_csv("zfile_to_be_stored/eurusd_hour.csv")
    """
    current_forex_info = alpha_vantage_API()
    data_info = data_information()
    market_entry = indicators()
    market_buy_test = Oanda_API()
    current_forex_info.get_current_info()
    dataset = current_forex_info.get_current_formated_data()"""

    #print(dataset.BC.to_numpy())




