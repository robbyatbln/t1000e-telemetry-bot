# SenseCAP T1000-E Telemetry Bot Firmware

## Deutsche Kurzbeschreibung

Diese Firmware ist eine angepasste MeshCore BLE Companion Firmware fuer den Seeed Studio SenseCAP T1000-E. Sie ist fuer Leute gedacht, die MeshCore bereits nutzen und den T1000-E als automatischen Telemetrie-Sender in einer MeshCore-Gruppe betreiben wollen.

Die Firmware bleibt grundsaetzlich eine normale MeshCore Companion Firmware: Verbindung per Android/iOS/Web-App, Gruppen, Kontakte, Region und normale Nachrichten funktionieren weiterhin wie gewohnt. Zusaetzlich gibt es einen Telemetrie-Bot, der per Direktnachricht gesteuert wird.

## Unterschiede zur normalen MeshCore T1000-E Firmware

| Bereich | Normale MeshCore T1000-E Companion Firmware | Diese Telemetry-Bot Firmware |
| --- | --- | --- |
| Telemetrie | Telemetrie kann abgefragt werden, wird aber nicht automatisch als Chattext in eine Gruppe geschrieben. | Sendet Akku, GPS, Temperatur und Licht automatisch als sichtbare Gruppennachricht. |
| Steuerung | Einstellungen hauptsaechlich ueber App/Companion-Protokoll. | Start, Stop, Status und Konfiguration per Direktnachricht, z. B. `config start`. |
| Zielgruppe | Keine feste automatische Telemetrie-Zielgruppe. | Zielgruppe per Name konfigurierbar, z. B. `config group Robbys_channel`. |
| Nachrichtentext | Keine automatische Chat-Nachricht mit Sensorwerten. | Erstes Wort/Label konfigurierbar, z. B. `config label tracker`. |
| GPS | Positionsdaten koennen im MeshCore-Kontext genutzt werden. | GPS wird optional als Google-Maps-Link in die Gruppennachricht geschrieben. |
| Intervall | Kein automatischer 5-Minuten-Gruppenpush. | Intervall per Direktnachricht einstellbar, z. B. `config interval 5`. |
| Felder | Keine Chat-Auswahl per Textbefehl. | Felder per Direktnachricht waehlbar: `gps`, `akku`, `temp`, `licht`, `all`. |
| Quittung | Keine Bot-artige Rueckmeldung auf solche Befehle. | Jeder erkannte Befehl wird per Direktnachricht bestaetigt. |
| Suchton | Standard-Buzzer-Sounds je nach UI/Build. | `config wo ist` spielt ein Suchsignal am Geraet. |
| Tonsteuerung | Buzzer kann lokal/UI-abhaengig gesteuert werden. | `config sound off` und `config sound on` per Direktnachricht. |

## Wofuer ist diese Firmware gedacht?

- T1000-E am Rucksack, Fahrrad, Auto, Werkzeugkoffer oder an einer mobilen Station.
- Regelmaessige Statusmeldung in eine MeshCore-Gruppe.
- Schnelles Wiederfinden in der Naehe per `config wo ist`.
- Einfache Fernsteuerung ohne neue Android-App und ohne Custom-Var-Menue.

## Fertige Firmware-Dateien

Im Ordner `firmware/` liegen zwei Dateien:

- `t1000e_companion_radio_ble-telemetry-bot.zip` fuer den MeshCore/Web nRF Flasher.
- `t1000e_companion_radio_ble-telemetry-bot.uf2` fuer Drag-and-Drop im DFU-Laufwerk.

Wichtig: Im Web-Flasher die ZIP-Datei verwenden. Die UF2-Datei nur direkt auf das DFU-Laufwerk kopieren.

## Flashen

### Variante A: Web-Flasher

1. T1000-E in den DFU/Bootloader-Modus bringen.
2. MeshCore/Web-Flasher oeffnen.
3. Als Custom Firmware die Datei `firmware/t1000e_companion_radio_ble-telemetry-bot.zip` auswaehlen.
4. Flashen und den Neustart abwarten.

### Variante B: UF2 per Drag-and-Drop

