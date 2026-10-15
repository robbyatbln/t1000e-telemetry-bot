#pragma once

#include "NodePrefs.h"

// Decode the pre-JSON layout used by telemetry v1-v8 without changing field widths.
template <typename Reader>
void loadLegacyTelemetryPrefs(Reader& file, NodePrefs& _prefs) {
  uint8_t pad[8];

  file.read((uint8_t *)&_prefs.airtime_factor, sizeof(float));                           // 0
  file.read((uint8_t *)_prefs.node_name, sizeof(_prefs.node_name));                      // 4
  file.read(pad, 4);                                                                     // 36
  file.read((uint8_t *)&_prefs.node_lat, sizeof(_prefs.node_lat));                       // 40
  file.read((uint8_t *)&_prefs.node_lon, sizeof(_prefs.node_lon));                       // 48
  file.read((uint8_t *)&_prefs.freq, sizeof(_prefs.freq));                               // 56
  file.read((uint8_t *)&_prefs.sf, sizeof(_prefs.sf));                                   // 60
  file.read((uint8_t *)&_prefs.cr, sizeof(_prefs.cr));                                   // 61
  file.read((uint8_t *)&_prefs._client_repeat, sizeof(_prefs._client_repeat));             // 62
  file.read((uint8_t *)&_prefs.manual_add_contacts, sizeof(_prefs.manual_add_contacts)); // 63
  file.read((uint8_t *)&_prefs.bw, sizeof(_prefs.bw));                                   // 64
  file.read((uint8_t *)&_prefs.tx_power_dbm, sizeof(_prefs.tx_power_dbm));               // 68
  file.read((uint8_t *)&_prefs.telemetry_mode_base, sizeof(_prefs.telemetry_mode_base)); // 69
  file.read((uint8_t *)&_prefs.telemetry_mode_loc, sizeof(_prefs.telemetry_mode_loc));   // 70
  file.read((uint8_t *)&_prefs.telemetry_mode_env, sizeof(_prefs.telemetry_mode_env));   // 71
  file.read((uint8_t *)&_prefs.rx_delay_base, sizeof(_prefs.rx_delay_base));             // 72
  file.read((uint8_t *)&_prefs.advert_loc_policy, sizeof(_prefs.advert_loc_policy));     // 76
  file.read((uint8_t *)&_prefs.multi_acks, sizeof(_prefs.multi_acks));                   // 77
  file.read((uint8_t *)&_prefs.path_hash_mode, sizeof(_prefs.path_hash_mode));           // 78
  file.read(pad, 1);                                                                     // 79
  file.read((uint8_t *)&_prefs.ble_pin, sizeof(_prefs.ble_pin));                         // 80
  file.read((uint8_t *)&_prefs.buzzer_quiet, sizeof(_prefs.buzzer_quiet));               // 84
  file.read((uint8_t *)&_prefs.gps_enabled, sizeof(_prefs.gps_enabled));                 // 85
  // Telemetry v1-v8 stored one byte here; the upstream JSON format uses uint32_t.
  uint8_t legacy_gps_interval = 0;
  file.read(&legacy_gps_interval, sizeof(legacy_gps_interval));                        // 86
  _prefs.gps_interval = legacy_gps_interval;
  file.read((uint8_t *)&_prefs.autoadd_config, sizeof(_prefs.autoadd_config));           // 87
  file.read((uint8_t *)&_prefs.autoadd_max_hops, sizeof(_prefs.autoadd_max_hops));       // 88
  file.read((uint8_t *)&_prefs.rx_boosted_gain, sizeof(_prefs.rx_boosted_gain));         // 89
  file.read((uint8_t *)_prefs.default_scope_name, sizeof(_prefs.default_scope_name));    // 90
  file.read((uint8_t *)_prefs.default_scope_key, sizeof(_prefs.default_scope_key));     // 121
  file.read((uint8_t *)&_prefs.telemetry_push_interval_mins, sizeof(_prefs.telemetry_push_interval_mins)); // 137
  file.read((uint8_t *)&_prefs.telemetry_push_group_idx, sizeof(_prefs.telemetry_push_group_idx));         // 139
  file.read((uint8_t *)&_prefs.telemetry_push_enabled, sizeof(_prefs.telemetry_push_enabled));             // 140
  file.read((uint8_t *)&_prefs.telemetry_push_fields, sizeof(_prefs.telemetry_push_fields));               // 141
  file.read((uint8_t *)_prefs.telemetry_push_group_name, sizeof(_prefs.telemetry_push_group_name));         // 142
  file.read((uint8_t *)_prefs.telemetry_push_label, sizeof(_prefs.telemetry_push_label));                   // 174
  file.read((uint8_t *)_prefs.telemetry_command_prefix, sizeof(_prefs.telemetry_command_prefix));           // 190
  file.read((uint8_t *)&_prefs.telemetry_push_mode, sizeof(_prefs.telemetry_push_mode));                    // 206
  file.read((uint8_t *)_prefs.telemetry_target_pub_key, sizeof(_prefs.telemetry_target_pub_key));            // 207
  file.read((uint8_t *)&_prefs.ble_auto_off, sizeof(_prefs.ble_auto_off));                                  // 239
  file.read((uint8_t *)&_prefs.alarm_enabled, sizeof(_prefs.alarm_enabled));                                // 240
  file.read((uint8_t *)&_prefs.alarm_hour, sizeof(_prefs.alarm_hour));                                      // 241
  file.read((uint8_t *)&_prefs.alarm_minute, sizeof(_prefs.alarm_minute));                                  // 242
  file.read((uint8_t *)&_prefs.gps_time_sync_interval_mins, sizeof(_prefs.gps_time_sync_interval_mins));    // 243

  // migrate old fields
  _prefs.setRepeatEn(_prefs._client_repeat != 0);

}
