from asyncio import Task
from datetime import datetime
from enum import StrEnum, Enum, auto
from typing import Self

from ..base import BaseItem, CoroutineCallback
from ...client import BaseClient
from ...exceptions import InvalidTag
from ...messages import BaseMessage
from ...tags import Who, What, Where, Dimension

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

    def with_parameter(self, parameter: str | int) -> Dimension:
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

    def with_parameter(self, parameter: str | int) -> What:
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
        
    @classmethod
    async def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        raise NotImplementedError
