[app]
title = Chat Extractor Tool
package.name = chatextractor
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,beautifulsoup4,dateutil
orientation = portrait
fullscreen = 0

# Android-specific
android.api = 33
android.build_tools_version = 33.0.2
android.ndk = 23b
android.arch = armeabi-v7a

# Permissions (optional, add as needed)
# android.permissions = INTERNET

# Icon (optional)
# icon.filename = chat_icon.png

[buildozer]
log_level = 2
warn_on_root = 1
