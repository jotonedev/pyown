from enum import StrEnum
from typing import Final

from .base import Tag

__all__ = [
    "Who",
]


class Who(Tag, StrEnum):
    """
    Who tag class.

    This is an enum class because the value allowed in this tag is limited to the ones listed.

    Attributes:
        SCENE: used for scenarios modules
        LIGHTING: used to manage all lighting devices
        AUTOMATION: used to control shutter, rolling shutters, and other automation devices
        LOAD_CONTROL: used to control power management devices
        THERMOREGULATION: used to control heating and cooling centralized systems or probes
        BURGLAR_ALARM: used to control security systems
        DOOR_ENTRY_SYSTEM: used to control outdoor entry systems
        VIDEO_DOOR_ENTRY: used to control video door entry systems
        AUXILIARY: used to control auxiliary devices
        GATEWAY: used to get information about the gateway
        ACTUATORS_LOCKS: used to control actuators and locks
        CEN_1: similar to the SCENE who
        SOUND_DIFFUSION_1: used to control sound diffusion systems
        MH200N_SCENE: used to control scenarios on the MH200N (similar to SCENE)
        ENERGY_MANAGEMENT: used to read data from energy measurement devices
        SOUND_DIFFUSION_2: extension of SOUND_DIFFUSION_1
        LIGHTING_MANAGEMENT: extension of LIGHTING
        CEN_2: extension of CEN_1
        AUTOMATION_DIAGNOSTICS: used to read and set low level values to automation devices
            (only used by the official MyHome software)
        THERMOREGULATION_DIAGNOSTICS: used to read and set low level values to thermoregulation devices
            (only used by the official MyHome software)
        DEVICE_DIAGNOSTICS: used to read and set low level values to devices
            (only used by the official MyHome software)
        ENERGY_DIAGNOSTICS: used to read and set low level values to energy management devices .
            (only used by the official MyHome software)
    """
    SCENE = "0"
    LIGHTING = "1"
    AUTOMATION = "2"
    LOAD_CONTROL = "3"
    THERMOREGULATION = "4"
    BURGLAR_ALARM = "5"
    DOOR_ENTRY_SYSTEM = "6"
    VIDEO_DOOR_ENTRY = "7"
    AUXILIARY = "8"
    GATEWAY = "13"
    ACTUATORS_LOCKS = "14"
    CEN_1 = "15"
    SOUND_DIFFUSION_1 = "16"
    MH200N_SCENE = "17"
    ENERGY_MANAGEMENT = "18"
    SOUND_DIFFUSION_2 = "22"
    LIGHTING_MANAGEMENT = "24"
    CEN_2 = "25"
    AUTOMATION_DIAGNOSTICS = "1001"
    THERMOREGULATION_DIAGNOSTICS = "1004"
    DEVICE_DIAGNOSTICS = "1013"
    ENERGY_DIAGNOSTICS = "1018"

    def __str__(self) -> str:
        return self.string

    @property
    def name(self) -> str:
        """Get a string description of the tag"""
        return who_map[self]


who_map: Final[dict[Who, str]] = {
    Who.SCENE: "Scene",
    Who.LIGHTING: "Lighting",
    Who.AUTOMATION: "Automation",
    Who.LOAD_CONTROL: "Load control",
    Who.THERMOREGULATION: "Thermoregulation",
    Who.BURGLAR_ALARM: "Burglar alarm",
    Who.VIDEO_DOOR_ENTRY: "Video door entry",
    Who.GATEWAY: "Gateway management",
    Who.CEN_1: "CEN",
    Who.SOUND_DIFFUSION_1: "Sound diffusion 1",
    Who.MH200N_SCENE: "MH200N Scene",
    Who.ENERGY_MANAGEMENT: "Energy management",
    Who.SOUND_DIFFUSION_2: "Sound diffusion 2",
    Who.CEN_2: "CEN plus / scenarios plus / dry contacts",
    Who.AUTOMATION_DIAGNOSTICS: "Automation diagnostics",
    Who.THERMOREGULATION_DIAGNOSTICS: "Thermoregulation diagnostics",
    Who.DEVICE_DIAGNOSTICS: "Device diagnostics",
}
