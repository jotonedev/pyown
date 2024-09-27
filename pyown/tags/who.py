import enum
from typing import Final

from .base import Tag

__all__ = [
    "Who",
]


class Who(Tag, enum.Enum):
    SCENE: str = "0"
    LIGHTING: str = "1"
    AUTOMATION: str = "2"
    LOAD_CONTROL: str = "3"
    THERMOREGULATION: str = "4"
    BURGLAR_ALARM: str = "5"
    VIDEO_DOOR_ENTRY: str = "6"
    GATEWAY: str = "13"
    CEN_1: str = "15"
    SOUND_DIFFUSION_1: str = "16"
    MH200N_SCENE: str = "17"
    ENERGY_MANAGEMENT: str = "18"
    SOUND_DIFFUSION_2: str = "22"
    CEN_2: str = "25"
    AUTOMATION_DIAGNOSTICS: str = "1001"
    THERMOREGULATION_DIAGNOSTICS: str = "1004"
    DEVICE_DIAGNOSTICS: str = "1013"
    ENERGY_DIAGNOSTICS: str = "1018"

    def __str__(self) -> str:
        return self.value

    @property
    def name(self) -> str:
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
