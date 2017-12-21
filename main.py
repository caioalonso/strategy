#!/usr/bin/env python
"""FOREX Strategy
Usage:
  main.py FILE
  main.py -h --help
"""
import os
import sys
from docopt import docopt
import backtrader as bt
import strategy


def main(argv):
    arguments = docopt(
        __doc__, argv, help=True, version=None, options_first=False)

    if os.path.isfile(arguments['FILE']) is not True:
        print('File not found')
        return

    cerebro = bt.Cerebro()

    cerebro.addstrategy(strategy.TestStrategy)
    # Load the Data
    data = bt.feeds.GenericCSVData(
        dataname=sys.argv[1],
        dtformat='%Y-%m-%d %H:%M:%S.%f',
        timeframe=bt.TimeFrame.Ticks,
        open=2,
        high=2,
        low=2,
        close=2,
        volume=4,
        openinterest=-1)

    # First add the original data - smaller timeframe
    cerebro.replaydata(data, timeframe=bt.TimeFrame.Minutes, compression=1)

    #cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=False)
    #cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    cerebro.broker.setcommission(commission=0.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    #cerebro.plot()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
