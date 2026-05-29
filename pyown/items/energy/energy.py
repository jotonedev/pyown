from datetime import datetime

from ...client import BaseClient
from ...events import item
from ...exceptions import InvalidTag
from ...messages import DimensionResponse, DimensionWriting
from ...tags import Value, Where, Who
from ..base import BaseItem, EventMessage
from .dataclass import ActuatorStatus
from .enums import DimensionEnergy, TypeEnergy, WhatEnergy

__all__ = [
    "EnergyManagement",
]


@item(Who.ENERGY_MANAGEMENT)
class EnergyManagement(BaseItem):
    """Used to control energy management items, like actuators with current sensors, etc.

    Allowed where tags:

    - 1N (N=[1-127]): Stop&Go devices,
        these are circuit breakers capable of detecting a fault and opening the circuit.
    - 5N (N=[1-255]): Power meters, these are devices that measure the power consumption.
    - 7N#0 (N=[1-255]): Actuators,
        these implement the same functionalities as power meters but can also control the power flow.
    """

    def __init__(self, client: BaseClient, where: Where | str, *, who: Who | str | None = None):
        """Initializes the item and check if the where tag is valid.

        Raises:
            InvalidTag: If the where tag is not valid.
        """
        super().__init__(client, where, who=who)
        self.get_type()

    def get_type(self) -> TypeEnergy:
        """The type of the item.

        Raises:
            InvalidTag: If the where tag is not valid.
        """
        if self.where.string.startswith("1") and self.where.string[1:].isnumeric():
            return TypeEnergy.STOP_GO
        elif self.where.string.startswith("5") and self.where.string[1:].isnumeric():
            return TypeEnergy.POWER_METER
        elif (
            self.where.string.startswith("7")
            and self.where.parameters[0] == "0"
            and self.where.tag[1:].isnumeric()
        ):
            return TypeEnergy.ACTUATOR
        else:
            raise InvalidTag(self.where)

    async def start_sending_daily_totalizers_hourly(self, day: int | None, month: int | None):
        """Start sending daily totalizers on an hourly basis on an event session.

        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.
        """
        if day is None:
            day = datetime.now().day
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(
            WhatEnergy.SEND_DAILY_REPORT.with_parameter(day).with_parameter(month)
        )

    async def start_sending_monthly_average_hourly(self, month: int | None):
        """Start sending monthly average on an hourly basis on an event session.

        !!! note
            Even if the data is sent to the event session, this command must be sent on a command session.
        """
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(WhatEnergy.SEND_MONTHLY_REPORT.with_parameter(month))

    async def start_sending_monthly_totalizers_current_year(self, month: int | None):
        """Start sending monthly totalizers current year on a daily basis on an event session."""
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(WhatEnergy.SEND_YEARLY_REPORT.with_parameter(month))

    async def start_sending_monthly_totalizers_last_year(self, month: int | None):
        """Start sending monthly totalizers last year on a daily basis on an event session."""
        if month is None:
            month = datetime.now().month

        await self.send_normal_message(WhatEnergy.SEND_LAST_YEAR_REPORT.with_parameter(month))

    async def enable_actuator(self):
        """Enable the actuator."""
        await self.send_normal_message(WhatEnergy.ENABLE_ACTUATOR)

    async def force_actuator_on(self, time: int | None = None):
        """Force the actuator on for a specific time.

        Args:
            time: The time in tens of minutes [1-254]. Use default time if None.
        """
        if time is None:
            await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_ON)
        else:
            await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_ON.with_parameter(time))

    async def force_actuator_off(self):
        """End the forced actuator."""
        await self.send_normal_message(WhatEnergy.FORCE_ACTUATOR_OFF)

    async def reset_totalizers(self, tot_n: int):
        """Reset the totalizers.

        Args:
            tot_n: The totalizer number to reset [1-2]
        """
        await self.send_normal_message(WhatEnergy.RESET_REPORT.with_parameter(tot_n))

    async def start_sending_instant_power(self, time: int, power_type: int = 1):
        """Start sending the instant power consumption on an event session.

        Args:
            time: Indicates after how many minutes it sends the consumption if it changes [1-255]
            power_type: 1 for active power
        """
        await self.send_dimension_writing(
            DimensionEnergy.END_AUTOMATIC_UPDATE_SIZE.with_parameter(power_type),
            Value(time),
        )

    async def stop_sending_instant_power(self, power_type: int = 1):
        """Stop sending the instant power consumption on an event session.

        Args:
            power_type: 1 for active power
        """
        await self.send_dimension_writing(
            DimensionEnergy.END_AUTOMATIC_UPDATE_SIZE.with_parameter(power_type),
            Value(0),
        )

    async def get_active_power(self) -> float:
        """Get the active power."""
        message = await self._single_dim_req(DimensionEnergy.ACTIVE_POWER)
        return float(message.values[0].string)

    async def get_energy_unit_totalizer(self) -> float:
        """Get the energy/unit totalizer."""
        message = await self._single_dim_req(DimensionEnergy.ENERGY_UNIT_TOTALIZER)
        return float(message.values[0].string)

    async def get_energy_unit_per_month(
        self,
        month: int | None = None,
        year: int | None = None,
    ) -> float:
        """Get the energy/unit per month.

        Args:
            month: The month to get the energy from [1-12]. Use the current month if None.
            year: The year to get the energy from. Format: YY (e.g., 21). Use the current year if None.
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
        """Get the partial totalizer for the current month."""
        resp = await self._single_dim_req(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_MONTH)
        return float(resp.values[0].string)

    async def get_partial_totalizer_current_day(self) -> float:
        """Get the partial totalizer for the current day."""
        message = await self._single_dim_req(DimensionEnergy.PARTIAL_TOTALIZER_CURRENT_DAY)
        return float(message.values[0].string)

    # ------------------------------------------------------------------
    # Sync decoders for event-friendly reuse.
    # ------------------------------------------------------------------

    @staticmethod
    def _decode_actuators_info(
        message: DimensionResponse | DimensionWriting,
    ) -> ActuatorStatus:
        s = message.values[0].string
        return ActuatorStatus(
            disabled=bool(int(s[0])),
            forcing=bool(int(s[1])),
            threshold=bool(int(s[2])),
            protection=bool(int(s[3])),
            phase=bool(int(s[4])),
            advanced=not bool(int(s[5]) - 1),
        )

    @staticmethod
    def _decode_totalizers(
        message: DimensionResponse | DimensionWriting,
    ) -> tuple[datetime, float]:
        energy = float(message.values[0].string)
        d = message.values[1].string
        m = message.values[2].string
        y = message.values[3].string
        h = message.values[4].string
        mi = message.values[5].string
        return datetime(int(y), int(m), int(d), int(h), int(mi)), energy

    async def get_actuators_info(self, *, message: EventMessage = None) -> ActuatorStatus:
        """Get the actuator info."""
        msg = (
            message
            if message is not None
            else await self._single_dim_req(DimensionEnergy.ACTUATORS_INFO)
        )
        return self._decode_actuators_info(msg)

    async def get_totalizers(
        self, tot_n: int, *, message: EventMessage = None
    ) -> tuple[datetime, float]:
        """Get the energy measured from the last reset.

        Args:
            tot_n: The totalizer number to get [1-2]
        """
        msg = (
            message
            if message is not None
            else await self._single_dim_req(
                DimensionEnergy.TOTALIZERS.with_parameter(tot_n)
            )
        )
        return self._decode_totalizers(msg)

    async def get_differential_current_level(self) -> int:
        """Get the differential current level."""
        message = await self._single_dim_req(DimensionEnergy.DIFFERENTIAL_CURRENT_LEVEL)
        return int(message.values[0].string)
