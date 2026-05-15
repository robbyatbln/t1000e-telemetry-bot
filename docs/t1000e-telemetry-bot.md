# SenseCAP T1000-E Telemetry Bot Firmware

This fork adds a telemetry bot mode to the MeshCore BLE companion firmware for the Seeed Studio SenseCAP T1000-E.

The firmware periodically sends visible group chat messages with selected telemetry fields and can be controlled by direct messages.

## Features

- Periodic telemetry messages to a configurable MeshCore group.
- Direct-message control with acknowledgements.
- Configurable message label, group name, interval, and telemetry fields.
- Google Maps links for GPS coordinates.
- Optional zero-hop advert after each telemetry push.
- Buzzer mute/unmute by direct message.
- Find-device sound by direct message.

## Firmware Files

Prebuilt firmware artifacts are in the `firmware/` folder:

- `t1000e_companion_radio_ble-telemetry-bot.zip` for the MeshCore/Web nRF flasher.
- `t1000e_companion_radio_ble-telemetry-bot.uf2` for drag-and-drop flashing in DFU mode.

Use the ZIP with web flashing. Use the UF2 only when the T1000-E appears as a DFU mass-storage drive.

## Flashing

### Option A: Web Flasher

1. Put the T1000-E into DFU/bootloader mode.
2. Open the MeshCore flasher.
3. Choose the custom firmware ZIP from `firmware/t1000e_companion_radio_ble-telemetry-bot.zip`.
4. Flash and wait until the device reboots.

### Option B: UF2 Drag-and-Drop

1. Put the T1000-E into DFU/bootloader mode.
2. Wait until the T1000-E DFU drive appears.
3. Copy `firmware/t1000e_companion_radio_ble-telemetry-bot.uf2` onto that drive.
4. Wait for the device to reboot.

## Default Behavior

Default build settings for the T1000-E BLE companion target:

- Target group: `Robbys_channel`
- Interval: 5 minutes
- Command prefix: `config`
- Message label: `Telemetry`
- Fields: battery, GPS, temperature, light

The group must exist on the device and the group name must match exactly.

## Direct Message Commands

Send these as direct messages to the T1000-E node.

| Command | Effect |
| --- | --- |
| `config help` | Sends a short command list as a direct reply. |
| `config status` | Sends current settings as a direct reply. |
| `config start` | Enables periodic telemetry. First message is sent after about 3 seconds. |
| `config stop` | Disables periodic telemetry. |
| `config group Robbys_channel` | Sets the target group by name. |
| `config interval 5` | Sets the interval in minutes. Use `0` to disable timer scheduling. |
| `config label test` | Sets the first word of every outgoing telemetry message. |
| `config all` | Enables all telemetry fields. |
| `config gps akku temp licht` | Selects GPS, battery, temperature, and light fields. |
| `config sound off` | Mutes normal buzzer notifications. |
| `config sound on` | Enables normal buzzer notifications. |
| `config wo ist` | Plays a find-device sound even if normal sound is muted. |
| `config prefix xy` | Changes the command prefix from `config` to `xy`. |

After changing the prefix, commands must use the new prefix, for example:

```text
xy help
xy stop
xy label tracker
```

## Example Messages

With default settings:

```text
Telemetry: Akku 3.95V Temp 24.1C Licht 42% GPS https://maps.google.com/?q=52.123456,13.123456
```

After:

```text
config label test
config gps akku
```

The group message becomes:

```text
test: Akku 3.95V GPS https://maps.google.com/?q=52.123456,13.123456
```

## Build From Source

Install PlatformIO, then build the T1000-E BLE companion target:

```powershell
$env:PLATFORMIO_CORE_DIR='X:\.platformio'
python -m platformio run -e t1000e_companion_radio_ble
```

On Windows, a short workspace path is recommended because the nRF52 ARM toolchain can hit path-length issues. One workaround is:

```powershell
subst X: 'C:\path\to\workspace'
cd X:\MeshCore
$env:PLATFORMIO_CORE_DIR='X:\.platformio'
python -m platformio run -e t1000e_companion_radio_ble
```

Create a UF2 after a successful build:

```powershell
python bin\uf2conv\uf2conv.py .pio\build\t1000e_companion_radio_ble\firmware.hex -c -o .pio\build\t1000e_companion_radio_ble\firmware.uf2 -f 0xADA52840
```

## Modified Areas

The implementation is intentionally scoped to the companion radio firmware and T1000-E BLE target:

- `examples/companion_radio/MyMesh.cpp`
- `examples/companion_radio/MyMesh.h`
- `examples/companion_radio/NodePrefs.h`
- `examples/companion_radio/DataStore.cpp`
- `examples/companion_radio/AbstractUITask.h`
- `examples/companion_radio/ui-orig/UITask.cpp`
- `examples/companion_radio/ui-orig/UITask.h`
- `variants/t1000-e/platformio.ini`

## Notes

- This is a custom firmware fork, not an official MeshCore release.
- Flash only firmware built for the Seeed Studio SenseCAP T1000-E.
- Group names are case-sensitive.
- GPS coordinates are only useful after the GPS has a valid fix.
- The Find sound is intended for nearby recovery, not remote location tracking.
