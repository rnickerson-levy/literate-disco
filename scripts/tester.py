import os
from config import Config
from build_path import buildPath
from logger import Logger
from typing import Optional
from get_epoch_ms import getEpochMS
import time

lgr = Logger()

ts = time.time()
lgr.p(ts)
lgr.p(getEpochMS(ts))

scriptPath = os.path.dirname(os.path.realpath(__file__))
cfgPath = buildPath(os.path.dirname(os.path.realpath(__file__)), "config.toml")

def reportWarnings(warnings: list[str], logger: Optional[Logger] = None):
  if len(warnings) > 0:
    for warning in warnings:
      if logger is not None:
        logger.p(f"WARNING: {warning}")
      else:
        print(f"WARNING: {warning}")

cfg = Config()

lgr.p(f"timestamp: {int(time.time())}")

try:
  reportWarnings(cfg.load(cfgPath))
  # if len(warnings) > 0:
  #   lgr.p("WARNINGS:")
  #   for warning in warnings:
  #     lgr.p(f"  -{warning}")
# except FileNotFoundError as err:
#   lgr.p(f"ERROR: [FileNotFoundError] {str(err)}")
# except KeyError as err:
#   lgr.p(f"ERROR: {str(err)}")
# except ValueError as err:
#   lgr.p(f"ERROR: {str(err)}")
except Exception as err:
  lgr.p(f"ERROR: {str(err)}")


cfg.report()

# import tomllib
# from build_path import buildPath
# from load_toml import loadToml
  
# config = loadToml(buildPath(os.path.dirname(os.path.realpath(__file__)), "config.toml"))

# print(config["filenames"]["lineItems"])
# print(config["filenames"]["orders"])
# print(config["filenames"]["salesData"])
# print(config["filenamess"]["salesData"])




# import argparse
# from cl_args import CLArgs

# parser = argparse.ArgumentParser()
# parser.add_argument('--foo', type=str)
# parser.add_argument('--bar', type=int)

# cla = CLArgs()

# print(cla.getArgs("foo"))
# i = cla.getArgs("bar")
# print(i + 2)
# print(cla.getArgs())
# cla.report()







# from datetime import datetime
# from yyyymmdd import getYYYYMMDD

# def getYYYYMMDD(dateString):
#   for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y"):
#     try:
#       dt = datetime.strptime(dateString, fmt)
#       return f"{dt.year}{str(dt.month).rjust(2, "0")}{str(dt.day).rjust(2, "0")}"
#     except ValueError:
#       pass
#   raise ValueError('no valid date format found')

# print(getYYYYMMDD("1/10/2024"))


# import os

# fp1 = os.getcwd()
# fp2 = os.path.realpath(__file__)
# print(fp1)
# print(fp2)

# import datetime
# import dateutil.parser # type: ignore

# d1 = dateutil.parser.parse("2024-11-14")
# d2 = dateutil.parser.parse("2024-11-15 09:58:53")

# print(d1)
# print(d2)

# 2024-11-15 09:58:53
# date_string = "2024-11-15 09:58:53"
# format_string = "%Y-%m-%d %H:%M:%S"
# datee = datetime.strptime(date_string, format_string)
# print(datee)
# print(datee.day)


# def isOnDate(targetDateString, datetimeString):
#   targetDate = "%m-%d-%Y"

# from line_items import LineItems

# lineItems = LineItems("./data/items.csv")
# lineItems.load()
# print(len(lineItems.getRawData()))
# lineItems.filter()
# print(len(lineItems.getFilteredData()))

# def isSameDay(date1, date2):
#   if not isinstance(date1, datetime.date) or not isinstance(date2, datetime.date):
#     raise ValueError("Value is not a date")
  
#   if not date1.month == date2.month:
#     return False
  
#   if not date1.day == date2.day:
#     return False
  
#   if not date1.year == date2.year:
#     return False
  
#   return True

# print(isSameDay(d1, d2))
