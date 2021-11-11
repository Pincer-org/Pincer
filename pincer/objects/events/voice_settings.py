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
    Represents an available device for voice settings

    Attributes
    ----------
    id : :class:`str`
        id of the available device

    name : :class:`str`
        name of the available device
    """

    id: str
    name: str


@dataclass
class VoiceSettingsInput(APIObject):
    """
    Represents a voice setting input object

    Attributes
    ----------
    device_id : :class:`str`
        the device's id

    volume : :class:`float`
        input voice level (min: 0, max: 100)

    available_devices : List[:class:`AvailableDevices`]
        array of read-only device objects containing id and name string keys
    """

    device_id: str
    volume: float
    available_devices: List[AvailableDevices]


@dataclass
class VoiceSettingsOutput(APIObject):
    """
    Represents a voice setting output object

    Attributes
    ----------
    device_id : :class:`str`
        the device's id

    volume : :class:`float`
        input voice level (min: 0, max: 100)

    available_devices : List[:class:`AvailableDevices`]
        array of read-only device objects containing id and name string keys
    """

    device_id: str
    volume: float
    available_devices: List[AvailableDevices]


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

    Attributes
    ----------
    type : :class:`KeyTypes`
        type of shortcut key combo

    code : :class:`str`
        key code

    name : :class:`str`
        key name
    """

    type: KeyTypes
    code: int
    name: str


@dataclass
class VoiceSettingsMode(APIObject):
    """
    Represents the voice mode settings from a user

    Attributes
    ----------
    type : :class:`VoiceSettingsModeType`
        voice setting mode type

    auto_threshold : :class:`bool`
        voice activity threshold automatically sets its threshold

    threshold : :class:`float`
        threshold for voice activity (in dB)

    shortcut : :class:`ShortcutKeyCombo`
        shortcut key combos for PTT

    delay : :class:`float`
        the PTT release delay (in ms) (min: 0, max: 2000)
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

    Attributes
    ----------
    input : :class:`VoiceSettingsInput`
        input settings

    output : :class:`VoiceSettingsOutput`
        output settings

    mode : :class:`bool`
        voice mode settings

    automatic_gain_control : :class:`bool`
        state of automatic gain control

    echo_cancellation : :class:`bool`
        state of echo cancellation

    noise_suppression : :class:`bool`
        state of noise suppression

    qos : :class:`bool`
        state of voice quality of service

    silence_warning : :class:`bool`
        state of silence warning notice

    deaf : :class:`bool`
        state of self-deafen

    mute : :class:`bool`
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
