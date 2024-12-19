import pandas # type: ignore
from convert_to_float import convertToFloat

class Orders:
  __useCols = [
    "revenue_center",
    "order_uuid",
    "tip",
  ]
  
  __datatypes = {
    "revenue_center": "str",
    "order_uuid": "str",
    "tip": "float",
  }
  
  def __init__(self, filePath, report = None):
    self.filePath = filePath
    self.rawData = None
    self.filteredData = None
    self.bucketedData = None
    self.report = report

  def getRawData(self):
    return self.rawData
  
  def filteredData(self):
    return self.filteredData
  
  def bucketedData(self):
    return self.bucketedData

  def load(self):
    if self.report:
      self.report.p(f"Loading orders from {self.filePath}")

    data = pandas.read_csv(self.filePath, dtype = self.__datatypes, usecols=self.__useCols, keep_default_na=False)
    self.rawData = data.to_dict("records")
    
    if self.report:
      self.report.p(f"Loaded {len(self.rawData):,} records from {self.filePath}")
    
    return self.rawData
  
  def filter(self, validUuids):
    """
    The above function filters orders based on a provided list of valid UUIDs.
    
    :param validUuids: A list of valid UUIDs that will be used to filter the data
    """
    if self.rawData is None:
      raise TypeError("Loaded data is None")
    
    # TODO: filter the orders by uuids
  
  
  def bucket(self, validUuids):
    if self.rawData is None:
      raise TypeError("Order data must be loaded before bucketing")
    
    self.bucketedData: dict[str, float] = {}

    if self.report:
      self.report.p("Bucketing tips...")
      
    for row in self.rawData:
      if row["order_uuid"] not in validUuids:
        continue

      locationName = str(row["revenue_center"]).strip()
      tips = convertToFloat(row["tip"])
      
      existing = self.bucketedData.get(locationName, 0)
      
      self.bucketedData[locationName] = existing + tips
    
    if self.report:
      self.report.p(f"Created {len(self.bucketedData.values()):,} tips buckets")

    return self.bucketedData