from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class TelemetryName(StrEnum):
    """
    Specifies the name of sensed data reported by a Spaceheat SCADA. [More Info](https://gridworks-protocol.readthedocs.io/en/latest/telemetry-name.html).

    Choices and descriptions:
    
      * Unknown: Default Value - unknown telemetry name
      * PowerW: Power in Watts
      * RelayState: State of a Relay. 0 means open, 1 means closed
      * WaterTempCTimes1000: Water temperature, in Degrees Celcius multiplied by 1000. So 43200 means 43.2 deg C
      * WaterTempFTimes1000: Water temperature, in Degrees F multiplied by 1000. So 142100 means 142.1 deg F
      * GpmTimes100: Gallons Per Minute multiplied by 100. So 433 means 4.33 gallons per minute.
      * CurrentRmsMicroAmps: Current measurement in Root Mean Square MicroAmps
      * GallonsTimes100: Gallons multipled by 100
      * VoltageRmsMilliVolts: Voltage in Root Mean Square MilliVolts
      * MilliWattHours: Energy in MilliWattHours.
      * FrequencyMicroHz: Frequency in MicroHz
      * AirTempCTimes1000: Air temperature, in Degrees Celsius multiplied by 1000.
      * AirTempFTimes1000: Air temperature, in Degrees F multiplied by 1000.
    """
    Unknown = auto()
    PowerW = auto()
    MilliWattHours = auto()
    FrequencyMicroHz = auto()
    AirTempCTimes1000 = auto()
    AirTempFTimes1000 = auto()
    RelayState = auto()
    WaterTempCTimes1000 = auto()
    WaterTempFTimes1000 = auto()
    GpmTimes100 = auto()
    CurrentRmsMicroAmps = auto()
    GallonsTimes100 = auto()
    VoltageRmsMilliVolts = auto()
    
    @classmethod
    def default(cls) -> "TelemetryName":
        """
        Returns default value Unknown
        """
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]
