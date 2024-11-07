from asyncio import Task
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, Enum, auto
from typing import Self, AsyncIterator

from ..base import BaseItem, CoroutineCallback
from ...client import BaseClient
from ...exceptions import InvalidTag
from ...messages import BaseMessage, DimensionResponse
from ...tags import Who, What, Where, Dimension, Value

__all__ = [
    "EnergyManagement",
    "DimensionEnergy",
    "WhatEnergy",
    "TypeEnergy",
]


class DimensionEnergy(Dimension, StrEnum):
    """
    Dimension tags for energy management items.
    It is used only internally to send the correct command and parse the event messages.

    Attributes:
        ACTIVE_POWER: Active Power
        END_AUTOMATIC_UPDATE_SIZE: End Automatic Update size
        ENERGY_UNIT_TOTALIZER: Energy/Unit Totalizer
        ENERGY_UNIT_PER_MONTH: Energy/Unit per month
        PARTIAL_TOTALIZER_CURRENT_MONTH: Partial totalizer for current month
        PARTIAL_TOTALIZER_CURRENT_DAY: Partial totalizer for current day
        ACTUATORS_INFO: Actuators info
        TOTALIZERS: Totalizers
        DIFFERENTIAL_CURRENT_LEVEL: Differential current level
        STATUS_STOP_GO_GENERAL: Status Stop&Go (General)
        STATUS_STOP_GO_OPEN_CLOSE: Status Stop&Go (open/close)
        STATUS_STOP_GO_FAILURE_NO_FAILURE: Status Stop&Go (failure/no failure)
        STATUS_STOP_GO_BLOCK_NOT_BLOCK: Status Stop&Go (block/not block)
        STATUS_STOP_GO_OPEN_CC_BETWEEN_N: Status Stop&Go (open for CC between the N/not open for CC between the N)
        STATUS_STOP_GO_OPENED_GROUND_FAULT: Status Stop&Go (opened ground fault/not opened ground fault)
        STATUS_STOP_GO_OPEN_VMAX: Status Stop&Go (open for Vmax/Not open for Vmax)
        STATUS_STOP_GO_SELF_TEST_DISABLED: Status Stop&Go (Self-test disabled/close)
        STATUS_STOP_GO_AUTOMATIC_RESET_OFF: Status Stop&Go (Automatic reset off/close)
        STATUS_STOP_GO_CHECK_OFF: Status Stop&Go (check off/close)
        STATUS_STOP_GO_WAITING_FOR_CLOSING: Status Stop&Go (Waiting for closing/close)
        STATUS_STOP_GO_FIRST_24H_OPENING: Status Stop&Go (First 24 hours of opening/close)
        STATUS_STOP_GO_POWER_FAILURE_DOWNSTREAM: Status Stop&Go (Power failure downstream/close)
        STATUS_STOP_GO_POWER_FAILURE_UPSTREAM: Status Stop&Go (Power failure upstream/close)
        DAILY_TOTALIZERS_HOURLY_16BIT: Daily totalizers on an hourly basis for 16-bit Daily graphics
        MONTHLY_AVERAGE_HOURLY_16BIT: Monthly average on an hourly basis for 16-bit Media Daily graphics
        MONTHLY_TOTALIZERS_CURRENT_YEAR_32BIT: Monthly totalizers current year on a daily basis for
            32-bit Monthly graphics
        MONTHLY_TOTALIZERS_LAST_YEAR_32BIT: Monthly totalizers on a daily basis last year compared to
            32-bit graphics TouchX Previous Year
    """
    ACTIVE_POWER = "113"
    END_AUTOMATIC_UPDATE_SIZE = "1200"
    ENERGY_UNIT_TOTALIZER = "51"
    ENERGY_UNIT_PER_MONTH = "52"
    PARTIAL_TOTALIZER_CURRENT_MONTH = "53"
    PARTIAL_TOTALIZER_CURRENT_DAY = "54"
    ACTUATORS_INFO = "71"
    TOTALIZERS = "72"
    DIFFERENTIAL_CURRENT_LEVEL = "73"
    STATUS_STOP_GO_GENERAL = "250"
    STATUS_STOP_GO_OPEN_CLOSE = "251"
    STATUS_STOP_GO_FAILURE_NO_FAILURE = "252"
    STATUS_STOP_GO_BLOCK_NOT_BLOCK = "253"
    STATUS_STOP_GO_OPEN_CC_BETWEEN_N = "254"
    STATUS_STOP_GO_OPENED_GROUND_FAULT = "255"
    STATUS_STOP_GO_OPEN_VMAX = "256"
    STATUS_STOP_GO_SELF_TEST_DISABLED = "257"
    STATUS_STOP_GO_AUTOMATIC_RESET_OFF = "258"
    STATUS_STOP_GO_CHECK_OFF = "259"
    STATUS_STOP_GO_WAITING_FOR_CLOSING = "260"
    STATUS_STOP_GO_FIRST_24H_OPENING = "261"
    STATUS_STOP_GO_POWER_FAILURE_DOWNSTREAM = "262"
    STATUS_STOP_GO_POWER_FAILURE_UPSTREAM = "263"
    DAILY_TOTALIZERS_HOURLY_16BIT = "511"
    MONTHLY_AVERAGE_HOURLY_16BIT = "512"
    MONTHLY_TOTALIZERS_CURRENT_YEAR_32BIT = "513"
    MONTHLY_TOTALIZERS_LAST_YEAR_32BIT = "514"

    # TODO: Refactor this
    def with_parameter(self, parameter: str | int) -> Dimension:  # type: ignore[override]
        """Returns the tag with the specified parameter"""
        return Dimension(f"{self}#{parameter}")


