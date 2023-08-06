from .GcodeFile import GcodeFile
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class Job(BaseModel): 
  file: Optional[GcodeFile] = Field()
  estimatedPrintTime: Optional[str] = Field()
  lastPrintTime: Optional[str] = Field()
  filamentLength: Optional[str] = Field()
  filamentVolume: Optional[str] = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return Job(**json.loads(json_string))
