# MeshCore Tracker Control fuer Home Assistant

Diese Custom Integration erstellt GPS-Tracker und Bedienbuttons aus
MeshCore-Channel-Nachrichten
wie:

```text
<Tracking_Private> Tracker_Node_A: status :: ... https://maps.google.com/?q=52.417405,13.363181
```

## Funktionen

- Einrichtung ueber **Einstellungen > Geraete & Dienste**
- Auswahl der in MeshCore konfigurierten Channels, nicht einer manuellen Entity
- Automatische Ermittlung der zugehoerigen Channel-Nachrichten-Entity
- Erkennung der Teilnehmer aus dem sichtbaren Home-Assistant-Aktivitaetsverlauf
- Auswahl einer bestehenden Home-Assistant-Person als Zielhinweis
- GPS-Tracker ohne MQTT-Automation oder manuell gepflegte YAML
- Attribute fuer zuletzt empfangene Nachricht, Spannung, Temperatur und Licht
- Geraete-Buttons fuer Channel-Kommandos wie Status, Telemetrie und Bluetooth
- Direct-Buttons fuer Ton, Suchsignal und erweiterte Tracker-Funktionen
- Freier Dienst `meshcore_location.send_command` fuer Kommandos mit Parametern

Die Integration verwendet zum Senden die bereits vorhandenen Dienste der
Meshcore-HA-Integration: `meshcore.send_channel_message` und
`meshcore.send_message`.

## Installation per SSH

1. Die Datei `meshcore_location.zip` nach `/config/` in Home Assistant
   uebertragen.
2. Im Home-Assistant-SSH-Terminal ausfuehren:

   ```sh
   cd /config
   unzip -o meshcore_location.zip
   ```

3. Home Assistant neu starten.

Nach dem Entpacken muss diese Datei existieren:

```text
/config/custom_components/meshcore_location/manifest.json
```

## Einrichtung in der GUI

1. **Einstellungen > Geraete & Dienste > Integration hinzufuegen** oeffnen.
2. Nach **MeshCore Location** suchen.
3. Den aus der MeshCore-Integration angebotenen Channel auswaehlen, zum
   Beispiel `Tracking_Private (3)`. Die Nachrichten-Entity und der Channel-Index
   werden automatisch zugeordnet.
4. Den erkannten Teilnehmer auswaehlen, zum Beispiel
   `Tracker_Node_A`. Wenn im Aktivitaetsverlauf keine passende
   Standortnachricht steht, kann der Teilnehmername von Hand eingetragen
   werden.
5. Die bestehende Person auswaehlen, zum Beispiel `Alex`, und den vorgeschlagenen
   Trackernamen bestaetigen.
6. Im Pruefschritt kontrollieren, ob bereits eine Koordinate erkannt wurde,
   und den Tracker erstellen.

## Person einmalig verknuepfen

Home Assistant verwaltet die Tracker-Zuordnung einer Person selbst. Nach der
Einrichtung:

1. **Einstellungen > Personen > Alex** oeffnen.
2. Den neu erzeugten Tracker, zum Beispiel **Tracker_Node_A MeshCore**,
   zur Person hinzufuegen.
3. In der Landkarte-Karte `person.alex` oder direkt den neuen
   `device_tracker` anzeigen.

Bei einer Landkarte-Karte mit einzeln ausgewaehlten Entitaeten muss
**Alle anzeigen** ausgeschaltet sein.

## Teilnehmer-Erkennung

Im Einrichtungsdialog werden die konfigurierten Channels direkt aus der
MeshCore-Integration ausgelesen. Anschliessend wird die passende
Channel-Nachrichten-Entity gesucht und ihr Home-Assistant-Aktivitaetsverlauf
aus den letzten 24 Stunden ausgewertet. Das ist derselbe Verlauf, der im
Popup der Entity sichtbar ist. Nur Nachrichten mit Google-Maps-Standort werden
als Teilnehmerquelle verwendet; technische Attribute wie `mdi:message` werden
ignoriert.

Wenn ein Standort im Verlauf gefunden wurde, uebernimmt der neu erzeugte
Tracker direkt die neueste passende Position. Falls Recorder fuer diese Entity
deaktiviert ist oder die letzte Meldung aelter als 24 Stunden ist, sende vor
der Einrichtung eine neue Standortnachricht oder trage den Namen manuell ein.

## Aktualisierung

