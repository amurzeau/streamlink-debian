# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all modules.
#
# CDP version: v0.0.1359167
# CDP domain: Input

from __future__ import annotations

import enum
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

from streamlink.webbrowser.cdp.devtools.util import T_JSON_DICT, event_class


@dataclass
class TouchPoint:
    #: X coordinate of the event relative to the main frame's viewport in CSS pixels.
    x: float

    #: Y coordinate of the event relative to the main frame's viewport in CSS pixels. 0 refers to
    #: the top of the viewport and Y increases as it proceeds towards the bottom of the viewport.
    y: float

    #: X radius of the touch area (default: 1.0).
    radius_x: float | None = None

    #: Y radius of the touch area (default: 1.0).
    radius_y: float | None = None

    #: Rotation angle (default: 0.0).
    rotation_angle: float | None = None

    #: Force (default: 1.0).
    force: float | None = None

    #: The normalized tangential pressure, which has a range of [-1,1] (default: 0).
    tangential_pressure: float | None = None

    #: The plane angle between the Y-Z plane and the plane containing both the stylus axis and the Y axis, in degrees of the range [-90,90], a positive tiltX is to the right (default: 0)
    tilt_x: float | None = None

    #: The plane angle between the X-Z plane and the plane containing both the stylus axis and the X axis, in degrees of the range [-90,90], a positive tiltY is towards the user (default: 0).
    tilt_y: float | None = None

    #: The clockwise rotation of a pen stylus around its own major axis, in degrees in the range [0,359] (default: 0).
    twist: int | None = None

    #: Identifier used to track touch sources between events, must be unique within an event.
    id_: float | None = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = {}
        json["x"] = self.x
        json["y"] = self.y
        if self.radius_x is not None:
            json["radiusX"] = self.radius_x
        if self.radius_y is not None:
            json["radiusY"] = self.radius_y
        if self.rotation_angle is not None:
            json["rotationAngle"] = self.rotation_angle
        if self.force is not None:
            json["force"] = self.force
        if self.tangential_pressure is not None:
            json["tangentialPressure"] = self.tangential_pressure
        if self.tilt_x is not None:
            json["tiltX"] = self.tilt_x
        if self.tilt_y is not None:
            json["tiltY"] = self.tilt_y
        if self.twist is not None:
            json["twist"] = self.twist
        if self.id_ is not None:
            json["id"] = self.id_
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TouchPoint:
        return cls(
            x=float(json["x"]),
            y=float(json["y"]),
            radius_x=float(json["radiusX"]) if "radiusX" in json else None,
            radius_y=float(json["radiusY"]) if "radiusY" in json else None,
            rotation_angle=float(json["rotationAngle"]) if "rotationAngle" in json else None,
            force=float(json["force"]) if "force" in json else None,
            tangential_pressure=float(json["tangentialPressure"]) if "tangentialPressure" in json else None,
            tilt_x=float(json["tiltX"]) if "tiltX" in json else None,
            tilt_y=float(json["tiltY"]) if "tiltY" in json else None,
            twist=int(json["twist"]) if "twist" in json else None,
            id_=float(json["id"]) if "id" in json else None,
        )


class GestureSourceType(enum.Enum):
    DEFAULT = "default"
    TOUCH = "touch"
    MOUSE = "mouse"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> GestureSourceType:
        return cls(json)


class MouseButton(enum.Enum):
    NONE = "none"
    LEFT = "left"
    MIDDLE = "middle"
    RIGHT = "right"
    BACK = "back"
    FORWARD = "forward"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> MouseButton:
        return cls(json)


class TimeSinceEpoch(float):
    """
    UTC time in seconds, counted from January 1, 1970.
    """
    def to_json(self) -> float:
        return self

    @classmethod
    def from_json(cls, json: float) -> TimeSinceEpoch:
        return cls(json)

    def __repr__(self):
        return f"TimeSinceEpoch({super().__repr__()})"


