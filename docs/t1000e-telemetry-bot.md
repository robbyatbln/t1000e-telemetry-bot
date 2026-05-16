# SenseCAP T1000-E Telemetry Bot Firmware

## Deutsche Kurzbeschreibung

Diese Firmware ist eine angepasste MeshCore BLE Companion Firmware fuer den Seeed Studio SenseCAP T1000-E. Sie ist fuer Leute gedacht, die MeshCore bereits nutzen und den T1000-E als einfachen Tracker einsetzen wollen, zum Beispiel fuer Kinder, Tiere, Gruppen auf Veranstaltungen, Treffen im Park oder andere Situationen, in denen man ohne Mobilfunknetz sehen moechte, wo etwas oder jemand gerade ist.

Die Firmware bleibt grundsaetzlich eine normale MeshCore Companion Firmware: Verbindung per Android/iOS/Web-App, Gruppen, Kontakte, Region und normale Nachrichten funktionieren weiterhin wie gewohnt. Zusaetzlich gibt es eine Tracking-Funktion, die Akku, Position und Sensorwerte regelmaessig in eine ausgewaehlte MeshCore-Gruppe schreibt und per Direktnachricht gesteuert wird.

## Unterschiede zur normalen MeshCore T1000-E Firmware

| Bereich | Normale MeshCore T1000-E Companion Firmware | Diese Telemetry-Bot Firmware |
| --- | --- | --- |
| Telemetrie | Telemetrie kann abgefragt werden, wird aber nicht automatisch als Chattext verschickt. | Sendet Akku, GPS, Temperatur und Licht automatisch, standardmaessig als private Direktnachricht. |
| Steuerung | Einstellungen hauptsaechlich ueber App/Companion-Protokoll. | Start, Stop, Status und Konfiguration per Direktnachricht, z. B. `config start`. |
| Zielgruppe | Keine feste automatische Telemetrie-Zielgruppe. | Standard ist Direct an den steuernden Kontakt. Flood in einen privaten Kanal muss bewusst aktiviert werden. |
| Nachrichtentext | Keine automatische Chat-Nachricht mit Sensorwerten. | Erstes Wort/Label konfigurierbar, z. B. `config label tracker`. |
| GPS | Positionsdaten koennen im MeshCore-Kontext genutzt werden. | GPS wird optional als Google-Maps-Link in die Telemetrie-Nachricht geschrieben. |
| Intervall | Kein automatischer Telemetrie-Push. | Intervall per Direktnachricht einstellbar, mindestens 10 Minuten. |
| Felder | Keine Chat-Auswahl per Textbefehl. | Felder per Direktnachricht waehlbar: `gps`, `akku`, `temp`, `licht`, `all`. |
| Quittung | Keine Bot-artige Rueckmeldung auf solche Befehle. | Jeder erkannte Befehl wird per Direktnachricht bestaetigt. |
| Suchton | Standard-Buzzer-Sounds je nach UI/Build. | `config wo ist` spielt ein Suchsignal am Geraet. |
| Tonsteuerung | Buzzer kann lokal/UI-abhaengig gesteuert werden. | `config sound off` und `config sound on` per Direktnachricht. |
| Bluetooth | BLE bleibt normalerweise fuer die App verfuegbar. | BLE kann nach 10 Minuten ohne Verbindung automatisch abschalten und per Direktnachricht wieder eingeschaltet werden. |
| Taste | Standard-UI-Funktionen je nach Build. | Einmaliges Druecken sendet sofort eine Telemetrie-Nachricht mit der aktuellen Konfiguration. |

## Wofuer ist diese Firmware gedacht?

- T1000-E am Rucksack eines Kindes, am Tierhalsband, Fahrrad, Auto, Werkzeugkoffer oder an einer mobilen Station.
- Veranstaltungen, Parktreffen, Camps oder andere Orte, an denen eine Gruppe ohne Mobilfunknetz grob sehen moechte, wo jemand oder etwas ist.
- Regelmaessige private Standort- und Statusmeldung an einen MeshCore-Kontakt.
- Optionaler Flood-Versand in einen privaten MeshCore-Kanal, wenn eine Gruppe es bewusst sehen soll.
- Schnelles Wiederfinden in der Naehe per `config wo ist`.
- Einfache Fernsteuerung ohne neue Android-App und ohne Custom-Var-Menue.

## Fertige Firmware-Dateien

Im Ordner `firmware/` liegen zwei Dateien:

