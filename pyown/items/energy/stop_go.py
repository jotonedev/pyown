from typing import AsyncIterator

from .dataclass import StopGoStatus
from .energy import EnergyManagement
from .enums import TypeEnergy, DimensionEnergy, WhatEnergy
from ...client import BaseClient
from ...exceptions import InvalidTag, InvalidMessage
from ...messages import DimensionResponse
from ...tags import Where, Who

__all__ = [
    "StopGo",
]


class StopGo(EnergyManagement):
    """
    Used to manage the Stop&Go items.
    """

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
        if self.get_type() != TypeEnergy.STOP_GO:
            raise InvalidTag(f"Invalid tag for a Stop&Go item: {where}")

    async def enable_automatic_reset(self) -> None:
        """
        Enable the automatic reset of the Stop&Go device.
        """
        await self.send_normal_message(WhatEnergy.AUTO_RESET_ON)

    async def disable_automatic_reset(self) -> None:
        """
        Disable the automatic reset of the Stop&Go device.
        """
        await self.send_normal_message(WhatEnergy.AUTO_RESET_OFF)

    async def request_status(
            self,
            *,
            messages: AsyncIterator[DimensionResponse] | None = None,
            dim_req: DimensionEnergy = DimensionEnergy.STATUS_STOP_GO_GENERAL
    ) -> StopGoStatus:
        """
        Request the status of the Stop&Go device.

        Args:
            messages: The messages to parse the status from.
                It's used internally to avoid code duplication.
            dim_req: The dimension to request the status from.
                It's used internally to avoid code duplication.

        Returns:
            The status of the Stop&Go device.

        Raises:
            InvalidMessage: If the response is invalid.
        """
        status = StopGoStatus()

        if messages is None:
            messages = self.send_dimension_request(dim_req)

        async for msg in messages:
            if not isinstance(msg, DimensionResponse):
                raise InvalidMessage(msg.message)

            dim = msg.dimension
            val = int(msg.values[0].string)

            if val is None:
                raise InvalidMessage(msg.message)

            match dim:
                case DimensionEnergy.STATUS_STOP_GO_GENERAL:
                    # in this case we have a value containing a 13-bit bitmask with each bit representing one attribute
                    status.open = bool(val & 0x01)  # bit 1
                    status.failure = bool(val & 0x02)  # bit 2
                    status.block = bool(val & 0x04)  # bit 3
                    status.open_cc = bool(val & 0x08)  # bit 4
                    status.open_ground_fault = bool(val & 0x10)  # bit 5
                    status.open_vmax = bool(val & 0x20)  # bit 6
                    status.self_test_off = bool(val & 0x40)  # bit 7
                    status.auto_reset_off = bool(val & 0x80)  # bit 8
                    status.check_off = bool(val & 0x100)  # bit 9
                    status.waiting_closing = bool(val & 0x200)  # bit 10
                    status.first_24h_open = bool(val & 0x400)  # bit 11
                    status.power_fail_down = bool(val & 0x800)  # bit 12
                    status.power_fail_up = bool(val & 0x1000)  # bit 13
                case DimensionEnergy.STATUS_STOP_GO_OPEN_CLOSE:
                    # in this case the value is a single bit representing the open/close status
                    status.open = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_FAILURE_NO_FAILURE:
                    status.failure = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_BLOCK_NOT_BLOCK:
                    status.block = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_OPEN_CC_BETWEEN_N:
                    status.open_cc = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_OPENED_GROUND_FAULT:
                    status.open_ground_fault = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_OPEN_VMAX:
                    status.open_vmax = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_SELF_TEST_DISABLED:
                    status.self_test_off = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_AUTOMATIC_RESET_OFF:
                    status.auto_reset_off = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_CHECK_OFF:
                    status.check_off = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_WAITING_FOR_CLOSING:
                    status.waiting_closing = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_FIRST_24H_OPENING:
                    status.first_24h_open = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_POWER_FAILURE_DOWNSTREAM:
                    status.power_fail_down = bool(val)
                case DimensionEnergy.STATUS_STOP_GO_POWER_FAILURE_UPSTREAM:
                    status.power_fail_up = bool(val)
                case _:
                    raise InvalidMessage(msg.message)

        return status
