from dataclasses import dataclass

__all__ = [
    "ActuatorStatus",
    "StopGoStatus"
]


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


@dataclass
class StopGoStatus:
    """
    Status of a Stop&Go device.

    Attributes:
        open: set if the circuit is open
        failure: set if a failure is detected
        block: set if the circuit is blocked
        open_cc: set if the circuit is open due to a current overload
        open_ground_fault: set if the circuit is open due to a ground fault
        open_vmax: set if the circuit is open due to a voltage overload
        auto_reset_off: set if the automatic reset is disabled
        check_off: set if the check is disabled
        waiting_closing: set if the circuit is waiting to be closed
        first_24h_open: set if the circuit was open for the first 24 hours
        power_fail_down: set if the circuit is open due to a power failure downstream
        power_fail_up: set if the circuit is open due to a power failure upstream
    """
    open: bool | None = None
    failure: bool | None = None
    block: bool | None = None
    open_cc: bool | None = None
    open_ground_fault: bool | None = None
    open_vmax: bool | None = None
    self_test_off: bool | None = None
    auto_reset_off: bool | None = None
    check_off: bool | None = None
    waiting_closing: bool | None = None
    first_24h_open: bool | None = None
    power_fail_down: bool | None = None
    power_fail_up: bool | None = None
