#include <gtest/gtest.h>

#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

#include "../../examples/companion_radio/NodePrefs.h"
#include "../../examples/companion_radio/TelemetryCommandHelpers.h"
#include "../../examples/companion_radio/LegacyTelemetryPrefs.h"

// Radio CLI access is outside these persistence tests.
bool CommonRadioPrefs::getByKey(const char*, char*, size_t) { return false; }
bool CommonRadioPrefs::setByKey(const char*, const char*) { return false; }

class ReplayStream : public Stream {
  const char* _text;
  int _pos = 0;
  int _len;

public:
  explicit ReplayStream(const char* text) : _text(text), _len(strlen(text)) { }

  int available() override { return _len - _pos; }
  int read() override { return _pos < _len ? _text[_pos++] : -1; }
  int peek() override { return _pos < _len ? _text[_pos] : -1; }
};

class CaptureStream : public Stream {
  std::string _text;

  size_t emit(long long value) {
    char text[24];
    int length = snprintf(text, sizeof(text), "%lld", value);
    return write(reinterpret_cast<const uint8_t*>(text), length);
  }

public:
  size_t write(uint8_t value) override {
    _text.push_back(static_cast<char>(value));
    return 1;
  }

  size_t write(const uint8_t* buffer, size_t size) override {
    _text.append(reinterpret_cast<const char*>(buffer), size);
    return size;
  }

  size_t print(unsigned char value, int = DEC) override { return emit(value); }
  size_t print(int value, int = DEC) override { return emit(value); }
  size_t print(unsigned int value, int = DEC) override { return emit(value); }
  size_t print(long value, int = DEC) override { return emit(value); }
  size_t print(unsigned long value, int = DEC) override { return emit(value); }
  size_t print(long long value, int = DEC) override { return emit(value); }
  size_t print(unsigned long long value, int = DEC) override { return emit(value); }

  const std::string& text() const { return _text; }
};

#if 0
// Re-enable test once we can SET fem_ values in companion
TEST(CompanionNodePrefs, RxGainSettingsRoundTripIndependently) {
  NodePrefs saved;
  saved.rx_boosted_gain = 0;
  saved.radio_fem_rxgain = 1;
  saved.radio_fem_txgain = 0;

  CaptureStream output;
  ASSERT_TRUE(saved.saveSerial(output));
  EXPECT_NE(std::string::npos, output.text().find("rxgain:0"));
  EXPECT_NE(std::string::npos, output.text().find("fem_rxgain:1"));
  EXPECT_NE(std::string::npos, output.text().find("fem_txgain:0"));

  ReplayStream input("{radio:{rxgain:1,fem_rxgain:0,fem_txgain:1}}");
  NodePrefs loaded;
  loaded.rx_boosted_gain = 0;
  loaded.radio_fem_rxgain = 1;
  loaded.radio_fem_txgain = 0;

  ASSERT_TRUE(loaded.loadSerial(input));
  EXPECT_EQ(1, loaded.rx_boosted_gain);
  EXPECT_EQ(0, loaded.radio_fem_rxgain);
  EXPECT_EQ(1, loaded.radio_fem_txgain);
}
#endif

TEST(CompanionNodePrefs, TelemetrySettingsSurviveSaveAndReload) {
  NodePrefs saved;
  saved.telemetry_push_interval_mins = 45;
  saved.telemetry_push_fields = 0x0A;
  saved.telemetry_push_mode = TELEMETRY_PUSH_MODE_FLOOD;
  strcpy(saved.telemetry_push_group_name, "Robbys_channel");
  strcpy(saved.telemetry_push_label, "Park");
  strcpy(saved.telemetry_command_prefix, "tracker");
  saved.telemetry_target_pub_key[0] = 0xAB;
  saved.telemetry_target_pub_key[31] = 0xCD;
  saved.ble_auto_off = 0;
  saved.alarm_enabled = 1;
  saved.alarm_hour = 15;
  saved.alarm_minute = 44;
  saved.gps_time_sync_interval_mins = 30;
  saved.node_name[0] = 0;

  CaptureStream output;
  ASSERT_TRUE(saved.saveSerial(output));
  ReplayStream input(output.text().c_str());
  NodePrefs loaded;
  ASSERT_TRUE(loaded.loadSerial(input));
  EXPECT_EQ(45, loaded.telemetry_push_interval_mins);
  EXPECT_EQ(0x0A, loaded.telemetry_push_fields);
  EXPECT_EQ(TELEMETRY_PUSH_MODE_FLOOD, loaded.telemetry_push_mode);
  EXPECT_STREQ("Robbys_channel", loaded.telemetry_push_group_name);
  EXPECT_STREQ("Park", loaded.telemetry_push_label);
  EXPECT_STREQ("tracker", loaded.telemetry_command_prefix);
  EXPECT_EQ(0xAB, loaded.telemetry_target_pub_key[0]);
  EXPECT_EQ(0xCD, loaded.telemetry_target_pub_key[31]);
  EXPECT_EQ(0, loaded.ble_auto_off);
  EXPECT_EQ(1, loaded.alarm_enabled);
  EXPECT_EQ(15, loaded.alarm_hour);
  EXPECT_EQ(44, loaded.alarm_minute);
  EXPECT_EQ(30, loaded.gps_time_sync_interval_mins);
}

class LegacyFile {
  const std::vector<uint8_t>& _bytes;
  size_t _pos = 0;
public:
  explicit LegacyFile(const std::vector<uint8_t>& bytes) : _bytes(bytes) { }
  size_t read(uint8_t* dest, size_t size) {
    size_t count = std::min(size, _bytes.size() - _pos);
    memcpy(dest, _bytes.data() + _pos, count);
    _pos += count;
    return count;
  }
};

