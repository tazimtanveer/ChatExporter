[app]
title = ChatExtractor
package.name = chatextractor
package.domain = org.chat.extractor
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,beautifulsoup4,python-dateutil
orientation = portrait
osx.kivy_version = 2.1.0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.accept_android_license = True