- `t1000e_companion_radio_ble-telemetry-bot.zip` fuer den MeshCore/Web nRF Flasher.
- `t1000e_companion_radio_ble-telemetry-bot.uf2` fuer Drag-and-Drop im DFU-Laufwerk.
- `t1000e_companion_radio_ble-telemetry-bot-v2.zip` als Folgeversion mit Icon-only-Ausgabe, manuellem Versand per Tastendruck und `config wo ist X`.
- `t1000e_companion_radio_ble-telemetry-bot-v2.uf2` als UF2-Datei dieser Folgeversion.

Wichtig: Im Web-Flasher die ZIP-Datei verwenden. Die UF2-Datei nur direkt auf das DFU-Laufwerk kopieren. Wer die bisherige Version behalten moechte, nutzt die Dateien ohne `-v2`; wer die neue Komfort-Version testen moechte, nutzt die Dateien mit `-v2`.

## Flashen

### Variante A: Web-Flasher

1. T1000-E in den DFU/Bootloader-Modus bringen.
2. MeshCore/Web-Flasher oeffnen.
3. Als Custom Firmware die passende ZIP auswaehlen, z. B. `firmware/t1000e_companion_radio_ble-telemetry-bot-v2.zip` fuer die Folgeversion.
4. Flashen und den Neustart abwarten.

### Variante B: UF2 per Drag-and-Drop

1. T1000-E in den DFU/Bootloader-Modus bringen.
2. Warten, bis das T1000-E-Laufwerk erscheint.
3. Die passende UF2-Datei auf dieses Laufwerk kopieren, z. B. `firmware/t1000e_companion_radio_ble-telemetry-bot-v2.uf2` fuer die Folgeversion.
4. Neustart abwarten.

## Standardverhalten

Im aktuellen Build sind diese Defaults gesetzt:

- Versand: private Direktnachricht an den Kontakt, der `config start` sendet
- Flood-Zielgruppe bei bewusst aktiviertem Flood-Modus: `Robbys_channel`
- Intervall: 10 Minuten
- Befehlswort: `config`
- Nachrichten-Label: `Telemetry`
- Felder: Akku, GPS, Temperatur, Licht

Der automatische Versand geht zuerst privat per Direct. Ein Gruppen-/Flood-Versand passiert nur nach `config flood`. Der Kanal `Public` wird fuer Tracking nicht verwendet.

## Befehle per Direktnachricht

Alle Befehle werden als Direktnachricht an den T1000-E gesendet. Jeder erkannte Befehl wird ebenfalls per Direktnachricht bestaetigt.

| Befehl | Wirkung |
| --- | --- |
| `config help` | Gibt eine kurze Befehlsuebersicht zurueck. |
| `config status` | Gibt aktuelle Einstellungen zurueck. |
| `config start` | Startet den periodischen Direct-Versand an den Absender. Erste Meldung nach ca. 3 Sekunden. |
| `config stop` | Stoppt den periodischen Versand. |
| `config direct` | Stellt den Versand auf private Direktnachricht. |
| `config target me` | Setzt den Absender als Direct-Ziel. |
| `config flood` | Stellt bewusst auf Flood-Versand in einen privaten Kanal. |
| `config group Robbys_channel` | Setzt die Flood-Zielgruppe. `Public` wird abgelehnt. |
| `config scope PARK` | Setzt den Flood-Scope fuer gezielteres Flooding. |
| `config scope off` | Entfernt den gesetzten Flood-Scope. |
| `config interval 10` | Setzt das Intervall in Minuten. 0 oder mindestens 10 Minuten. |
| `config label test` | Setzt das erste Wort der Telemetrie-Nachricht, z. B. `test:`. |
| `config all` | Aktiviert alle Felder. |
| `config gps akku temp licht` | Aktiviert genau diese Felder. |
| `config ble on` | Schaltet Bluetooth wieder ein, z. B. fuer die App-Verbindung. |
| `config ble off` | Schaltet Bluetooth aus. |
| `config ble auto on` | Bluetooth schaltet nach 10 Minuten ohne Verbindung automatisch ab. |
| `config ble auto off` | Deaktiviert das automatische Bluetooth-Abschalten. |
| `config sound off` | Deaktiviert normale Tonsignale. |
| `config sound on` | Aktiviert normale Tonsignale. |
| `config wo ist` | Spielt ein Suchsignal am Geraet ab. |
| `config wo ist 3` | Spielt das Suchsignal 3-mal ab. Erlaubt sind 1 bis 10 Wiederholungen. |
| `config prefix xy` | Aendert das Befehlswort von `config` auf `xy`. |