class WhatEnergy(What, StrEnum):
    """
    What tags for energy management items.
    It is used only internally to send the correct command to the gateway.

    Attributes:
        AUTO_RESET_ON: Activate the auto reset.
        AUTO_RESET_OFF: Deactivate the auto reset.
        SEND_DAILY_REPORT: Send the power consumption for the day for each hour.
        SEND_MONTHLY_REPORT: Send the hourly average power consumption for the month.
        SEND_YEARLY_REPORT: Send the daily average power consumption for the year.
        SEND_LAST_YEAR_REPORT: Send the daily average power consumption for the last year.
        ENABLE_ACTUATOR: Command to enable the actuator.
        FORCE_ACTUATOR_ON: Command to force the actuator on for a specific time.
        FORCE_ACTUATOR_OFF: End the forced actuator.
        RESET_REPORT: Command to reset the measurements.
    """
    AUTO_RESET_ON = "26"
    AUTO_RESET_OFF = "27"
    SEND_DAILY_REPORT = "57"
    SEND_MONTHLY_REPORT = "58"
    SEND_YEARLY_REPORT = "59"
    SEND_LAST_YEAR_REPORT = "510"
    ENABLE_ACTUATOR = "71"
    FORCE_ACTUATOR_ON = "73"
    FORCE_ACTUATOR_OFF = "74"
    RESET_REPORT = "75"

    # TODO: Refactor this
    def with_parameter(self, parameter: str | int) -> What:  # type: ignore[override]
        """Returns the tag with the specified parameter"""
        return What(f"{self}#{parameter}")


class TypeEnergy(Enum):
    """
    Type of energy management items.

    Attributes:
        POWER_METER: Power meter.
        ACTUATOR: Actuator.
        STOP_GO: Stop&Go device.
    """
    POWER_METER = auto()
    ACTUATOR = auto()
    STOP_GO = auto()


@dataclass
class ActuatorStatus:
    """
    Represents the status of an actuator.

    Attributes:
        disabled: The actuator is disabled.
        forcing: The actuator is forced.
        threshold: The actuator is below the threshold.
        protection: The actuator is in protection.
        phase: The local phase is disabled.
        advanced: It's set in advanced mode, otherwise it is basic
    """
    disabled: bool
    forcing: bool
    threshold: bool
    protection: bool
    phase: bool
    advanced: bool


