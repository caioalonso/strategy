import datetime
import backtrader as bt


class TestStrategy(bt.Strategy):
    params = (
        ('sma1', 7),
        ('sma2', 26),
        ('ema', 50),
        ('printlog', False)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma1 = bt.indicators.SMA(self.datas[0], period=self.params.sma1)
        self.sma2 = bt.indicators.SMA(self.datas[0], period=self.params.sma2)
        self.ema  = bt.indicators.EMA(self.datas[0], period=self.params.ema)
        self.buysig = bt.And(self.sma1 > self.sma2, self.sma1 > self.ema)

    def next(self):
        if self.order:
            return
        if not self.position:
            if not self.buysig[-1] and self.buysig[0]:
                close = self.dataclose[0]
                sl = close - 0.0010
                tp = close + 0.0020
                self.order = self.buy_bracket(stopprice=sl, limitprice=tp)
                self.log('BUY CREATE, %.5f' % self.dataclose[0])

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log('Order Canceled or Client-side SL/TP')
        elif order.status in [order.Margin, order.Rejected]:
            self.log('Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.5f, NET %.5f' %
                 (trade.pnl, trade.pnlcomm))

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.datetime()
            print('%s, %s' % (dt.isoformat(), txt))
