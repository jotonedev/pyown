"""Typed events and parser for energy management (WHO=18)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Iterable

from ...events import Event, parser
from ...messages import BaseMessage, DimensionResponse
from ...tags import Who
from ..base import BaseItem
from .dataclass import ActuatorStatus, StopGoStatus
from .energy import EnergyManagement
from .enums import DimensionEnergy

__all__ = [
    "EnergyActivePowerEvent",
    "EnergyUnitTotalizerEvent",
    "EnergyUnitPerMonthEvent",
    "EnergyPartialTotalizerCurrentMonthEvent",
    "EnergyPartialTotalizerCurrentDayEvent",
    "EnergyActuatorsInfoEvent",
    "EnergyTotalizerEvent",
    "EnergyDifferentialCurrentLevelEvent",
    "EnergyStopGoStatusEvent",
    "EnergyDailyTotalizersHourlyEvent",
    "EnergyMonthlyAverageHourlyEvent",
    "EnergyMonthlyTotalizersCurrentYearEvent",
    "EnergyMonthlyTotalizersLastYearEvent",
]


@dataclass(frozen=True, slots=True)
class EnergyActivePowerEvent(Event):
    """Active power reading (dimension 113)."""

    power: float


@dataclass(frozen=True, slots=True)
class EnergyUnitTotalizerEvent(Event):
    """Energy/unit totalizer (dimension 51)."""

    energy: float


@dataclass(frozen=True, slots=True)
class EnergyUnitPerMonthEvent(Event):
    """Energy/unit per month (dimension 52)."""

    month: int
    year: int
    energy: float


@dataclass(frozen=True, slots=True)
class EnergyPartialTotalizerCurrentMonthEvent(Event):
    """Partial totalizer for the current month (dimension 53)."""

    energy: float


@dataclass(frozen=True, slots=True)
class EnergyPartialTotalizerCurrentDayEvent(Event):
    """Partial totalizer for the current day (dimension 54)."""

    energy: float


@dataclass(frozen=True, slots=True)
class EnergyActuatorsInfoEvent(Event):
    """Actuator state snapshot (dimension 71)."""

    status: ActuatorStatus


@dataclass(frozen=True, slots=True)
class EnergyTotalizerEvent(Event):
    """Totalizer since reset (dimension 72)."""

    totalizer: int
    last_reset: datetime
    energy: float


@dataclass(frozen=True, slots=True)
class EnergyDifferentialCurrentLevelEvent(Event):
    """Differential current level (dimension 73)."""

    level: int


@dataclass(frozen=True, slots=True)
class EnergyStopGoStatusEvent(Event):
    """Stop&Go general status snapshot (dimension 250).

    The status is parsed from the 13-character bitfield string carried in
    DimensionResponse value 0.
    """

    status: StopGoStatus


@dataclass(frozen=True, slots=True)
class EnergyDailyTotalizersHourlyEvent(Event):
    """Daily totalizers on an hourly basis for 16-bit Daily graphics (dimension 511)."""

    month: int
    hour: int
    energy: float


@dataclass(frozen=True, slots=True)
class EnergyMonthlyAverageHourlyEvent(Event):
    """Monthly average on an hourly basis for 16-bit Media Daily graphics (dimension 512)."""

    month: int
    hour: int
    energy: float


@dataclass(frozen=True, slots=True)
class EnergyMonthlyTotalizersCurrentYearEvent(Event):
    """Monthly totalizers current year on a daily basis for 32-bit Monthly graphics (dimension 513)."""

    month: int
    day: int
    energy: float


@dataclass(frozen=True, slots=True)
class EnergyMonthlyTotalizersLastYearEvent(Event):
    """Monthly totalizers last year on a daily basis for 32-bit graphics (dimension 514)."""

    month: int
    day: int
    energy: float


def _decode_stop_go_general(message: DimensionResponse) -> StopGoStatus:
    s = message.values[0].string
    return StopGoStatus(
        open=bool(int(s[0])),
        failure=bool(int(s[1])),
        block=bool(int(s[2])),
        open_cc=bool(int(s[3])),
        open_ground_fault=bool(int(s[4])),
        open_vmax=bool(int(s[5])),
        self_test_off=bool(int(s[6])),
        auto_reset_off=bool(int(s[7])),
        check_off=bool(int(s[8])),
        waiting_closing=bool(int(s[9])),
        first_24h_open=bool(int(s[10])),
        power_fail_down=bool(int(s[11])),
        power_fail_up=bool(int(s[12])),
    )


HandlerFn = Callable[[BaseItem, DimensionResponse], Event]


_DISPATCH: dict[str, HandlerFn] = {
    DimensionEnergy.ACTIVE_POWER.value: lambda i, m: EnergyActivePowerEvent(
        i, i.where, power=float(m.values[0].string)
    ),
    DimensionEnergy.ENERGY_UNIT_TOTALIZER.value: lambda i, m: EnergyUnitTotalizerEvent(
        i, i.where, energy=float(m.values[0].string)
    ),
    DimensionEnergy.ENERGY_UNIT_PER_MONTH.value: lambda i, m: EnergyUnitPerMonthEvent(
        i, i.where,
        month=int(m.dimension.parameters[1]),
        year=int(m.dimension.parameters[0]),
        energy=float(m.values[0].string),
    ),
    DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_MONTH.value: lambda i, m: (
        EnergyPartialTotalizerCurrentMonthEvent(i, i.where, energy=float(m.values[0].string))
    ),
    DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_DAY.value: lambda i, m: (
        EnergyPartialTotalizerCurrentDayEvent(i, i.where, energy=float(m.values[0].string))
    ),
    DimensionEnergy.ACTUATORS_INFO.value: lambda i, m: EnergyActuatorsInfoEvent(
        i, i.where, status=EnergyManagement._decode_actuators_info(m)
    ),
    DimensionEnergy.TOTALIZERS.value: lambda i, m: _build_totalizer_event(i, m),
    DimensionEnergy.DIFFERENTIAL_CURRENT_LEVEL.value: lambda i, m: (
        EnergyDifferentialCurrentLevelEvent(i, i.where, level=int(m.values[0].string))
    ),
    DimensionEnergy.STATUS_STOP_GO_GENERAL.value: lambda i, m: EnergyStopGoStatusEvent(
        i, i.where, status=_decode_stop_go_general(m)
    ),
    DimensionEnergy.DAILY_TOTALIZERS_HOURLY_16BIT.value: lambda i, m: (
        EnergyDailyTotalizersHourlyEvent(
            i, i.where,
            month=int(m.dimension.parameters[0]),
            hour=int(m.values[0].string),
            energy=float(m.values[1].string),
        )
    ),
    DimensionEnergy.MONTHLY_AVERAGE_HOURLY_16BIT.value: lambda i, m: (
        EnergyMonthlyAverageHourlyEvent(
            i, i.where,
            month=int(m.dimension.parameters[0]),
            hour=int(m.values[0].string),
            energy=float(m.values[1].string),
        )
    ),
    DimensionEnergy.MONTHLY_TOTALIZERS_CURRENT_YEAR_32BIT.value: lambda i, m: (
        EnergyMonthlyTotalizersCurrentYearEvent(
            i, i.where,
            month=int(m.dimension.parameters[0]),
            day=int(m.values[0].string),
            energy=float(m.values[1].string),
        )
    ),
    DimensionEnergy.MONTHLY_TOTALIZERS_LAST_YEAR_32BIT.value: lambda i, m: (
        EnergyMonthlyTotalizersLastYearEvent(
            i, i.where,
            month=int(m.dimension.parameters[0]),
            day=int(m.values[0].string),
            energy=float(m.values[1].string),
        )
    ),
}


def _build_totalizer_event(i: BaseItem, m: DimensionResponse) -> EnergyTotalizerEvent:
    tot_n = int(m.dimension.parameters[0])
    last_reset, energy = EnergyManagement._decode_totalizers(m)
    return EnergyTotalizerEvent(
        i, i.where, totalizer=tot_n, last_reset=last_reset, energy=energy
    )


@parser(Who.ENERGY_MANAGEMENT)
def parse_energy(item: BaseItem, message: BaseMessage) -> Iterable[Event]:
    if not isinstance(message, DimensionResponse):
        return
    builder = _DISPATCH.get(message.dimension.tag)
    if builder is None:
        return
    yield builder(item, message)
