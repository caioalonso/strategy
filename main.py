#!/usr/bin/env python
"""FOREX Strategy
Usage:
  main.py FILE
  main.py -h --help
"""
from docopt import docopt
import sys
import datetime
import backtrader as bt
import os


def main(argv):
  arguments = docopt(
    __doc__, argv, help=True, version=None, options_first=False)

  if os.path.isfile(arguments['FILE']) is not True:
    print('File not found')
    return

  cerebro = bt.Cerebro()
  data = bt.feeds.GenericCSVData(
    dataname=sys.argv[1],
    dtformat='%Y-%m-%d %H:%M:%S.%f',
    timeframe=bt.TimeFrame.Ticks,
    open=1,
    high=1,
    low=1,
    close=1,
    volume=-1,
    openinterest=-1)
  data = cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes)
  cerebro.adddata(data)
  cerebro.broker.setcash(10000)
  print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
  cerebro.run()
  print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


if __name__ == "__main__":
  try:
    main(sys.argv[1:])
  except KeyboardInterrupt:
    sys.exit(0)