1. T1000-E in den DFU/Bootloader-Modus bringen.
2. Warten, bis das T1000-E-Laufwerk erscheint.
3. `firmware/t1000e_companion_radio_ble-telemetry-bot.uf2` auf dieses Laufwerk kopieren.
4. Neustart abwarten.

## Standardverhalten

Im aktuellen Build sind diese Defaults gesetzt:

- Zielgruppe: `Robbys_channel`
- Intervall: 5 Minuten
- Befehlswort: `config`
- Nachrichten-Label: `Telemetry`
- Felder: Akku, GPS, Temperatur, Licht

Die Zielgruppe muss auf dem Geraet existieren und exakt gleich geschrieben sein.

## Befehle per Direktnachricht

Alle Befehle werden als Direktnachricht an den T1000-E gesendet. Jeder erkannte Befehl wird ebenfalls per Direktnachricht bestaetigt.

| Befehl | Wirkung |
| --- | --- |
| `config help` | Gibt eine kurze Befehlsuebersicht zurueck. |
| `config status` | Gibt aktuelle Einstellungen zurueck. |
| `config start` | Startet den periodischen Versand. Erste Meldung nach ca. 3 Sekunden. |
| `config stop` | Stoppt den periodischen Versand. |
| `config group Robbys_channel` | Setzt die Zielgruppe. |
| `config interval 5` | Setzt das Intervall in Minuten. |
| `config label test` | Setzt das erste Wort der Gruppennachricht, z. B. `test:`. |
| `config all` | Aktiviert alle Felder. |
| `config gps akku temp licht` | Aktiviert genau diese Felder. |
| `config sound off` | Deaktiviert normale Tonsignale. |
| `config sound on` | Aktiviert normale Tonsignale. |
| `config wo ist` | Spielt ein Suchsignal am Geraet ab. |
| `config prefix xy` | Aendert das Befehlswort von `config` auf `xy`. |

Nach `config prefix xy` muessen weitere Befehle mit `xy` beginnen:

```text
xy help
xy status
xy stop
xy label tracker
```

## Beispiele

Standardmeldung:

```text
Telemetry: Akku 3.95V Temp 24.1C Licht 42% GPS https://maps.google.com/?q=52.123456,13.123456
```

Label und Felder aendern:

```text
config label test
config gps akku
```

Danach sendet die Gruppe z. B.:

```text
test: Akku 3.95V GPS https://maps.google.com/?q=52.123456,13.123456
```

Geraet stumm schalten, aber trotzdem finden:

```text
config sound off
config wo ist
```

## Build aus dem Quellcode

PlatformIO installieren und dann das T1000-E BLE Companion Target bauen:

```powershell
$env:PLATFORMIO_CORE_DIR='X:\.platformio'
python -m platformio run -e t1000e_companion_radio_ble
```

Unter Windows ist ein kurzer Pfad empfehlenswert, weil die nRF52-Toolchain sonst Pfadlaengenprobleme bekommen kann:

```powershell
subst X: 'C:\path\to\workspace'
cd X:\MeshCore
$env:PLATFORMIO_CORE_DIR='X:\.platformio'
python -m platformio run -e t1000e_companion_radio_ble
```

UF2 erzeugen:

```powershell
python bin\uf2conv\uf2conv.py .pio\build\t1000e_companion_radio_ble\firmware.hex -c -o .pio\build\t1000e_companion_radio_ble\firmware.uf2 -f 0xADA52840
```

## Geaenderte Bereiche

- `examples/companion_radio/MyMesh.cpp`
- `examples/companion_radio/MyMesh.h`
- `examples/companion_radio/NodePrefs.h`
- `examples/companion_radio/DataStore.cpp`
- `examples/companion_radio/AbstractUITask.h`
- `examples/companion_radio/ui-orig/UITask.cpp`
- `examples/companion_radio/ui-orig/UITask.h`
- `variants/t1000-e/platformio.ini`

## Hinweise

- Dies ist ein Custom-Fork, keine offizielle MeshCore-Release.
- Nur auf dem Seeed Studio SenseCAP T1000-E verwenden.
- Gruppennamen sind case-sensitive.
- GPS ist erst sinnvoll, wenn das Geraet einen Fix hat.
- `config wo ist` ist zum Finden in der Naehe gedacht, nicht als Apple-Find-My-Ersatz.

---

## English Summary

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
