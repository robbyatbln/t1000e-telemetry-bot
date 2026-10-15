#pragma once

#include <cstring>

namespace telemetry {

inline char lowerAscii(char c) {
  return c >= 'A' && c <= 'Z' ? c + ('a' - 'A') : c;
}

inline bool consumeName(const char*& text, const char* name) {
  if (!*name) return false;
  const char* p = text;
  for (; *name; ++name, ++p) {
    if (!*p || lowerAscii(*p) != lowerAscii(*name)) return false;
  }
  if (*p && *p != ' ') return false;
  while (*p == ' ') ++p;
  text = p;
  return true;
}

inline const char* addressedCommand(const char* text, const char* prefix, const char* node) {
  while (*text == ' ') ++text;
  if (!consumeName(text, prefix)) return nullptr;
  if (!consumeName(text, node) && !consumeName(text, "all")) return nullptr;
  return *text ? text : nullptr;
}

inline const char* channelCommand(const char* text, const char* prefix, const char* node) {
  if (const char* body = addressedCommand(text, prefix, node)) return body;
  const char* separator = std::strstr(text, ": ");
  return separator ? addressedCommand(separator + 2, prefix, node) : nullptr;
}

}  // namespace telemetry
