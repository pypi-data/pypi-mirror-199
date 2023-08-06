from abc import ABC
from typing import Dict
from typing import List

from gwproto.enums import TelemetryName
from gwproto.errors import MpSchemaError


class SpaceheatTelemetryName100GtEnum(ABC):
    symbols: List[str] = [
        "00000000",
        "af39eec9",
        "5a71d4b3",
        "c89d0ba1",
        "793505aa",
        "d70cce28",
        "ad19e79c",
        "329a68c0",
        "bb6fdd59",
        "e0bb014b",
        "337b8659",
        "0f627faa",
        "4c3f8c78",
    ]


class TelemetryNameGtEnum(SpaceheatTelemetryName100GtEnum):
    @classmethod
    def is_symbol(cls, candidate) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class TelemetryNameMap:
    @classmethod
    def gt_to_local(cls, symbol):
        if not TelemetryNameGtEnum.is_symbol(symbol):
            raise MpSchemaError(
                f"{symbol} must belong to key of {TelemetryNameMap.gt_to_local_dict}"
            )
        return cls.gt_to_local_dict[symbol]

    @classmethod
    def local_to_gt(cls, telemetry_name):
        if not isinstance(telemetry_name, TelemetryName):
            raise MpSchemaError(f"{telemetry_name} must be of type {TelemetryName}")
        return cls.local_to_gt_dict[telemetry_name]

    gt_to_local_dict: Dict[str, TelemetryName] = {
        "00000000": TelemetryName.Unknown,
        "af39eec9": TelemetryName.PowerW,
        "5a71d4b3": TelemetryName.RelayState,
        "c89d0ba1": TelemetryName.WaterTempCTimes1000,
        "793505aa": TelemetryName.WaterTempFTimes1000,
        "d70cce28": TelemetryName.GpmTimes100,
        "ad19e79c": TelemetryName.CurrentRmsMicroAmps,
        "329a68c0": TelemetryName.GallonsTimes100,
        "bb6fdd59": TelemetryName.VoltageRmsMilliVolts,
        "e0bb014b": TelemetryName.MilliWattHours,
        "337b8659": TelemetryName.FrequencyMicroHz,
        "0f627faa": TelemetryName.AirTempCTimes1000,
        "4c3f8c78": TelemetryName.AirTempFTimes1000,
    }

    local_to_gt_dict: Dict[TelemetryName, str] = {
        TelemetryName.Unknown: "00000000",
        TelemetryName.PowerW: "af39eec9",
        TelemetryName.RelayState: "5a71d4b3",
        TelemetryName.WaterTempCTimes1000: "c89d0ba1",
        TelemetryName.WaterTempFTimes1000: "793505aa",
        TelemetryName.GpmTimes100: "d70cce28",
        TelemetryName.CurrentRmsMicroAmps: "ad19e79c",
        TelemetryName.GallonsTimes100: "329a68c0",
        TelemetryName.VoltageRmsMilliVolts: "bb6fdd59",
        TelemetryName.MilliWattHours: "e0bb014b",
        TelemetryName.FrequencyMicroHz: "337b8659",
        TelemetryName.AirTempCTimes1000: "0f627faa",
        TelemetryName.AirTempFTimes1000: "4c3f8c78",
    }
