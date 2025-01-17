import sys
import os.path
import pandas as pd # type: ignore
from config import Config
from logger import Logger
from orders import Orders
from line_items import LineItems
from get_epoch_ms import getEpochMS
from report_warnings import reportWarnings

def stop():
  print("")
  sys.exit("Script halted")

# just a blank line to separate the logger output from the command line
print("")

# MARK START TIME
startTime = getEpochMS()

# CREATE LOGGER
logger = Logger()

# LOAD CONFIG
config = Config()
try:
  reportWarnings(config.load(f"{os.path.dirname(os.path.realpath(__file__))}\\config.toml"), logger)
# except FileNotFoundError as err:
#   pass
# except KeyError as err:
#   pass
# except ValueError as err:
#   pass
except Exception as err:
  logger.p(f"ERROR: {str(err)}")
  stop()

# sys.exit("TEST HALT")


# LINE ITEMS
lineItems = LineItems(config.lineItems, logger)
lineItems.load()
filteredData = lineItems.filter()
buckets = lineItems.bucket()
validUuids = lineItems.createValidUuids()

# ORDERS
orders = Orders(config.orders, logger)
orders.load()
tipsBuckets = orders.bucket(validUuids)

# ADD TIPS
withTips = lineItems.addTips(tipsBuckets)

# VERIFY BUCKET COUNTS
if len(buckets) != len(tipsBuckets):
  logger.p(f"WARNING: Sales buckets count does not match tips bucket counts. sales buckets: {len(buckets)}, tips buckets: {len(tipsBuckets)}")

# SAVE TO CSV
outputFile = str(config.salesDataFile)
logger.p(f"Saving invoice data to \"{outputFile}\"")
df = pd.DataFrame(list(withTips.values()))
df.to_csv(outputFile, index = False)

# DONE
logger.p(f"Done. Completed in {(getEpochMS() - startTime)}ms.")

# fp1 = os.getcwd()
# fp2 = os.path.realpath(__file__)
# print(fp1)
# print(fp2)
