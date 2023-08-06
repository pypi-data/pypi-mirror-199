# ZankPy - Python Client Library for Zank Media Player

ZankPy is a Python client library designed to control a Zank Media Player by sending UDP commands. It simplifies the process of sending commands to the media player and can be integrated with Home Assistant.

## Features

- Simple and easy-to-use API
- Supports a wide range of commands for controlling the media player
- Compatible with Home Assistant custom components

## Installation

You can install the ZankPy library using pip:

```bash
pip install zankpy
```

## Usage

Here's a basic example of how to use the ZankPy library to control a Zank Media Player:

```python
from zankpy import ZankControlClient

client = ZankControlClient("192.168.1.100", 12345)  # Replace with the correct IP address and port number
client.send_command("home")
```

## Command List

Here is the list of supported commands:

- home
- back
- recent
- scrollUp
- scrollDown
- pageRight
- pageLeft
- volumeUp
- volumeDown
- volumeMute
- pageUp
- pageDown
- dpadUp
- dpadDown
- dpadLeft
- dpadRight
- dpadCenter
- dpadCenterLong
- openNotification
- takeScreenShot
- powerDialog
- lockScreen
- switchToTV
- mediaPrevious
- mediaNext
- mediaPlayPause
- channelUp
- channelDown
- fastRewind
- fastForward
- pressNumber 0-9
- pressMenu
- keycodeGuide
- click
- longClick

## License

This project is licensed under the MIT License. See the LICENSE file for details.
