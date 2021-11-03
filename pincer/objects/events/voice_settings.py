# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import List

from ...utils.api_object import APIObject


@dataclass
class AvailableDevices(APIObject):
    """
    Represents an availabe device for voice settings
    
    :param id:
        id of the available device
        
    :param name:
        name of the available device
    """

    id: str
    name: str


@dataclass
class VoiceSettingsInput(APIObject):
    """
    Represents a voice setting input object
    
    :param device_id:
        the device's id
        
    :param volume:
        input voice level (min: 0, max: 100)
        
    :param available_devices:
        array of read-only device objects containing id and name string keys
    """

    device_id: str
    volume: float
    available_devices: List[AvailableDevices]


VoiceSettingsOutput = VoiceSettingsInput


class VoiceSettingsModeType(Enum):
    """Represents a voice settings mode type"""

    PUSH_TO_TALK = auto()
    VOICE_ACTIVITY = auto()


class KeyTypes(IntEnum):
    """Represents a key type"""

    KEYBOARD_KEY = 0
    MOUSE_BUTTON = 1
    KEYBOARD_MODIFIER_KEY = 2
    GAMEPAD_BUTTON = 3


@dataclass
class ShortcutKeyCombo(APIObject):
    """
    Represents a shortcut key combo for the voice mode settings from a user
    
    :param type:
        type of shortcut key combo
        
    :param code:
        key code
        
    :param name:
        key name
    """

    type: KeyTypes
    code: int
    name: str


@dataclass
class VoiceSettingsMode(APIObject):
    """
    Represents the voice mode settings from a user
    
    :param type:
        voice setting mode type
        
    :param auto_threshold:
        voice activity threshold automatically sets its threshold
        
    :param threshold:
        threshold for voice activity (in dB)
        
    :param shortcut:
        shortcut key combos for PTT
    """

    type: VoiceSettingsModeType
    auto_threshold: bool
    threshold: float
    shortcut: ShortcutKeyCombo
    delay: float


@dataclass
class VoiceSettingsUpdateEvent(APIObject):
    """
    Represents a user's voice settings
    
    :param input:
        input settings

    :param output:
        output settings

    :param mode:
        voice mode settings

    :param automatic_gain_control:
        state of automatic gain control

    :param echo_cancellation:
        state of echo cancellation

    :param noise_suppression:
        state of noise suppression

    :param qos:
        state of voice quality of service

    :param silence_warning:
        state of silence warning notice

    :param deaf:
        state of self-deafen

    :param mute:
        state of self-mute
    """

    input: VoiceSettingsInput
    output: VoiceSettingsOutput
    automatic_gain_control: bool
    echo_cancellation: bool
    noise_suppression: bool
    qos: bool
    silence_warning: bool
    deaf: bool
    mute: bool
