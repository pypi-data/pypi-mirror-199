""" List of all the types used"""
from typing import Dict
from typing import List
from typing import no_type_check

from gwproto.types import GtDispatchBoolean_Maker
from gwproto.types import GtDispatchBooleanLocal_Maker
from gwproto.types import GtDriverBooleanactuatorCmd_Maker
from gwproto.types import GtShBooleanactuatorCmdStatus_Maker
from gwproto.types import GtShCliAtnCmd_Maker
from gwproto.types import GtShMultipurposeTelemetryStatus_Maker
from gwproto.types import GtShSimpleTelemetryStatus_Maker
from gwproto.types import GtShStatus_Maker
from gwproto.types import GtShTelemetryFromMultipurposeSensor_Maker
from gwproto.types import GtTelemetry_Maker
from gwproto.types import HeartbeatB_Maker
from gwproto.types import SnapshotSpaceheat_Maker
from gwproto.types import TelemetrySnapshotSpaceheat_Maker


TypeMakerByName: Dict[str, HeartbeatB_Maker] = {}


@no_type_check
def type_makers() -> List[HeartbeatB_Maker]:
    return [
        GtDispatchBoolean_Maker,
        GtDispatchBooleanLocal_Maker,
        GtDriverBooleanactuatorCmd_Maker,
        GtShBooleanactuatorCmdStatus_Maker,
        GtShCliAtnCmd_Maker,
        GtShMultipurposeTelemetryStatus_Maker,
        GtShSimpleTelemetryStatus_Maker,
        GtShStatus_Maker,
        GtShTelemetryFromMultipurposeSensor_Maker,
        GtTelemetry_Maker,
        HeartbeatB_Maker,
        SnapshotSpaceheat_Maker,
        TelemetrySnapshotSpaceheat_Maker,
    ]


for maker in type_makers():
    TypeMakerByName[maker.type_name] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "gt.dispatch.boolean": "110",
        "gt.dispatch.boolean.local": "110",
        "gt.driver.booleanactuator.cmd": "100",
        "gt.sh.booleanactuator.cmd.status": "100",
        "gt.sh.cli.atn.cmd": "110",
        "gt.sh.multipurpose.telemetry.status": "100",
        "gt.sh.simple.telemetry.status": "100",
        "gt.sh.status": "110",
        "gt.sh.telemetry.from.multipurpose.sensor": "100",
        "gt.telemetry": "110",
        "heartbeat.b": "001",
        "snapshot.spaceheat": "000",
        "telemetry.snapshot.spaceheat": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "gt.dispatch.boolean.110": "Active",
        "gt.dispatch.boolean.local.110": "Active",
        "gt.driver.booleanactuator.cmd.100": "Active",
        "gt.sh.booleanactuator.cmd.status.100": "Active",
        "gt.sh.cli.atn.cmd.110": "Active",
        "gt.sh.multipurpose.telemetry.status.100": "Active",
        "gt.sh.simple.telemetry.status.100": "Active",
        "gt.sh.status.110": "Active",
        "gt.sh.telemetry.from.multipurpose.sensor.100": "Active",
        "gt.telemetry.110": "Active",
        "heartbeat.b.001": "Active",
        "snapshot.spaceheat.000": "Active",
        "telemetry.snapshot.spaceheat.000": "Active",
    }

    return v
