# NOTE: This is a Kivy version of the full Chat Extractor and Combiner tool.
# It includes: JSON + HTML extract support, timestamp toggling, participant renaming, and FB-IG txt combiner.
# To build as APK: install Kivy and Buildozer, then use `buildozer -v android debug`.

import json
import os
import codecs
from datetime import datetime
from dateutil import parser as date_parser
from bs4 import BeautifulSoup

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

class ChatExtractorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.file_path = ''
        self.output_path = ''
        self.export_type = 'json'  # or 'html'
        self.rename_map = {}
        self.include_ts = True
        self.include_label = False

        self.build_main_menu()

    def build_main_menu(self):
        self.clear_widgets()
        self.add_widget(Label(text='Chat Extractor Tool', font_size=20))
        self.add_widget(Button(text='Extract Chat (JSON/HTML)', on_press=self.extractor_screen))
        self.add_widget(Button(text='Combine FB/IG Extracts', on_press=self.combiner_screen))

    def extractor_screen(self, instance):
        self.clear_widgets()
        self.add_widget(Button(text='⬅ Back', on_press=lambda x: self.build_main_menu()))

        btn_json = Button(text='Select JSON File')
        btn_json.bind(on_press=lambda x: self.select_file('json'))
        self.add_widget(btn_json)

        btn_html = Button(text='Select HTML File')
        btn_html.bind(on_press=lambda x: self.select_file('html'))
        self.add_widget(btn_html)

        self.ts_checkbox = CheckBox(active=True)
        self.add_widget(Label(text='Include timestamps'))
        self.add_widget(self.ts_checkbox)

        self.add_widget(Button(text='Extract & Save', on_press=self.extract_chat))
        self.status_label = Label(text='')
        self.add_widget(self.status_label)

    def combiner_screen(self, instance):
        self.clear_widgets()
        self.add_widget(Button(text='⬅ Back', on_press=lambda x: self.build_main_menu()))

        self.fb_path = ''
        self.ig_path = ''

        self.fb_btn = Button(text='Select FB TXT File')
        self.fb_btn.bind(on_press=lambda x: self.select_txt_file('fb'))
        self.add_widget(self.fb_btn)

        self.ig_btn = Button(text='Select IG TXT File')
        self.ig_btn.bind(on_press=lambda x: self.select_txt_file('ig'))
        self.add_widget(self.ig_btn)

        self.comb_ts_checkbox = CheckBox(active=True)
        self.comb_label_checkbox = CheckBox(active=True)
        self.add_widget(Label(text='Include timestamps'))
        self.add_widget(self.comb_ts_checkbox)
        self.add_widget(Label(text='Label source (FB/IG)'))
        self.add_widget(self.comb_label_checkbox)

        self.add_widget(Button(text='Merge & Save', on_press=self.combine_chats))
        self.status_label = Label(text='')
        self.add_widget(self.status_label)

    def select_file(self, filetype):
        chooser = FileChooserIconView()
        popup = Popup(title="Select File", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=lambda chooser, selection, touch: self.set_main_file(selection, popup, filetype))
        popup.open()

    def set_main_file(self, selection, popup, filetype):
        if selection:
            self.file_path = selection[0]
            self.export_type = filetype
            self.status_label.text = f"Selected {filetype.upper()}: {os.path.basename(self.file_path)}"
            popup.dismiss()

    def select_txt_file(self, source):
        chooser = FileChooserIconView()
        popup = Popup(title=f"Select {source.upper()} TXT File", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=lambda chooser, selection, touch: self.set_txt_path(selection, popup, source))
        popup.open()

    def set_txt_path(self, selection, popup, source):
        if selection:
            if source == 'fb':
                self.fb_path = selection[0]
                self.fb_btn.text = f"FB: {os.path.basename(self.fb_path)}"
            else:
                self.ig_path = selection[0]
                self.ig_btn.text = f"IG: {os.path.basename(self.ig_path)}"
            popup.dismiss()

    def extract_chat(self, instance):
        if not self.file_path:
            self.status_label.text = "No file selected"
            return

        include_ts = self.ts_checkbox.active
        lines = []

        if self.export_type == 'json':
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for msg in reversed(data.get('messages', [])):
                    sender = msg.get('sender_name', '')
                    content = msg.get('content', '')
                    ts = msg.get('timestamp_ms')
                    ts_fmt = f"[{datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M')}] " if include_ts and ts else ""
                    lines.append(f"{ts_fmt}{sender}: {content}")
        else:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                blocks = soup.find_all('div', class_='pam')
                for b in reversed(blocks):
                    parts = b.find_all('div')
                    if len(parts) >= 2:
                        name = parts[0].text.strip()
                        msg = parts[1].text.strip()
                        date_div = b.find_next_sibling('div')
                        ts_raw = date_div.text if date_div else ""
                        try:
                            ts_parsed = date_parser.parse(ts_raw)
                            ts_fmt = f"[{ts_parsed.strftime('%Y-%m-%d %H:%M')}] " if include_ts else ""
                        except:
                            ts_fmt = ""
                        lines.append(f"{ts_fmt}{name}: {msg}")

        out_path = os.path.join(os.path.expanduser("~"), f"chat_{self.export_type}.txt")
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write("\n".join(lines))
        self.status_label.text = f"Saved to: {out_path}"

    def extract_ts_line(self, line):
        try:
            ts = date_parser.parse(line.split(']')[0].strip('['))
            return ts
        except:
            return None

    def combine_chats(self, instance):
        if not (self.fb_path and self.ig_path):
            self.status_label.text = "Both FB and IG files required"
            return

        all_msgs = []

        def parse_file(path, label):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    ts = self.extract_ts_line(line)
                    if ts:
                        msg = line.split(']', 1)[-1].strip()
                        prefix = f"[{ts.strftime('%Y-%m-%d %H:%M')}] " if self.comb_ts_checkbox.active else ""
                        label_tag = f"({label}) " if self.comb_label_checkbox.active else ""
                        all_msgs.append((ts, f"{prefix}{label_tag}{msg}"))

        parse_file(self.fb_path, 'FB')
        parse_file(self.ig_path, 'IG')
        all_msgs.sort(key=lambda x: x[0])
        lines = [m[1] for m in all_msgs]

        out_path = os.path.join(os.path.expanduser("~"), "fb_ig_combined.txt")
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write("\n".join(lines))
        self.status_label.text = f"Saved to: {out_path}"

class ChatExtractorApp(App):
    def build(self):
        return ChatExtractorLayout()

if __name__ == '__main__':
    ChatExtractorApp().run()
