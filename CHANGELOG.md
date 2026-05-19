# Changelog

## v4-status-time-boot-send

- `config status` und andere bestaetigte Konfigurationsbefehle zeigen jetzt die aktuelle Tracker-Uhrzeit als `Zeit HH:MM:SS`.
- Wenn Telemetrie aktiviert ist, startet der Tracker nach dem Einschalten automatisch nach wenigen Sekunden mit der ersten Uebertragung.
- Firmware-Dateien:
  - `firmware/t1000e_companion_radio_ble-telemetry-bot-v4.zip`
  - `firmware/t1000e_companion_radio_ble-telemetry-bot-v4.uf2`

## v3-alarm-time-sync

- Fuegt einen lokalen Wecker hinzu: `wecker 15:44` oder `config wecker 15:44`.
- `config wecker aus` deaktiviert den Wecker.
- Der Wecker nutzt die standortbezogen synchronisierte Tracker-Uhr. In Europa werden CET/CEST-Regeln verwendet, sonst ein grober Laengengrad-Versatz.
- Die interne Tracker-Uhr wird bei GPS-Zeitsync standortbezogen auf lokale Zeit gesetzt, damit Wecker und sichtbare Zeit ohne Verschiebung laufen.
- GPS-Zeitabgleich per Direktnachricht:
  - `config timesync einmal`
  - `config timesync 30`
  - `config timesync aus`
- Erfolgreicher manueller Versand per Taste bekommt einen kurzen eigenen Quittungston.
- Alarm, Suchton und Versandquittung verwenden unterschiedliche Tonfolgen.
- Wenn der Wecker klingelt, stoppt ein kurzer Tastendruck den Alarm lokal.
- Firmware-Dateien:
  - `firmware/t1000e_companion_radio_ble-telemetry-bot-v3.zip`
  - `firmware/t1000e_companion_radio_ble-telemetry-bot-v3.uf2`

## v2-manual-telemetry

- Telemetrie-Ausgabe nur mit Icon und Wert, wenn ein Icon vorhanden ist.
- Ein kurzer Tastendruck sendet sofort eine Telemetrie-Nachricht mit der aktuellen Konfiguration.
- `config wo ist 3` spielt den Suchton mehrfach ab.
- Firmware-Dateien:
  - `firmware/t1000e_companion_radio_ble-telemetry-bot-v2.zip`
  - `firmware/t1000e_companion_radio_ble-telemetry-bot-v2.uf2`

## v1-private-telemetry

- Private Direct-Nachricht als Standard fuer Tracking.
- Flood/Gruppe nur bewusst per `config flood`.
- `Public` wird fuer Tracking abgelehnt.
- Scope-Konfiguration per Direktnachricht.
- Mindestintervall 10 Minuten.
- Bluetooth-Auto-Off nach 10 Minuten ohne App-Verbindung.
- Firmware-Dateien:
  - `firmware/t1000e_companion_radio_ble-telemetry-bot.zip`
  - `firmware/t1000e_companion_radio_ble-telemetry-bot.uf2`
