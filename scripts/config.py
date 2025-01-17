import os
import time
import argparse
from typing import Optional
from build_path import buildPath
from build_data_filename import buildDataFilename
from get_epoch_ms import getEpochMS
from yyyymmdd import getYYYYMMDD
from load_toml import loadToml

class Config:
  def __init__(self, program: Optional[str] = None, desc: Optional[str] = None):
    self.parser = argparse.ArgumentParser(prog=program, description=desc)
    # self.parser.add_argument("-d", "--eventDate")
    self.parser.add_argument("eventDate")
    self.parser.add_argument("-p", "--sourcePath")
    self.parser.add_argument("-l", "--lineItems")
    self.parser.add_argument("-o", "--orders")
    self.parsed_args = self.parser.parse_args()
    self.dict_args = vars(self.parsed_args)
    self.eventDate = self.dict_args["eventDate"]
  
  def getArgs(self, argName: Optional[str] = None):
    if (argName is None):
      return self.dict_args

    return self.dict_args[argName]
  
  def load(self, configFile: Optional[str] = None, verify: Optional[bool] = True):
    messages: list[str] = []

    filepath = configFile
    if (filepath is None):
      # use default config file path
      filepath = buildPath(os.path.dirname(os.path.realpath(__file__)), "config.toml")
    
    # load config; abort if no config file is found
    try:
      self.configFile = loadToml(filepath)
    except FileNotFoundError:
      raise FileNotFoundError(f"Unable to locate config file at \"{filepath}\"")
    
    # load defaults for required keys
    self.defaultLineItemsFilename = "line_items_[[YYYYMMDD]].csv"
    self.defaultOrdersFilename = "orders_[[YYYYMMDD]].csv"
    self.defaultSalesDataFilename = "[[YYYYMMDD]]_sales_data_[[ts]].csv"
    
    # assign values from config file to required keys
    try:
      self.defaultLineItemsFilename = self.configFile["filenames"]["lineItems"]
    except KeyError:
      messages.append(f"Missing key \"filenames/lineItems\" in config file. Using default value. ({self.defaultLineItemsFilename})")
      
    try:
      self.defaultOrdersFilename = self.configFile["filenames"]["orders"]
    except KeyError:
      messages.append(f"Missing key \"filenames/orders\" in config file. Using default value. ({self.defaultOrdersFilename})")
      
    try:
      self.defaultSalesDataFilename = self.configFile["filenames"]["salesData"]
    except KeyError:
      messages.append(f"Missing key \"filenames/salesData\" in config file. Using default value. ({self.defaultSalesDataFilename})")
    
    self.sourcePath = self.dict_args["sourcePath"]
    self.lineItems = self.dict_args["lineItems"]
    self.orders = self.dict_args["orders"]
    
    # use eventDate to generate a date stamp
    try:
      self.datestamp = getYYYYMMDD(self.eventDate)
    except ValueError: # BAD DATE
      raise ValueError(f"Invalid date or date format \"{self.eventDate}\"")
    except Exception:  # UNKNOWN ERROR
      raise Exception(f"Unable to create datestamp from \"{self.eventDate}\"")
    
    # make sure we have both lineItems and orders or sourcePath
    if (self.lineItems is None or self.orders is None):
      if (self.sourcePath is None):
        raise KeyError("Either --sourcePath or both --lineItems path and --orders path is required")
    
    # if lineItems is None then build from sourcePath
    if self.lineItems is None:
      self.lineItems = buildPath(self.sourcePath, buildDataFilename(self.defaultLineItemsFilename, self.datestamp))
    
    # if orders is None then build from sourcePath
    if self.orders is None:
      self.orders = buildPath(self.sourcePath, buildDataFilename(self.defaultOrdersFilename, self.datestamp))

    # verify we can find the files
    if not os.path.isfile(self.lineItems):
      raise FileNotFoundError(f"Unable to find file \"{self.lineItems}\"")
    
    if not os.path.isfile(self.orders):
      raise FileNotFoundError(f"Unable to find file \"{self.orders}\"")

    # set the expected output sales data file path
    if self.sourcePath is None:
      self.salesDataFile = buildPath("./", buildDataFilename(self.defaultSalesDataFilename, self.datestamp))
    else:
      self.salesDataFile = buildPath(self.sourcePath, buildDataFilename(self.defaultSalesDataFilename, self.datestamp, str(getEpochMS(time.time()))))

    return messages
  
  def report(self):
    print("CONFIG:")
    print(f"  eventDate:      {self.eventDate}")
    print(f"  lineItems:      {self.lineItems}")
    print(f"  orders:         {self.orders}")
    print(f"  sourcePath:     {self.sourcePath}")
    print(f"  salesDataFile:  {self.salesDataFile}")
    print("  ")
