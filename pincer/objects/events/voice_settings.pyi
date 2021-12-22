from ...utils.api_object import APIObject as APIObject
from enum import Enum, IntEnum
from typing import Any, List

class AvailableDevices(APIObject):
    id: str
    name: str

class VoiceSettingsInput(APIObject):
    device_id: str
    volume: float
    available_devices: List[AvailableDevices]

class VoiceSettingsOutput(APIObject):
    device_id: str
    volume: float
    available_devices: List[AvailableDevices]

class VoiceSettingsModeType(Enum):
    PUSH_TO_TALK: Any
    VOICE_ACTIVITY: Any

class KeyTypes(IntEnum):
    KEYBOARD_KEY: int
    MOUSE_BUTTON: int
    KEYBOARD_MODIFIER_KEY: int
    GAMEPAD_BUTTON: int

class ShortcutKeyCombo(APIObject):
    type: KeyTypes
    code: int
    name: str

class VoiceSettingsMode(APIObject):
    type: VoiceSettingsModeType
    auto_threshold: bool
    threshold: float
    shortcut: ShortcutKeyCombo
    delay: float

class VoiceSettingsUpdateEvent(APIObject):
    input: VoiceSettingsInput
    output: VoiceSettingsOutput
    automatic_gain_control: bool
    echo_cancellation: bool
    noise_suppression: bool
    qos: bool
    silence_warning: bool
    deaf: bool
    mute: bool
