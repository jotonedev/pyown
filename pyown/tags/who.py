from enum import StrEnum

__all__ = [
    "WHO",
    "WHO_MAP",
]


class WHO(StrEnum):
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

    @property
    def name(self) -> str:
        return WHO_MAP[self]

    @property
    def number(self) -> int:
        return int(self)


WHO_MAP = {
    WHO.SCENE: "Scene",
    WHO.LIGHTING: "Lighting",
    WHO.AUTOMATION: "Automation",
    WHO.LOAD_CONTROL: "Load control",
    WHO.THERMOREGULATION: "Thermoregulation",
    WHO.BURGLAR_ALARM: "Burglar alarm",
    WHO.VIDEO_DOOR_ENTRY: "Video door entry",
    WHO.GATEWAY: "Gateway management",
    WHO.CEN_1: "CEN",
    WHO.SOUND_DIFFUSION_1: "Sound diffusion 1",
    WHO.MH200N_SCENE: "MH200N Scene",
    WHO.ENERGY_MANAGEMENT: "Energy management",
    WHO.SOUND_DIFFUSION_2: "Sound diffusion 2",
    WHO.CEN_2: "CEN plus / scenarios plus / dry contacts",
    WHO.AUTOMATION_DIAGNOSTICS: "Automation diagnostics",
    WHO.THERMOREGULATION_DIAGNOSTICS: "Thermoregulation diagnostics",
    WHO.DEVICE_DIAGNOSTICS: "Device diagnostics",
}