@dataclass
class DragDataItem:
    #: Mime type of the dragged data.
    mime_type: str

    #: Depending of the value of ``mimeType``, it contains the dragged link,
    #: text, HTML markup or any other data.
    data: str

    #: Title associated with a link. Only valid when ``mimeType`` == "text/uri-list".
    title: str | None = None

    #: Stores the base URL for the contained markup. Only valid when ``mimeType``
    #: == "text/html".
    base_url: str | None = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = {}
        json["mimeType"] = self.mime_type
        json["data"] = self.data
        if self.title is not None:
            json["title"] = self.title
        if self.base_url is not None:
            json["baseURL"] = self.base_url
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DragDataItem:
        return cls(
            mime_type=str(json["mimeType"]),
            data=str(json["data"]),
            title=str(json["title"]) if "title" in json else None,
            base_url=str(json["baseURL"]) if "baseURL" in json else None,
        )


@dataclass
class DragData:
    items: list[DragDataItem]

    #: Bit field representing allowed drag operations. Copy = 1, Link = 2, Move = 16
    drag_operations_mask: int

    #: List of filenames that should be included when dropping
    files: list[str] | None = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = {}
        json["items"] = [i.to_json() for i in self.items]
        json["dragOperationsMask"] = self.drag_operations_mask
        if self.files is not None:
            json["files"] = list(self.files)
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DragData:
        return cls(
            items=[DragDataItem.from_json(i) for i in json["items"]],
            drag_operations_mask=int(json["dragOperationsMask"]),
            files=[str(i) for i in json["files"]] if "files" in json else None,
        )


