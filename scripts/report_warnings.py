from logger import Logger
from typing import Optional

def reportWarnings(warnings: list[str], logger: Optional[Logger] = None):
  if len(warnings) > 0:
    for warning in warnings:
      if logger is not None:
        logger.p(f"WARNING: {warning}")
      else:
        print(f"WARNING: {warning}")
