#!/usr/bin/env python
import sys
import datetime
import backtrader as bt

cerebro = bt.Cerebro()
data = bt.feeds.GenericCSVData(
	dataname = sys.argv[1],
	dtformat='%Y-%m-%d %H:%M:%S.%f',
	timeframe=bt.TimeFrame.Ticks,
	open=1,
	high=1,
	low=1,
	close=1,
	volume=-1,
	openinterest=-1
)
data = cerebro.resampledata(data,
    timeframe=bt.TimeFrame.Minutes)
cerebro.adddata(data)
cerebro.broker.setcash(10000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
