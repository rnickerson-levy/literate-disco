# import os
import sys
import argparse
import tomllib
import os.path
import pandas as pd # type: ignore
from logger import Logger
from line_items import LineItems
from orders import Orders
from epoch_time import getEpochTime
from yyyymmdd import getYYYYMMDD

def stop():
  print("")
  sys.exit("Script halted")

# just a blank line to separate the logger output from the command line
print("")

# LOAD CONFIG
scriptPath = os.path.dirname(os.path.realpath(__file__))
# configFilePath = f"{scriptPath}\\config.toml"
with open(f"{scriptPath}\\config.toml", "rb") as f:
  config = tomllib.load(f)

# CREATE LOGGER
logger = Logger()

# PARSE CMDLINE ARGS
parser = argparse.ArgumentParser(prog="Invoice Data", description="Generate sales data grouped by location")
parser.add_argument("-d", "--eventDate")
parser.add_argument("-s", "--sourcePath")
args = parser.parse_args()

# ASSIGN ARGS TO VARIABLES
eventDate = args.eventDate
sourcePath = args.sourcePath

logger.p(f"eventDate = {eventDate}")
logger.p(f"sourcePath = {sourcePath}")

# VERIFY EVENT DATE
if (eventDate is None):
  logger.p("Missing required argument: eventDate")
  stop()

try:
  datestamp = getYYYYMMDD(eventDate)
except ValueError:
  logger.p(f"Invalid date or date format \"{eventDate}\"")
  stop()

# VERIFY SOURCE PATH
if (sourcePath is None):
  logger.p("Missing required argument: sourcePath")
  stop()

# VERIFY EXPECTED FILES EXIST IN PATH
print(f"sourcePath = {sourcePath}")

sys.exit("TEST HALT")



# LINE ITEMS
lineItems = LineItems("./data/line_items_20241116.csv", logger)
lineItems.load()
filteredData = lineItems.filter()
buckets = lineItems.bucket()
validUuids = lineItems.createValidUuids()

# ORDERS
orders = Orders("./data/orders_20241116.csv", logger)
orders.load()
tipsBuckets = orders.bucket(validUuids)

# ADD TIPS
withTips = lineItems.addTips(tipsBuckets)

# VERIFY BUCKET COUNTS
if len(buckets) != len(tipsBuckets):
  logger.p( "WARNING: Sales buckets count does not match tips bucket counts")
  logger.p(f"--> sales buckets: {len(buckets)}, tips buckets: {len(tipsBuckets)}")

# SAVE TO CSV
outputFile = str(config["filenames"]["output"]).replace("[[YYYYMMDD]]", datestamp).replace("[[ts]]", getEpochTime())
logger.p(f"Saving invoice data to \"{outputFile}\"")
df = pd.DataFrame(list(withTips.values()))
df.to_csv(outputFile, index = False)
logger.p("Done")

# fp1 = os.getcwd()
# fp2 = os.path.realpath(__file__)
# print(fp1)
# print(fp2)