def dispatch_drag_event(
    type_: str,
    x: float,
    y: float,
    data: DragData,
    modifiers: int | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Dispatches a drag event into the page.

    **EXPERIMENTAL**

    :param type_: Type of the drag event.
    :param x: X coordinate of the event relative to the main frame's viewport in CSS pixels.
    :param y: Y coordinate of the event relative to the main frame's viewport in CSS pixels. 0 refers to the top of the viewport and Y increases as it proceeds towards the bottom of the viewport.
    :param data:
    :param modifiers: *(Optional)* Bit field representing pressed modifier keys. Alt=1, Ctrl=2, Meta/Command=4, Shift=8 (default: 0).
    """
    params: T_JSON_DICT = {}
    params["type"] = type_
    params["x"] = x
    params["y"] = y
    params["data"] = data.to_json()
    if modifiers is not None:
        params["modifiers"] = modifiers
    cmd_dict: T_JSON_DICT = {
        "method": "Input.dispatchDragEvent",
        "params": params,
    }
    yield cmd_dict


def dispatch_key_event(
    type_: str,
    modifiers: int | None = None,
    timestamp: TimeSinceEpoch | None = None,
    text: str | None = None,
    unmodified_text: str | None = None,
    key_identifier: str | None = None,
    code: str | None = None,
    key: str | None = None,
    windows_virtual_key_code: int | None = None,
    native_virtual_key_code: int | None = None,
    auto_repeat: bool | None = None,
    is_keypad: bool | None = None,
    is_system_key: bool | None = None,
    location: int | None = None,
    commands: list[str] | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Dispatches a key event to the page.

    :param type_: Type of the key event.
    :param modifiers: *(Optional)* Bit field representing pressed modifier keys. Alt=1, Ctrl=2, Meta/Command=4, Shift=8 (default: 0).
    :param timestamp: *(Optional)* Time at which the event occurred.
    :param text: *(Optional)* Text as generated by processing a virtual key code with a keyboard layout. Not needed for for ```keyUp```` and ````rawKeyDown```` events (default: "")
    :param unmodified_text: *(Optional)* Text that would have been generated by the keyboard if no modifiers were pressed (except for shift). Useful for shortcut (accelerator) key handling (default: "").
    :param key_identifier: *(Optional)* Unique key identifier (e.g., 'U+0041') (default: "").
    :param code: *(Optional)* Unique DOM defined string value for each physical key (e.g., 'KeyA') (default: "").
    :param key: *(Optional)* Unique DOM defined string value describing the meaning of the key in the context of active modifiers, keyboard layout, etc (e.g., 'AltGr') (default: "").
    :param windows_virtual_key_code: *(Optional)* Windows virtual key code (default: 0).
    :param native_virtual_key_code: *(Optional)* Native virtual key code (default: 0).
    :param auto_repeat: *(Optional)* Whether the event was generated from auto repeat (default: false).
    :param is_keypad: *(Optional)* Whether the event was generated from the keypad (default: false).
    :param is_system_key: *(Optional)* Whether the event was a system key event (default: false).
    :param location: *(Optional)* Whether the event was from the left or right side of the keyboard. 1=Left, 2=Right (default: 0).
    :param commands: **(EXPERIMENTAL)** *(Optional)* Editing commands to send with the key event (e.g., 'selectAll') (default: []). These are related to but not equal the command names used in ````document.execCommand``` and NSStandardKeyBindingResponding. See https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/editing/commands/editor_command_names.h for valid command names.
    """
    params: T_JSON_DICT = {}
    params["type"] = type_
    if modifiers is not None:
        params["modifiers"] = modifiers
    if timestamp is not None:
        params["timestamp"] = timestamp.to_json()
    if text is not None:
        params["text"] = text
    if unmodified_text is not None:
        params["unmodifiedText"] = unmodified_text
    if key_identifier is not None:
        params["keyIdentifier"] = key_identifier
    if code is not None:
        params["code"] = code
    if key is not None:
        params["key"] = key
    if windows_virtual_key_code is not None:
        params["windowsVirtualKeyCode"] = windows_virtual_key_code
    if native_virtual_key_code is not None:
        params["nativeVirtualKeyCode"] = native_virtual_key_code
    if auto_repeat is not None:
        params["autoRepeat"] = auto_repeat
    if is_keypad is not None:
        params["isKeypad"] = is_keypad
    if is_system_key is not None:
        params["isSystemKey"] = is_system_key
    if location is not None:
        params["location"] = location
    if commands is not None:
        params["commands"] = list(commands)
    cmd_dict: T_JSON_DICT = {
        "method": "Input.dispatchKeyEvent",
        "params": params,
    }
    yield cmd_dict


def insert_text(
    text: str,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    This method emulates inserting text that doesn't come from a key press,
    for example an emoji keyboard or an IME.

    **EXPERIMENTAL**

    :param text: The text to insert.
    """
    params: T_JSON_DICT = {}
    params["text"] = text
    cmd_dict: T_JSON_DICT = {
        "method": "Input.insertText",
        "params": params,
    }
    yield cmd_dict


def ime_set_composition(
    text: str,
    selection_start: int,
    selection_end: int,
    replacement_start: int | None = None,
    replacement_end: int | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    This method sets the current candidate text for IME.
    Use imeCommitComposition to commit the final text.
    Use imeSetComposition with empty string as text to cancel composition.

    **EXPERIMENTAL**

    :param text: The text to insert
    :param selection_start: selection start
    :param selection_end: selection end
    :param replacement_start: *(Optional)* replacement start
    :param replacement_end: *(Optional)* replacement end
    """
    params: T_JSON_DICT = {}
    params["text"] = text
    params["selectionStart"] = selection_start
    params["selectionEnd"] = selection_end
    if replacement_start is not None:
        params["replacementStart"] = replacement_start
    if replacement_end is not None:
        params["replacementEnd"] = replacement_end
    cmd_dict: T_JSON_DICT = {
        "method": "Input.imeSetComposition",
        "params": params,
    }
    yield cmd_dict


def dispatch_mouse_event(
    type_: str,
    x: float,
    y: float,
    modifiers: int | None = None,
    timestamp: TimeSinceEpoch | None = None,
    button: MouseButton | None = None,
    buttons: int | None = None,
    click_count: int | None = None,
    force: float | None = None,
    tangential_pressure: float | None = None,
    tilt_x: float | None = None,
    tilt_y: float | None = None,
    twist: int | None = None,
    delta_x: float | None = None,
    delta_y: float | None = None,
    pointer_type: str | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Dispatches a mouse event to the page.

    :param type_: Type of the mouse event.
    :param x: X coordinate of the event relative to the main frame's viewport in CSS pixels.
    :param y: Y coordinate of the event relative to the main frame's viewport in CSS pixels. 0 refers to the top of the viewport and Y increases as it proceeds towards the bottom of the viewport.
    :param modifiers: *(Optional)* Bit field representing pressed modifier keys. Alt=1, Ctrl=2, Meta/Command=4, Shift=8 (default: 0).
    :param timestamp: *(Optional)* Time at which the event occurred.
    :param button: *(Optional)* Mouse button (default: "none").
    :param buttons: *(Optional)* A number indicating which buttons are pressed on the mouse when a mouse event is triggered. Left=1, Right=2, Middle=4, Back=8, Forward=16, None=0.
    :param click_count: *(Optional)* Number of times the mouse button was clicked (default: 0).
    :param force: **(EXPERIMENTAL)** *(Optional)* The normalized pressure, which has a range of [0,1] (default: 0).
    :param tangential_pressure: **(EXPERIMENTAL)** *(Optional)* The normalized tangential pressure, which has a range of [-1,1] (default: 0).
    :param tilt_x: *(Optional)* The plane angle between the Y-Z plane and the plane containing both the stylus axis and the Y axis, in degrees of the range [-90,90], a positive tiltX is to the right (default: 0).
    :param tilt_y: *(Optional)* The plane angle between the X-Z plane and the plane containing both the stylus axis and the X axis, in degrees of the range [-90,90], a positive tiltY is towards the user (default: 0).
    :param twist: **(EXPERIMENTAL)** *(Optional)* The clockwise rotation of a pen stylus around its own major axis, in degrees in the range [0,359] (default: 0).
    :param delta_x: *(Optional)* X delta in CSS pixels for mouse wheel event (default: 0).
    :param delta_y: *(Optional)* Y delta in CSS pixels for mouse wheel event (default: 0).
    :param pointer_type: *(Optional)* Pointer type (default: "mouse").
    """
    params: T_JSON_DICT = {}
    params["type"] = type_
    params["x"] = x
    params["y"] = y
    if modifiers is not None:
        params["modifiers"] = modifiers
    if timestamp is not None:
        params["timestamp"] = timestamp.to_json()
    if button is not None:
        params["button"] = button.to_json()
    if buttons is not None:
        params["buttons"] = buttons
    if click_count is not None:
        params["clickCount"] = click_count
    if force is not None:
        params["force"] = force
    if tangential_pressure is not None:
        params["tangentialPressure"] = tangential_pressure
    if tilt_x is not None:
        params["tiltX"] = tilt_x
    if tilt_y is not None:
        params["tiltY"] = tilt_y
    if twist is not None:
        params["twist"] = twist
    if delta_x is not None:
        params["deltaX"] = delta_x
    if delta_y is not None:
        params["deltaY"] = delta_y
    if pointer_type is not None:
        params["pointerType"] = pointer_type
    cmd_dict: T_JSON_DICT = {
        "method": "Input.dispatchMouseEvent",
        "params": params,
    }
    yield cmd_dict


def dispatch_touch_event(
    type_: str,
    touch_points: list[TouchPoint],
    modifiers: int | None = None,
    timestamp: TimeSinceEpoch | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Dispatches a touch event to the page.

    :param type_: Type of the touch event. TouchEnd and TouchCancel must not contain any touch points, while TouchStart and TouchMove must contains at least one.
    :param touch_points: Active touch points on the touch device. One event per any changed point (compared to previous touch event in a sequence) is generated, emulating pressing/moving/releasing points one by one.
    :param modifiers: *(Optional)* Bit field representing pressed modifier keys. Alt=1, Ctrl=2, Meta/Command=4, Shift=8 (default: 0).
    :param timestamp: *(Optional)* Time at which the event occurred.
    """
    params: T_JSON_DICT = {}
    params["type"] = type_
    params["touchPoints"] = [i.to_json() for i in touch_points]
    if modifiers is not None:
        params["modifiers"] = modifiers
    if timestamp is not None:
        params["timestamp"] = timestamp.to_json()
    cmd_dict: T_JSON_DICT = {
        "method": "Input.dispatchTouchEvent",
        "params": params,
    }
    yield cmd_dict


def cancel_dragging() -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Cancels any active dragging in the page.
    """
    cmd_dict: T_JSON_DICT = {
        "method": "Input.cancelDragging",
    }
    yield cmd_dict


def emulate_touch_from_mouse_event(
    type_: str,
    x: int,
    y: int,
    button: MouseButton,
    timestamp: TimeSinceEpoch | None = None,
    delta_x: float | None = None,
    delta_y: float | None = None,
    modifiers: int | None = None,
    click_count: int | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Emulates touch event from the mouse event parameters.

    **EXPERIMENTAL**

    :param type_: Type of the mouse event.
    :param x: X coordinate of the mouse pointer in DIP.
    :param y: Y coordinate of the mouse pointer in DIP.
    :param button: Mouse button. Only "none", "left", "right" are supported.
    :param timestamp: *(Optional)* Time at which the event occurred (default: current time).
    :param delta_x: *(Optional)* X delta in DIP for mouse wheel event (default: 0).
    :param delta_y: *(Optional)* Y delta in DIP for mouse wheel event (default: 0).
    :param modifiers: *(Optional)* Bit field representing pressed modifier keys. Alt=1, Ctrl=2, Meta/Command=4, Shift=8 (default: 0).
    :param click_count: *(Optional)* Number of times the mouse button was clicked (default: 0).
    """
    params: T_JSON_DICT = {}
    params["type"] = type_
    params["x"] = x
    params["y"] = y
    params["button"] = button.to_json()
    if timestamp is not None:
        params["timestamp"] = timestamp.to_json()
    if delta_x is not None:
        params["deltaX"] = delta_x
    if delta_y is not None:
        params["deltaY"] = delta_y
    if modifiers is not None:
        params["modifiers"] = modifiers
    if click_count is not None:
        params["clickCount"] = click_count
    cmd_dict: T_JSON_DICT = {
        "method": "Input.emulateTouchFromMouseEvent",
        "params": params,
    }
    yield cmd_dict


def set_ignore_input_events(
    ignore: bool,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Ignores input events (useful while auditing page).

    :param ignore: Ignores input events processing when set to true.
    """
    params: T_JSON_DICT = {}
    params["ignore"] = ignore
    cmd_dict: T_JSON_DICT = {
        "method": "Input.setIgnoreInputEvents",
        "params": params,
    }
    yield cmd_dict


def set_intercept_drags(
    enabled: bool,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Prevents default drag and drop behavior and instead emits ``Input.dragIntercepted`` events.
    Drag and drop behavior can be directly controlled via ``Input.dispatchDragEvent``.

    **EXPERIMENTAL**

    :param enabled:
    """
    params: T_JSON_DICT = {}
    params["enabled"] = enabled
    cmd_dict: T_JSON_DICT = {
        "method": "Input.setInterceptDrags",
        "params": params,
    }
    yield cmd_dict


def synthesize_pinch_gesture(
    x: float,
    y: float,
    scale_factor: float,
    relative_speed: int | None = None,
    gesture_source_type: GestureSourceType | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Synthesizes a pinch gesture over a time period by issuing appropriate touch events.

    **EXPERIMENTAL**

    :param x: X coordinate of the start of the gesture in CSS pixels.
    :param y: Y coordinate of the start of the gesture in CSS pixels.
    :param scale_factor: Relative scale factor after zooming (>1.0 zooms in, <1.0 zooms out).
    :param relative_speed: *(Optional)* Relative pointer speed in pixels per second (default: 800).
    :param gesture_source_type: *(Optional)* Which type of input events to be generated (default: 'default', which queries the platform for the preferred input type).
    """
    params: T_JSON_DICT = {}
    params["x"] = x
    params["y"] = y
    params["scaleFactor"] = scale_factor
    if relative_speed is not None:
        params["relativeSpeed"] = relative_speed
    if gesture_source_type is not None:
        params["gestureSourceType"] = gesture_source_type.to_json()
    cmd_dict: T_JSON_DICT = {
        "method": "Input.synthesizePinchGesture",
        "params": params,
    }
    yield cmd_dict


def synthesize_scroll_gesture(
    x: float,
    y: float,
    x_distance: float | None = None,
    y_distance: float | None = None,
    x_overscroll: float | None = None,
    y_overscroll: float | None = None,
    prevent_fling: bool | None = None,
    speed: int | None = None,
    gesture_source_type: GestureSourceType | None = None,
    repeat_count: int | None = None,
    repeat_delay_ms: int | None = None,
    interaction_marker_name: str | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Synthesizes a scroll gesture over a time period by issuing appropriate touch events.

    **EXPERIMENTAL**

    :param x: X coordinate of the start of the gesture in CSS pixels.
    :param y: Y coordinate of the start of the gesture in CSS pixels.
    :param x_distance: *(Optional)* The distance to scroll along the X axis (positive to scroll left).
    :param y_distance: *(Optional)* The distance to scroll along the Y axis (positive to scroll up).
    :param x_overscroll: *(Optional)* The number of additional pixels to scroll back along the X axis, in addition to the given distance.
    :param y_overscroll: *(Optional)* The number of additional pixels to scroll back along the Y axis, in addition to the given distance.
    :param prevent_fling: *(Optional)* Prevent fling (default: true).
    :param speed: *(Optional)* Swipe speed in pixels per second (default: 800).
    :param gesture_source_type: *(Optional)* Which type of input events to be generated (default: 'default', which queries the platform for the preferred input type).
    :param repeat_count: *(Optional)* The number of times to repeat the gesture (default: 0).
    :param repeat_delay_ms: *(Optional)* The number of milliseconds delay between each repeat. (default: 250).
    :param interaction_marker_name: *(Optional)* The name of the interaction markers to generate, if not empty (default: "").
    """
    params: T_JSON_DICT = {}
    params["x"] = x
    params["y"] = y
    if x_distance is not None:
        params["xDistance"] = x_distance
    if y_distance is not None:
        params["yDistance"] = y_distance
    if x_overscroll is not None:
        params["xOverscroll"] = x_overscroll
    if y_overscroll is not None:
        params["yOverscroll"] = y_overscroll
    if prevent_fling is not None:
        params["preventFling"] = prevent_fling
    if speed is not None:
        params["speed"] = speed
    if gesture_source_type is not None:
        params["gestureSourceType"] = gesture_source_type.to_json()
    if repeat_count is not None:
        params["repeatCount"] = repeat_count
    if repeat_delay_ms is not None:
        params["repeatDelayMs"] = repeat_delay_ms
    if interaction_marker_name is not None:
        params["interactionMarkerName"] = interaction_marker_name
    cmd_dict: T_JSON_DICT = {
        "method": "Input.synthesizeScrollGesture",
        "params": params,
    }
    yield cmd_dict


def synthesize_tap_gesture(
    x: float,
    y: float,
    duration: int | None = None,
    tap_count: int | None = None,
    gesture_source_type: GestureSourceType | None = None,
) -> Generator[T_JSON_DICT, T_JSON_DICT, None]:
    """
    Synthesizes a tap gesture over a time period by issuing appropriate touch events.

    **EXPERIMENTAL**

    :param x: X coordinate of the start of the gesture in CSS pixels.
    :param y: Y coordinate of the start of the gesture in CSS pixels.
    :param duration: *(Optional)* Duration between touchdown and touchup events in ms (default: 50).
    :param tap_count: *(Optional)* Number of times to perform the tap (e.g. 2 for double tap, default: 1).
    :param gesture_source_type: *(Optional)* Which type of input events to be generated (default: 'default', which queries the platform for the preferred input type).
    """
    params: T_JSON_DICT = {}
    params["x"] = x
    params["y"] = y
    if duration is not None:
        params["duration"] = duration
    if tap_count is not None:
        params["tapCount"] = tap_count
    if gesture_source_type is not None:
        params["gestureSourceType"] = gesture_source_type.to_json()
    cmd_dict: T_JSON_DICT = {
        "method": "Input.synthesizeTapGesture",
        "params": params,
    }
    yield cmd_dict


@event_class("Input.dragIntercepted")
@dataclass
class DragIntercepted:
    """
    **EXPERIMENTAL**

    Emitted only when ``Input.setInterceptDrags`` is enabled. Use this data with ``Input.dispatchDragEvent`` to
    restore normal drag and drop behavior.
    """
    data: DragData

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DragIntercepted:
        return cls(
            data=DragData.from_json(json["data"]),
        )
