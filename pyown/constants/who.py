from typing import Final, Union

__all__ = [
    "SCENE",
    "LIGHTING",
    "AUTOMATION",
    "LOAD_CONTROL",
    "THERMOREGULATION",
    "BURGLAR_ALARM",
    "VIDEO_DOOR_ENTRY",
    "GATEWAY",
    "CEN_1",
    "SOUND_DIFFUSION_1",
    "MH200N_SCENE",
    "ENERGY_MANAGEMENT",
    "SOUND_DIFFUSION_2",
    "CEN_2",
    "AUTOMATION_DIAGNOSTICS",
    "THERMOREGULATION_DIAGNOSTICS",
    "DEVICE_DIAGNOSTICS",
    "WHO",
    "WHO_MAP",
]

SCENE: Final = "0"
LIGHTING: Final = "1"
AUTOMATION: Final = "2"
LOAD_CONTROL: Final = "3"
THERMOREGULATION: Final = "4"
BURGLAR_ALARM: Final = "5"
VIDEO_DOOR_ENTRY: Final = "6"
GATEWAY: Final = "13"
CEN_1: Final = "15"
SOUND_DIFFUSION_1: Final = "16"
MH200N_SCENE: Final = "17"
ENERGY_MANAGEMENT: Final = "18"
SOUND_DIFFUSION_2: Final = "22"
CEN_2: Final = "25"
AUTOMATION_DIAGNOSTICS: Final = "1001"
THERMOREGULATION_DIAGNOSTICS: Final = "1004"
DEVICE_DIAGNOSTICS: Final = "1013"
ENERGY_DIAGNOSTICS: Final = "1018"

WHO = Union[
    SCENE, 
    LIGHTING, 
    AUTOMATION, 
    LOAD_CONTROL, 
    THERMOREGULATION, 
    BURGLAR_ALARM, 
    VIDEO_DOOR_ENTRY, 
    GATEWAY, 
    CEN_1, 
    SOUND_DIFFUSION_1, 
    MH200N_SCENE,
    ENERGY_MANAGEMENT,
    SOUND_DIFFUSION_2,
    CEN_2,
    AUTOMATION_DIAGNOSTICS,
    THERMOREGULATION_DIAGNOSTICS,
    DEVICE_DIAGNOSTICS,
]

WHO_MAP = {
    SCENE: "Scene",
    LIGHTING: "Lighting",
    AUTOMATION: "Automation",
    LOAD_CONTROL: "Load control",
    THERMOREGULATION: "Thermoregulation",
    BURGLAR_ALARM: "Burglar alarm",
    VIDEO_DOOR_ENTRY: "Video door entry",
    GATEWAY: "Gateway management",
    CEN_1: "CEN",
    SOUND_DIFFUSION_1: "Sound diffusion 1",
    MH200N_SCENE: "MH200N Scene",
    ENERGY_MANAGEMENT: "Energy management",
    SOUND_DIFFUSION_2: "Sound diffusion 2",
    CEN_2: "CEN plus / scenarios plus / dry contacts",
    AUTOMATION_DIAGNOSTICS: "Automation diagnostics",
    THERMOREGULATION_DIAGNOSTICS: "Thermoregulation diagnostics",
    DEVICE_DIAGNOSTICS: "Device diagnostics",
}