TEST(CompanionNodePrefs, VersionEightBinaryLayoutMigratesAndPersists) {
  std::vector<uint8_t> bytes(245, 0);
  bytes[62] = 1;  // client repeat
  bytes[86] = 60; // one-byte GPS interval in old firmware
  bytes[87] = 5;  // next field must not be swallowed by uint32_t read
  memcpy(&bytes[90], "PARK", 5);
  bytes[137] = 45;
  bytes[140] = 1;
  bytes[141] = 0x0A;
  memcpy(&bytes[142], "Robbys_channel", 15);
  memcpy(&bytes[174], "Park", 5);
  memcpy(&bytes[190], "tracker", 8);
  bytes[206] = 1;
  bytes[207] = 0xAB;
  bytes[238] = 0xCD;
  bytes[240] = 1;
  bytes[241] = 15;
  bytes[242] = 44;
  bytes[243] = 30;
  LegacyFile file(bytes);
  NodePrefs loaded;
  loadLegacyTelemetryPrefs(file, loaded);
  EXPECT_EQ(60U, loaded.gps_interval);
  EXPECT_EQ(5, loaded.autoadd_config);
  EXPECT_TRUE(loaded.isRepeatEn());
  EXPECT_STREQ("PARK", loaded.default_scope_name);
  EXPECT_EQ(45, loaded.telemetry_push_interval_mins);
  EXPECT_STREQ("Robbys_channel", loaded.telemetry_push_group_name);
  EXPECT_STREQ("tracker", loaded.telemetry_command_prefix);
  EXPECT_EQ(0xCD, loaded.telemetry_target_pub_key[31]);
  EXPECT_EQ(15, loaded.alarm_hour);
  EXPECT_EQ(44, loaded.alarm_minute);
  EXPECT_EQ(30, loaded.gps_time_sync_interval_mins);

  CaptureStream output;
  ASSERT_TRUE(loaded.saveSerial(output));
  ReplayStream input(output.text().c_str());
  NodePrefs reloaded;
  ASSERT_TRUE(reloaded.loadSerial(input));
  EXPECT_EQ(45, reloaded.telemetry_push_interval_mins);
  EXPECT_STREQ("tracker", reloaded.telemetry_command_prefix);
  EXPECT_EQ(0xCD, reloaded.telemetry_target_pub_key[31]);
}

TEST(CompanionNodePrefs, OldStockBinaryKeepsTelemetryDefaults) {
  std::vector<uint8_t> bytes(137, 0);
  bytes[86] = 60;
  LegacyFile file(bytes);
  NodePrefs loaded;
  loadLegacyTelemetryPrefs(file, loaded);
  EXPECT_EQ(60U, loaded.gps_interval);
  EXPECT_STREQ("config", loaded.telemetry_command_prefix);
  EXPECT_EQ(TELEMETRY_PUSH_MODE_DIRECT, loaded.telemetry_push_mode);
  EXPECT_EQ(1, loaded.ble_auto_off);
}

TEST(CompanionNodePrefs, StockSettingsKeepTelemetryDefaults) {
  ReplayStream input("{name:\"Stock\",comp:{buzz_q:1},gps:{int:3600}}");
  NodePrefs loaded;
  ASSERT_TRUE(loaded.loadSerial(input));
  EXPECT_STREQ("Stock", loaded.node_name);
  EXPECT_EQ(3600U, loaded.gps_interval);
  EXPECT_STREQ("config", loaded.telemetry_command_prefix);
  EXPECT_EQ(TELEMETRY_PUSH_MODE_DIRECT, loaded.telemetry_push_mode);
  EXPECT_EQ(1, loaded.ble_auto_off);
  EXPECT_EQ(0, loaded.alarm_enabled);
}

TEST(TelemetryChannelCommand, SenderPrefixAndCasePreserveCommandValue) {
  auto command = telemetry::channelCommand(
    "Robby: CONFIG Rob@bln_Sense_MAX label MyTracker", "config", "Rob@bln_Sense_MAX");
  ASSERT_NE(nullptr, command);
  EXPECT_STREQ("label MyTracker", command);
}

TEST(TelemetryChannelCommand, DeviceNamesWithSpacesAndCustomPrefix) {
  auto command = telemetry::channelCommand(
    "Robby: tracker Park Tracker ble on", "tracker", "Park Tracker");
  ASSERT_NE(nullptr, command);
  EXPECT_STREQ("ble on", command);
}

TEST(TelemetryChannelCommand, OnlyWholeDeviceNamesMatch) {
  EXPECT_EQ(nullptr, telemetry::channelCommand("Robby: config Tracker2 status", "config", "Tracker"));
  EXPECT_EQ(nullptr, telemetry::channelCommand("Robby: config Tracker", "config", "Tracker"));
  EXPECT_EQ(nullptr, telemetry::channelCommand("Robby: hello Tracker status", "config", "Tracker"));
  EXPECT_EQ(nullptr, telemetry::channelCommand("Robby: config Other status", "config", "Tracker"));
}

TEST(TelemetryChannelCommand, RawAndBroadcastCommands) {
  EXPECT_STREQ("status", telemetry::channelCommand(" config Tracker status", "config", "Tracker"));
  EXPECT_STREQ("stop", telemetry::channelCommand("Robby: config all stop", "config", "Tracker"));
  EXPECT_STREQ("wecker 15:44", telemetry::channelCommand("Robby: config Tracker wecker 15:44", "config", "Tracker"));
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