class EnergyManagement(BaseItem):
    """
    Used to control energy management items, like actuators with current sensors, etc...

    Allowed where tags:
    - 1N (N=[1-127]): Stop&Go devices,
        these are circuit breakers capable of detecting a fault and opening the circuit.
    - 5N (N=[1-255]): Power meters, these are devices that measure the power consumption.
    - 7N#0 (N=[1-255]): Actuators,
        these implement the same functionalities as power meters but can also control the power flow.
    """
    _who = Who.ENERGY_MANAGEMENT

    _event_callbacks: dict[DimensionEnergy, list[CoroutineCallback]] = {}

    def __init__(self, client: BaseClient, where: Where | str, *, who: Who | str | None = None):
        """
        Initializes the item and check if the where tag is valid.

        Args:
            client: The client to use to communicate with the server.
            where: The location of the item.
            who: The type of item.

        Raises:
            InvalidTag: If the where tag is not valid.
        """
        super().__init__(client, where, who=who)
        self.get_type()

    def get_type(self) -> TypeEnergy:
        """
        The type of the item.

        Returns:
            The type of the item.

        Raises:
            InvalidTag: If the where tag is not valid.
        """
        if self.where.string.startswith("1") and self.where.string[1:].isnumeric():
            return TypeEnergy.STOP_GO
        elif self.where.string.startswith("5") and self.where.string[1:].isnumeric():
            return TypeEnergy.POWER_METER
        elif self.where.string.startswith("7") and self.where.parameters[0] == "0" and self.where.tag[1:].isnumeric():
            return TypeEnergy.ACTUATOR
        else:
            raise InvalidTag(self.where)

    async def start_sending_daily_totalizers_hourly(self, day: int | None, month: int | None):
        """
        Start sending daily totalizers on an hourly basis on an event session.
        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.

        Args:

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        if day is None:
            day = datetime.now().day
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(
            WhatEnergy.SEND_DAILY_REPORT.with_parameter(day).with_parameter(month)
        )

    async def start_sending_monthly_average_hourly(self, month: int | None):
        """
        Start sending monthly average on an hourly basis on an event session.
        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.

        Args:

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(
            WhatEnergy.SEND_MONTHLY_REPORT.with_parameter(month)
        )

    async def start_sending_monthly_totalizers_current_year(self, month: int | None):
        """
        Start sending monthly totalizers current year on a daily basis on an event session.
        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.

        Args:

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(
            WhatEnergy.SEND_YEARLY_REPORT.with_parameter(month)
        )

    async def start_sending_monthly_totalizers_last_year(self, month: int | None):
        """
        Start sending monthly totalizers last year on a daily basis on an event session.
        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.

        Args:

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(
            WhatEnergy.SEND_LAST_YEAR_REPORT.with_parameter(month)
        )

    async def enable_actuator(self):
        """
        Enable the actuator.

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_normal_message(WhatEnergy.ENABLE_ACTUATOR)

    async def force_actuator_on(self, time: int | None = None):
        """
        Force the actuator on for a specific time.

        Args:
            time: The time in tens of minutes [1-254]. Use default time if None.

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        if time is None:
            await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_ON)
        else:
            await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_ON.with_parameter(time))

    async def force_actuator_off(self):
        """
        End the forced actuator.

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_OFF)

    async def reset_totalizers(self, tot_n: int):
        """
        Reset the totalizers.

        Args:
            tot_n: The totalizer number to reset [1-2]

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_normal_message(WhatEnergy.RESET_REPORT.with_parameter(tot_n))

    async def start_sending_instant_power(self, time: int, power_type: int = 1):
        """
        Start sending the instant power consumption on an event session.
        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.

        Args:
            time: Indicates after how many minutes it sends the consumption if it changes [1-255]
            power_type: 1 for active power

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_dimension_writing(
            DimensionEnergy.END_AUTOMATIC_UPDATE_SIZE.with_parameter(power_type),
            Value(time)
        )

    async def stop_sending_instant_power(self, power_type: int = 1):
        """
        Stop sending the instant power consumption on an event session.
        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.

        Args:
            power_type: 1 for active power

        Returns:
            None

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_dimension_writing(
            DimensionEnergy.END_AUTOMATIC_UPDATE_SIZE.with_parameter(power_type),
            Value(0)
        )

    async def get_active_power(self) -> float:
        """
        Get the active power.

        Returns:
            The active power in W.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.ACTIVE_POWER)

        return float(resp.values[0].string)

    async def get_energy_unit_totalizer(self) -> float:
        """
        Get the energy/unit totalizer.

        Returns:
            The energy/unit totalizer in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.ENERGY_UNIT_TOTALIZER)

        return float(resp.values[0].string)

    async def get_energy_unit_per_month(self, month: int | None = None, year: int | None = None) -> float:
        """
        Get the energy/unit per month.

        Args:
            month: The month to get the energy from [1-12]. Use the current month if None.
            year: The year to get the energy from. Format: YY (e.g., 21).
                Use the current year if None.

        Returns:
            The energy measured in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year % 100

        resp = await self._single_dim_req(
            DimensionEnergy.ENERGY_UNIT_PER_MONTH.with_parameter(year).with_parameter(month)
        )

        return float(resp.values[0].string)

    async def get_partial_totalizer_current_month(self) -> float:
        """
        Get the partial totalizer for the current month.
        This is equivalent to get_energy_unit_per_month() without any args.

        Returns:
            The partial totalizer for the current month in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_MONTH)

        return float(resp.values[0].string)

    async def get_partial_totalizer_current_day(self) -> float:
        """
        Get the partial totalizer for the current day.

        Returns:
            The partial totalizer for the current day in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_DAY)

        return float(resp.values[0].string)

    async def get_actuators_info(self) -> ActuatorStatus:
        """
        Get the actuator info.

        Returns:
            The status of the actuator.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.ACTUATORS_INFO)

        return ActuatorStatus(
            disabled=bool(int(resp.values[0].string[0])),
            forcing=bool(int(resp.values[0].string[1])),
            threshold=bool(int(resp.values[0].string[2])),
            protection=bool(int(resp.values[0].string[3])),
            phase=bool(int(resp.values[0].string[4])),
            advanced=not bool(int(resp.values[0].string[5])-1),
        )

    async def get_totalizers(self, tot_n: int) -> tuple[datetime, float]:
        """
        Get the energy measured from the last reset.

        Args:
            tot_n: The totalizer number to get [1-2]

        Returns:
            A tuple containing the date and time of the last reset and the energy measured in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.TOTALIZERS.with_parameter(tot_n))

        energy = float(resp.values[0].string)
        d = resp.values[1].string
        m = resp.values[2].string
        y = resp.values[3].string
        h = resp.values[4].string
        mi = resp.values[5].string

        return datetime(int(y), int(m), int(d), int(h), int(mi)), energy

    async def get_differential_current_level(self) -> int:
        """
        Get the differential current level.

        Returns:
            The differential level [1-3].
            !!! note
                If you know the meaning of this value, please open an issue on GitHub.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        resp = await self._single_dim_req(DimensionEnergy.DIFFERENTIAL_CURRENT_LEVEL)

        return int(resp.values[0].string)

    @classmethod
    async def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        raise NotImplementedError
