from asyncio import Task
from datetime import datetime
from typing import Self, Callable, Coroutine, Any

from .dataclass import ActuatorStatus, StopGoStatus
from .enums import DimensionEnergy, WhatEnergy, TypeEnergy
from ..base import BaseItem, CoroutineCallback, EventMessage
from ...client import BaseClient
from ...exceptions import InvalidTag, InvalidMessage
from ...messages import BaseMessage, DimensionResponse
from ...tags import Who, Where, Value

__all__ = [
    "EnergyManagement",
]


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

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_normal_message(WhatEnergy.ENABLE_ACTUATOR)

    async def force_actuator_on(self, time: int | None = None):
        """
        Force the actuator on for a specific time.

        Args:
            time: The time in tens of minutes [1-254]. Use default time if None.

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

        Raises:
            ResponseError: When the gateway does not acknowledge the command
        """
        await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_OFF)

    async def reset_totalizers(self, tot_n: int):
        """
        Reset the totalizers.

        Args:
            tot_n: The totalizer number to reset [1-2]

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
        message = await self._single_dim_req(DimensionEnergy.ACTIVE_POWER)

        return float(message.values[0].string)

    async def get_energy_unit_totalizer(self) -> float:
        """
        Get the energy/unit totalizer.

        Returns:
            The energy/unit totalizer in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        message = await self._single_dim_req(DimensionEnergy.ENERGY_UNIT_TOTALIZER)

        return float(message.values[0].string)

    async def get_energy_unit_per_month(
            self,
            month: int | None = None,
            year: int | None = None,
    ) -> float:
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

        message = await self._single_dim_req(
            DimensionEnergy.ENERGY_UNIT_PER_MONTH.with_parameter(year).with_parameter(month)
        )

        return float(message.values[0].string)

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
        message = await self._single_dim_req(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_DAY)

        return float(message.values[0].string)

    async def get_actuators_info(self, *, message: EventMessage = None) -> ActuatorStatus:
        """
        Get the actuator info.

        Args:
            message: The message to parse the status from.
                It's used internally to avoid code duplication.

        Returns:
            The status of the actuator.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        if message is None:
            message = await self._single_dim_req(DimensionEnergy.ACTUATORS_INFO)

        return ActuatorStatus(
            disabled=bool(int(message.values[0].string[0])),
            forcing=bool(int(message.values[0].string[1])),
            threshold=bool(int(message.values[0].string[2])),
            protection=bool(int(message.values[0].string[3])),
            phase=bool(int(message.values[0].string[4])),
            advanced=not bool(int(message.values[0].string[5]) - 1),
        )

    async def get_totalizers(self, tot_n: int, *, message: EventMessage = None) -> tuple[datetime, float]:
        """
        Get the energy measured from the last reset.

        Args:
            tot_n: The totalizer number to get [1-2]
            message: The message to parse the status from.
                It's used internally to avoid code duplication.

        Returns:
            A tuple containing the date and time of the last reset and the energy measured in kWh.

        Raises:
            ResponseError: When the gateway does not respond with the requested data
        """
        if message is None:
            message = await self._single_dim_req(DimensionEnergy.TOTALIZERS.with_parameter(tot_n))

        energy = float(message.values[0].string)
        d = message.values[1].string
        m = message.values[2].string
        y = message.values[3].string
        h = message.values[4].string
        mi = message.values[5].string

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
        message = await self._single_dim_req(DimensionEnergy.DIFFERENTIAL_CURRENT_LEVEL)

        return int(message.values[0].string)

    #
    # Event callbacks
    #

    @classmethod
    def on_daily_totalizers_hourly(cls, callback: Callable[[Self, int, int, int, int], Coroutine[None, None, None]]):
        """
        Register a callback for the daily totalizers on an hourly basis event.
        !!! note
            To start receiving the event, use the start_sending_daily_totalizers_hourly() with a command session.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item, the day, the month, the hour, and the energy measured in Wh.
                If the hour is 25, it means that the energy is the total for the day.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.DAILY_TOTALIZERS_HOURLY_16BIT, []).append(callback)

    @classmethod
    def on_monthly_average_hourly(cls, callback: Callable[[Self, int, int, int, int], Coroutine[None, None, None]]):
        """
        Register a callback for the monthly average on an hourly basis event.
        !!! note
            To start receiving the event, use the start_sending_monthly_average_hourly() with a command session.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item, the month, the hour, and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.MONTHLY_AVERAGE_HOURLY_16BIT, []).append(callback)

    @classmethod
    def on_monthly_totalizers_current_year(
            cls,
            callback: Callable[[Self, int, int, int, int], Coroutine[None, None, None]]
    ):
        """
        Register a callback for the monthly totalizers current year on a daily basis event.
        !!! note
            To start receiving the event,
            use the start_sending_monthly_totalizers_current_year() with a command session.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item, the month, the day, and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.MONTHLY_TOTALIZERS_CURRENT_YEAR_32BIT, []).append(callback)

    @classmethod
    def on_monthly_totalizers_last_year(
            cls,
            callback: Callable[[Self, int, int, int, int], Coroutine[None, None, None]]
    ):
        """
        Register a callback for the monthly totalizers last year on a daily basis event.
        !!! note
            To start receiving the event,
            use the start_sending_monthly_totalizers_last_year() with a command session.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item, the month, the day, and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.MONTHLY_TOTALIZERS_LAST_YEAR_32BIT, []).append(callback)

    @classmethod
    def on_stop_go_status(cls, callback: Callable[[Self, StopGoStatus], Coroutine[None, None, None]]):
        """
        Register a callback for the stop&go status change event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the status of the stop&go device.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.STATUS_STOP_GO_GENERAL, []).append(callback)

    @classmethod
    def on_instant_power(cls, callback: Callable[[Self, float], Coroutine[None, None, None]]):
        """
        Register a callback for the instant power consumption event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the power measured in Watts.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.ACTIVE_POWER, []).append(callback)

    @classmethod
    def on_energy_unit_totalizer(cls, callback: Callable[[Self, float], Coroutine[None, None, None]]):
        """
        Register a callback for the energy/unit totalizer event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.ENERGY_UNIT_TOTALIZER, []).append(callback)

    @classmethod
    def on_energy_unit_per_month(cls, callback: Callable[[Self, int, int, float], Coroutine[None, None, None]]):
        """
        Register a callback for the energy/unit per month event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item, the month, the year, and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.ENERGY_UNIT_PER_MONTH, []).append(callback)

    @classmethod
    def on_partial_totalizer_current_month(cls, callback: Callable[[Self, float], Coroutine[None, None, None]]):
        """
        Register a callback for the partial totalizer current month event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_MONTH, []).append(callback)

    @classmethod
    def on_partial_totalizer_current_day(cls, callback: Callable[[Self, float], Coroutine[None, None, None]]):
        """
        Register a callback for the partial totalizer current day event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_DAY, []).append(callback)

    @classmethod
    def on_actuators_info(cls, callback: Callable[[Self, ActuatorStatus], Coroutine[None, None, None]]):
        """
        Register a callback for the actuator info event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the status of the actuator.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.ACTUATORS_INFO, []).append(callback)

    @classmethod
    def on_totalizer_since_reset(cls, callback: Callable[[Self, int, datetime, float], Coroutine[None, None, None]]):
        """
        Register a callback for the totalizer since reset event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item, the totalizer number, the date and time of the last reset,
                and the energy measured in Wh.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.TOTALIZERS, []).append(callback)

    @classmethod
    def on_differential_current_level(cls, callback: Callable[[Self, int], Coroutine[None, None, None]]):
        """
        Register a callback for the differential current level event.

        Args:
            callback: The callback to call when the event is received.
                It will receive the item and the differential current level.
        """
        cls._event_callbacks.setdefault(DimensionEnergy.DIFFERENTIAL_CURRENT_LEVEL, []).append(callback)

    @classmethod
    async def call_callbacks(cls, item: Self, message: BaseMessage) -> list[Task]:
        if not isinstance(message, DimensionResponse):
            raise InvalidMessage("The message is not a DimensionResponse message.")

        # TODO: Refactor this
        dim = DimensionEnergy(message.dimension.string)

        tasks = []
        callbacks = cls._event_callbacks.get(dim, [])

        # noinspection PyUnusedLocal
        args: tuple[Any, ...]
        if dim.tag == DimensionEnergy.DAILY_TOTALIZERS_HOURLY_16BIT:
            month = int(dim.parameters[0])
            hour = int(message.values[0].string)
            val = float(message.values[1].string)
            args = (item, month, hour, val)
        elif dim.tag == DimensionEnergy.MONTHLY_AVERAGE_HOURLY_16BIT:
            month = int(dim.parameters[0])
            hour = int(message.values[0].string)
            val = float(message.values[1].string)
            args = (item, month, hour, val)
        elif dim.tag == DimensionEnergy.MONTHLY_TOTALIZERS_CURRENT_YEAR_32BIT:
            month = int(dim.parameters[0])
            day = int(message.values[0].string)
            val = float(message.values[1].string)
            args = (item, month, day, val)
        elif dim.tag == DimensionEnergy.MONTHLY_TOTALIZERS_LAST_YEAR_32BIT:
            month = int(dim.parameters[0])
            day = int(message.values[0].string)
            val = float(message.values[1].string)
            args = (item, month, day, val)
        elif dim.tag == DimensionEnergy.STATUS_STOP_GO_GENERAL:
            status = StopGoStatus(
                open=bool(int(message.values[0].string[0])),
                failure=bool(int(message.values[0].string[1])),
                block=bool(int(message.values[0].string[2])),
                open_cc=bool(int(message.values[0].string[3])),
                open_ground_fault=bool(int(message.values[0].string[4])),
                open_vmax=bool(int(message.values[0].string[5])),
                self_test_off=bool(int(message.values[0].string[6])),
                auto_reset_off=bool(int(message.values[0].string[7])),
                check_off=bool(int(message.values[0].string[8])),
                waiting_closing=bool(int(message.values[0].string[9])),
                first_24h_open=bool(int(message.values[0].string[10])),
                power_fail_down=bool(int(message.values[0].string[11])),
                power_fail_up=bool(int(message.values[0].string[12])),
            )
            args = (item, status)
        elif dim.tag == DimensionEnergy.ACTUATORS_INFO:
            info = await item.get_actuators_info(message=message)
            args = (item, info)
        elif dim.tag == DimensionEnergy.ACTIVE_POWER:
            power = float(message.values[0].string)
            args = (item, power)
        elif dim.tag == DimensionEnergy.ENERGY_UNIT_TOTALIZER:
            energy = float(message.values[0].string)
            args = (item, energy)
        elif dim.tag == DimensionEnergy.ENERGY_UNIT_PER_MONTH:
            month = int(dim.parameters[1])
            year = int(dim.parameters[0])
            energy = float(message.values[0].string)
            args = (item, month, year, energy)
        elif dim.tag == DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_MONTH:
            energy = float(message.values[0].string)
            args = (item, energy)
        elif dim.tag == DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_DAY:
            energy = float(message.values[0].string)
            args = (item, energy)
        elif dim.tag == DimensionEnergy.TOTALIZERS:
            args = await item.get_totalizers(int(dim.parameters[0]), message=message)
            args = (item, *args)
        elif dim.tag == DimensionEnergy.DIFFERENTIAL_CURRENT_LEVEL:
            level = int(message.values[0].string)
            args = (item, level)
        else:
            return []

        tasks += cls._create_tasks(callbacks, *args)

        return tasks
