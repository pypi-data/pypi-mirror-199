from .PrinterStatus import PrinterStatus
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class PrinterStatusChanged(BaseModel): 
  status: PrinterStatus = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return PrinterStatusChanged(**json.loads(json_string))
