[app]
title = Chat Extractor Tool
package.name = chatextractor
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 1.0
requirements = python3,kivy,beautifulsoup4,dateutil
orientation = portrait
fullscreen = 0
icon.filename = chat_icon.png

# Entry point
source.main = main.py

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 23b
android.arch = armeabi-v7a
android.accept_sdk_license = True
android.accept_android_license = True
# Required to avoid AIDL issues
android.build_tools_version = 34.0.0
