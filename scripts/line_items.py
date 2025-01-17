import pandas # type: ignore
from convert_to_float import convertToFloat
from calc_sales import getAlcoholSales, getHouseSales, getSubconFoodSales, getSubconBevSales

class LineItems:
  __useCols = [
    "client_created_at",
    "line_item_created_at",
    "order_state",
    "item_name",
    "item_settled_at",
    "item_refunded_at",
    "item_price",
    "promotion_discount",
    "revenue_center",
    "item_quantity",
    "tax_applied",
    "menu_categories",
    "order_uuid",
  ]

  __datatypes = {
    "client_created_at": "str",
    "line_item_created_at": "str",
    "order_state": "str",
    "item_name": "str",
    "item_settled_at": "str",
    "item_refunded_at": "str",
    "item_price": "float",
    "promotion_discount": "float",
    "revenue_center": "str",
    "item_quantity": "float",
    "tax_applied": "float",
    "menu_categories": "str",
    "order_uuid": "str",
  }
  
  invalidOrderStates = [
    "authorization_failed".lower(),
    "submission_falied".lower(), # this _might_ be a data value so keep
    "submission_failed".lower(),
    "submitted".lower(),
    "refund".lower(),
    "refunded".lower(),
    "refund_failed".lower(),
    "cancelled".lower(),
  ]
  
  filterItemNames = [
    "YETI SOUVENIR CUP".lower(),
    "YETI SOUVENIR TUMBLER".lower(),
  ]

  def __init__(self, filePath, report = None):
    self.filePath = filePath
    self.rawData = None
    self.filteredData = None
    self.bucketedData = None
    self.validUuids = None
    # self.bucketedDataWithTips = None
    self.report = report
  
  def getRawData(self):
    return self.rawData
  
  def getFilteredData(self):
    return self.filteredData
  
  def getBucketedData(self):
    return self.bucketedData
  
  def getValidUuids(self):
    return self.validUuids
  
  # def getBucketedDataWithTips(self):
  #   return self.bucketedDataWithTips
  
  def getBucketedDataAsList(self):
    return list(self.bucketedData.values())
  
  # def getBucketedDataWithTipsAsList(self):
  #   return list(self.bucketedDataWithTips.values())
  
  def load(self):
    if self.report:
      self.report.p(f"Loading line items from {self.filePath}")

    data = pandas.read_csv(self.filePath, dtype = self.__datatypes, usecols=self.__useCols, keep_default_na=False)
    self.rawData = data.to_dict("records")
    
    if self.report:
      self.report.p(f"Loaded {len(self.rawData):,} records from {self.filePath}")
    
    return self.rawData
  
  def filter(self):
    if self.rawData is None:
      raise TypeError("Line Items data must be loaded before it can be filtered")
    
    recordsCount = len(self.rawData)
    if self.report:
      self.report.p(f"Filtering {recordsCount:,} records...")
      
    for row in self.rawData:
      if not row.get("client_created_at") and not row.get("line_item_created_at"):
        continue
      
      if row.get("order_state").lower() in self.invalidOrderStates:
        continue
      
      if row.get("item_name").lower() in self.filterItemNames:
        continue
      
      if not row.get("item_settled_at"):
        continue
      
      if row.get("item_refunded_at"):
        continue
      
      # TODO: CHECK DATE?
      #
      
      # promotion_discount is stored as a negative value
      discount = abs(convertToFloat(row.get("promotion_discount")))
      if discount > 0:
        itemPrice = convertToFloat(row.get("item_price"))
        row["item_price"] = convertToFloat(itemPrice - discount)
      
      if self.filteredData is None:
        self.filteredData = []

      self.filteredData.append(row)
    
    if self.report:
      self.report.p(f"Filtered {(recordsCount - len(self.filteredData)):,} records; {len(self.filteredData):,} remaining")
    
    return self.filteredData
  
  def bucket(self):
    if self.filteredData is None:
      raise TypeError("Line Item data must be filtered before bucketing")
    
    self.bucketedData: dict[str, dict] = {}

    if self.report:
      self.report.p("Creating location buckets...")

    for row in self.filteredData:
      locationName = str(row["revenue_center"]).strip()
      menu_categories = row["menu_categories"]
      item_quantity = int(row["item_quantity"])
      item_price = convertToFloat(row["item_price"])
      tax_applied = convertToFloat(row["tax_applied"])
      
      amount = item_price * item_quantity
      alcoholSales = getAlcoholSales(amount, menu_categories)
      subconFoodSales = getSubconFoodSales(amount, menu_categories)
      subconBevSales = getSubconBevSales(amount, menu_categories)
      houseSales = getHouseSales(amount, menu_categories)
      totalSales = sum([alcoholSales, subconFoodSales, subconBevSales, houseSales])
      
      existing = self.bucketedData.get(locationName, {
        "locationName": locationName,
        "alcoholSales": 0,
        "subconFoodSales": 0,
        "subconBevSales": 0,
        "houseSales": 0,
        "totalSales": 0,
        "tax": 0
      })
      
      bucket = {
        "locationName": locationName,
        "alcoholSales": existing["alcoholSales"] + alcoholSales,
        "subconFoodSales": existing["subconFoodSales"] + subconFoodSales,
        "subconBevSales": existing["subconBevSales"] + subconBevSales,
        "houseSales": existing["houseSales"] + houseSales,
        "totalSales": existing["totalSales"] + totalSales,
        "tax": existing["tax"] + tax_applied
      }
      
      self.bucketedData[locationName] = bucket
      
    if self.report:
      self.report.p(f"Created {len(self.bucketedData.values()):,} buckets")

    return self.bucketedData

  def addTips(self, tips):
    if tips is None:
      raise ValueError("Orders cannot be None")
    
    if self.bucketedData is None:
      raise TypeError("Line Item data must be bucketed before tips can be added")
    
    if self.report:
      self.report.p("Adding tips...")
      
    counter = 0
    
    for key in self.bucketedData.keys():
      row = self.bucketedData.get(key)
      row["tips"] = convertToFloat(tips.get(key, 0))
      self.bucketedData[key] = row
      counter += 1
    
    if self.report:
      self.report.p(f"Added tips into {counter:,} buckets")
  
    return self.bucketedData

  def createValidUuids(self):
    if self.filteredData is None:
      raise TypeError("Filtered Line Item data is None")

    self.validUuids = set()
    
    for row in self.filteredData:
      self.validUuids.add(row["order_uuid"])
      
    return self.validUuids