Ein kurzer Tastendruck am T1000-E sendet sofort eine Telemetrie-Nachricht mit der aktuellen Konfiguration. Im Direct-Modus geht sie an das konfigurierte Direct-Ziel, im Flood-Modus in den gesetzten privaten Kanal.

Nach `config prefix xy` muessen weitere Befehle mit `xy` beginnen:

```text
xy help
xy status
xy stop
xy label tracker
```

## Beispiele

Standardmeldung als private Direktnachricht:

```text
Telemetry:
🔋 3.95V
🌡️ 24.1C
🗺️🛰️ https://maps.google.com/?q=52.123456,13.123456
💡🔦 42%
```

Label und Felder aendern:

```text
config label test
config gps akku
```

Danach sendet der T1000-E z. B.:

```text
test:
🔋 3.95V
🗺️🛰️ https://maps.google.com/?q=52.123456,13.123456
```

Bewusst in einen privaten Kanal flooden:

```text
config group Robbys_channel
config scope PARK
config flood
config start
```

Zurueck auf privaten Direct-Versand:

```text
config direct
config target me
```

Geraet stumm schalten, aber trotzdem finden:

```text
config sound off
config wo ist 3
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

The firmware periodically sends selected telemetry fields by private direct message by default. Flood/group delivery is only used when explicitly enabled.

## Features

- Periodic telemetry messages by direct message.
- Optional flood delivery to a private MeshCore channel.
- Direct-message control with acknowledgements.
- Configurable message label, group name, flood scope, interval, and telemetry fields.
- Google Maps links for GPS coordinates.
- Optional zero-hop advert after each telemetry push.
- Buzzer mute/unmute by direct message.
- Find-device sound by direct message.
- BLE auto-off after 10 minutes without an app connection.
- Short button press sends one telemetry message with the current configuration.

## Firmware Files

Prebuilt firmware artifacts are in the `firmware/` folder:

- `t1000e_companion_radio_ble-telemetry-bot.zip` for the MeshCore/Web nRF flasher.
- `t1000e_companion_radio_ble-telemetry-bot.uf2` for drag-and-drop flashing in DFU mode.
- `t1000e_companion_radio_ble-telemetry-bot-v2.zip` as the follow-up version with icon-only output, manual button send, and repeated find sound.
- `t1000e_companion_radio_ble-telemetry-bot-v2.uf2` as the UF2 file for that follow-up version.

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

- Delivery mode: direct message to the contact that sends `config start`
- Flood target group when explicitly enabled: `Robbys_channel`
- Interval: 10 minutes
- Command prefix: `config`
- Message label: `Telemetry`
- Fields: battery, GPS, temperature, light

Group/flood delivery must be enabled with `config flood`. The `Public` channel is refused for tracking messages.

## Direct Message Commands

Send these as direct messages to the T1000-E node.

| Command | Effect |
| --- | --- |
| `config help` | Sends a short command list as a direct reply. |
| `config status` | Sends current settings as a direct reply. |
| `config start` | Enables periodic direct telemetry to the sender. First message is sent after about 3 seconds. |
| `config stop` | Disables periodic telemetry. |
| `config direct` | Uses private direct delivery. |
| `config target me` | Sets the sender as the direct target. |
| `config flood` | Explicitly enables flood delivery to a private channel. |
| `config group Robbys_channel` | Sets the flood target group by name. `Public` is refused. |
| `config scope PARK` | Sets the flood scope. |
| `config scope off` | Clears the flood scope. |
| `config interval 10` | Sets the interval in minutes. Use `0` or at least `10`. |
| `config label test` | Sets the first word of every outgoing telemetry message. |
| `config all` | Enables all telemetry fields. |
| `config gps akku temp licht` | Selects GPS, battery, temperature, and light fields. |
| `config ble on` | Enables Bluetooth for app access. |
| `config ble off` | Disables Bluetooth. |
| `config ble auto on` | Enables BLE auto-off after 10 idle minutes. |
| `config ble auto off` | Disables BLE auto-off. |
| `config sound off` | Mutes normal buzzer notifications. |
| `config sound on` | Enables normal buzzer notifications. |
| `config wo ist` | Plays a find-device sound even if normal sound is muted. |
| `config wo ist 3` | Plays the find-device sound 3 times. Valid range is 1 to 10. |
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
Telemetry:
🔋 3.95V
🌡️ 24.1C
🗺️🛰️ https://maps.google.com/?q=52.123456,13.123456
💡🔦 42%
```

After:

```text
config label test
config gps akku
```

The telemetry message becomes:

```text
test:
🔋 3.95V
🗺️🛰️ https://maps.google.com/?q=52.123456,13.123456
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
