# MeshCore Location Integration installieren

## Was diese Installation ersetzt

Die Integration ersetzt die zuvor verwendete MQTT-Automation. Sie legt einen
echten Home-Assistant-GPS-Tracker direkt aus MeshCore-Channel-Nachrichten an
und erzeugt Bedienbuttons fuer Firmware-Befehle.

## Installationsdatei

Die zu installierende Datei lautet:

```text
meshcore_location.zip
```

## Installation per Home-Assistant-SSH

1. `meshcore_location.zip` nach `/config/` auf Home Assistant uebertragen.
2. Das SSH-Terminal von Home Assistant oeffnen.
3. Ausfuehren:

   ```sh
   cd /config
   unzip -o meshcore_location.zip
   ```

4. Pruefen, dass diese Datei vorhanden ist:

   ```text
   /config/custom_components/meshcore_location/manifest.json
   ```

5. Home Assistant neu starten.

## Einrichtung ueber die GUI

1. **Einstellungen > Geraete & Dienste > Integration hinzufuegen**.
2. **MeshCore Location** auswaehlen.
3. Den gewuenschten Channel aus der Liste der MeshCore-Integration auswaehlen.
   Die passende Nachrichten-Entity und der Channel-Index werden automatisch
   ermittelt.
4. Den Teilnehmer auswaehlen, der getrackt und gesteuert werden soll.
5. Die Zielperson, zum Beispiel **Alex**, auswaehlen.
6. Die erkannte Koordinate im Pruefschritt kontrollieren und fertigstellen.

Falls noch kein Teilnehmer erkannt wird, vor Schritt 3 oder 4 eine neue
GPS-Nachricht dieses Teilnehmers in den Channel senden. Alternativ kann der
Teilnehmername von Hand eingetragen werden.

Die Version `0.3.1` liest die konfigurierten Channels aus der vorhandenen
MeshCore-Integration und durchsucht den Aktivitaets-/Logbuchverlauf der
automatisch zugeordneten Channel-Entity. Vorherige Versionen konnten
faelschlich ein Icon-Attribut wie `mdi` als Teilnehmer anzeigen und lasen die
sichtbaren Nachrichten nicht aus dem korrekten Verlauf.

## Letzter Schritt fuer die Person

Nach der Einrichtung wird ein neuer `device_tracker` angelegt. Home Assistant
erlaubt Custom Integrations nicht ueber eine oeffentliche Schnittstelle, diesen
Tracker automatisch an eine bestehende Person zu haengen.

Darum einmalig:

1. **Einstellungen > Personen > Alex** oeffnen.
2. Den neuen MeshCore-Tracker zuweisen.
3. In der Landkarte-Karte **Alex** (`person.alex`) oder direkt den Tracker
   anzeigen.

Ist in der Landkarte-Karte eine einzelne Entity hinzugefuegt, muss
**Alle anzeigen** ausgeschaltet sein.

## Bedienung

Nach der Einrichtung gehoeren zum Tracker Buttons fuer:

- Status, Start/Stop, Messwerte, Zeitsync und Bluetooth per privatem Channel
- Ton und Suchsignal per Direktnachricht an den Teilnehmer

Die Trennung ist durch die Tracker-Firmware bedingt: Firmware v8 versteht
`config GERAETENAME status`, `gps`, `ble on/off` usw. im konfigurierten privaten
Channel; `sound on/off`, `wo ist` und Weckerbefehle sind als Direct-Kommandos
implementiert.

Die Landkarte selbst erlaubt in ihrem Marker-Popup keine voll konfigurierbare
Steuerleiste. Fuege die erzeugten Button-Entities deshalb in einer
**Entitaeten**-Karte direkt unter oder neben der Landkarte hinzu.
