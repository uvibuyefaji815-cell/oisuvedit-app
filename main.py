import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from plyer import filechooser
import threading
import subprocess

Window.clearcolor = (0.1, 0.1, 0.1, 1)

KV = '''
<VideoEditorUI>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    BoxLayout:
        size_hint_y: 0.4
        canvas.before:
            Color:
                rgb: 0.05, 0.05, 0.05
            Rectangle:
                pos: self.pos
                size: self.size
        VideoPlayer:
            id: video_player
            source: ''
            state: 'stop'
            options: {'allow_stretch': True}
            volume: 0

    ScrollView:
        size_hint_y: 0.6
        do_scroll_x: False
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(15)
            padding: dp(10)

            Button:
                text: '📁 Import Video from Gallery'
                size_hint_y: None
                height: dp(50)
                background_color: 0.2, 0.5, 0.8, 1
                color: 1, 1, 1, 1
                on_press: root.open_filechooser()

            GridLayout:
                cols: 2
                spacing: dp(10)
                size_hint_y: None
                height: dp(220)

                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        text: 'Start Second'
                        color: 0.8, 0.8, 0.8, 1
                    TextInput:
                        id: start_sec
                        text: '0'
                        multiline: False

                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        text: 'End Second'
                        color: 0.8, 0.8, 0.8, 1
                    TextInput:
                        id: end_sec
                        text: '10'
                        multiline: False

                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        text: 'Brightness'
                        color: 0.8, 0.8, 0.8, 1
                    Slider:
                        id: brightness_slider
                        min: 0.5
                        max: 1.5
                        value: 1.0
                        step: 0.1
                    Label:
                        text: str(round(brightness_slider.value, 1))

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(80)
                Label:
                    text: 'Custom Watermark Text'
                    color: 0.8, 0.8, 0.8, 1
                TextInput:
                    id: watermark_text
                    text: 'Sujan Content'
                    multiline: False

            Button:
                text: '✨ Anti-Copyright Magic Export ✨'
                size_hint_y: None
                height: dp(60)
                background_color: 0.1, 0.8, 0.3, 1
                color: 1, 1, 1, 1
                bold: True
                on_press: root.start_export()
'''

class VideoEditorUI(BoxLayout):
    current_video_path = ''

    def open_filechooser(self):
        try:
            filechooser.open_file(on_selection=self.on_video_selected)
        except Exception as e:
            self.show_popup("Error", "Could not open gallery.")

    def on_video_selected(self, selection):
        if selection:
            self.current_video_path = selection[0]
            self.ids.video_player.source = self.current_video_path
            self.ids.video_player.state = 'play'

    def start_export(self):
        if not self.current_video_path:
            self.show_popup("No Video", "Please import a video first.")
            return

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.progress_label = Label(text="Magic Processing Active...\nPlease Wait.", color=(1,1,1,1))
        content.add_widget(self.progress_label)
        self.progress_popup = Popup(title="Exporting", content=content, size_hint=(0.8, 0.4))
        self.progress_popup.open()

        thread = threading.Thread(target=self.process_video)
        thread.daemon = True
        thread.start()

    def process_video(self):
        input_path = self.current_video_path
        output_dir = "/sdcard/Download" if os.path.exists("/sdcard/Download") else "."
        output_path = os.path.join(output_dir, "oisuvedit_output.mp4")

        start = self.ids.start_sec.text
        end = self.ids.end_sec.text
        watermark = self.ids.watermark_text.text
        color_val = float(self.ids.brightness_slider.value)

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-ss", start, "-to", end, "-i", input_path,
            "-vf", f"hflip,eq=brightness={color_val-1}:saturation={color_val},drawtext=text='{watermark}':x=10:y=10:fontcolor=white:fontsize=24",
            "-vcodec", "libx264", "-crf", "23", "-acodec", "aac", output_path
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True)
            Clock.schedule_once(lambda dt: self.export_complete(output_path), 0.5)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup("Export Failed", "Error processing video."), 0)
        finally:
            self.progress_popup.dismiss()

    def export_complete(self, output_path):
        self.show_popup("Success", f"Video Saved To:\nDownloads/oisuvedit_output.mp4")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text="Close", size_hint_y=0.4)
        content.add_widget(close_btn)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

class OisuveditProApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    OisuveditProApp().run()