Sobald MeshCore ein neues `meshcore_message`-Event dieses Teilnehmers im
gewaehlten Channel mit einem Google-Maps-Link meldet, wird der GPS-Tracker
automatisch aktualisiert.
Die Integration benoetigt dafuer kein MQTT.

## Steuerbuttons

Die Integration legt zusammen mit dem Tracker Schaltflaechen an. Die folgenden
Kommandos funktionieren per privatem Channel in Firmware v8:

| Button | Gesendete Channel-Nachricht |
| --- | --- |
| Status abfragen | `config GERAETENAME status` |
| Telemetrie starten / stoppen | `config GERAETENAME start` / `stop` |
| Alle Messwerte melden | `config GERAETENAME all` |
| Nur GPS melden | `config GERAETENAME gps` |
| GPS und Sensoren melden | `config GERAETENAME gps akku temp licht` |
| Zeitsync anfordern | `config GERAETENAME sync` |
| Bluetooth an / aus | `config GERAETENAME ble on` / `ble off` |
| Intervall 10 / 30 Minuten | `config GERAETENAME interval 10` / `30` |

Die Firmware nimmt diese Funktionen derzeit nur per Direktnachricht an:

| Button | Gesendete Direktnachricht |
| --- | --- |
| Ton an / aus | `config sound on` / `config sound off` |
| Suchton | `config wo ist 3` |
| Wecker aus | `config wecker aus` |
| GPS-Zeitsync einmal / aus | `config timesync einmal` / `config timesync aus` |

Fuer eigene Befehle, etwa ein anderes Intervall oder eine Weckerzeit, steht
unter **Entwicklerwerkzeuge > Aktionen** der Dienst
`meshcore_location.send_command` bereit. Der Befehl wird ohne `config`
eingegeben, zum Beispiel `interval 60` per Channel oder `wecker 07:30` als
Direktnachricht.

### Vollstaendige Firmware-Befehle

Nach dem Stand der Tracker-Firmware v8 sind im privaten Channel diese
adressierten Befehle verfuegbar:

```text
config GERAETENAME status
config GERAETENAME start
config GERAETENAME stop
config GERAETENAME sync
config GERAETENAME ble on
config GERAETENAME ble off
config GERAETENAME interval 10
config GERAETENAME all
config GERAETENAME gps
config GERAETENAME gps akku temp licht
```

Als Direktnachricht an den Teilnehmer sind zusaetzlich verfuegbar:

```text
config help
config status
config start
config stop
config direct
config target me
config flood
config group Tracking_Private
config scope PARK
config scope off
config interval 10
config label test
config all
config gps akku temp licht
config ble on
config ble off
config ble auto on
config ble auto off
config sound on
config sound off
config wo ist
config wo ist 3
config wecker 15:44
config wecker aus
config sync
config timesync einmal
config timesync 30
config timesync aus
config prefix xy
```

Die Befehle mit freien Werten werden absichtlich nicht alle als feste Buttons
erzeugt, damit beispielsweise keine versehentliche Weckerzeit oder
Prefix-Aenderung ausgeloest wird. Sie koennen ueber
`meshcore_location.send_command` verwendet werden.

## Dashboard mit Karte und Bedienung

Die Standard-Landkarte von Home Assistant zeigt den Standort, kann aber in
ihrem Marker-Popup keine frei zusammengestellte Buttonleiste aufnehmen.
Praktisch ist daher eine Karte mit einer Bedienkarte direkt darunter:

```yaml
type: vertical-stack
cards:
  - type: map
    entities:
      - entity: device_tracker.tracker_node_a_meshcore
    hours_to_show: 24
  - type: entities
    title: Tracker Node A Steuerung
    entities:
      - entity: button.tracker_node_a_meshcore_status_abfragen
      - entity: button.tracker_node_a_meshcore_telemetrie_starten
      - entity: button.tracker_node_a_meshcore_telemetrie_stoppen
      - entity: button.tracker_node_a_meshcore_gps_und_sensoren_melden
      - entity: button.tracker_node_a_meshcore_ton_einschalten
      - entity: button.tracker_node_a_meshcore_ton_ausschalten
      - entity: button.tracker_node_a_meshcore_suchton_abspielen
```

Die tatsaechlichen Entity-IDs werden von Home Assistant nach der Einrichtung
angezeigt und koennen geringfuegig von diesem Beispiel abweichen.
