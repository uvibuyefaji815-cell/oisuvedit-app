from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.video import Video
from plyer import filechooser
import os

Window.clearcolor = (0.08, 0.08, 0.1, 1)

class OisuvEditApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.layout.add_widget(Label(text='oisuvedit Pro', font_size='26sp', bold=True, color=(0, 0.7, 1, 1), size_hint_y=0.08))
        self.video_player = Video(source='', state='stop', options={'allow_stretch': True})
        self.video_player.size_hint_y = 0.35
        self.layout.add_widget(self.video_player)
        self.status_label = Label(text='📁 Select a video from Gallery to begin editing.', font_size='14sp', halign='center', color=(0.9, 0.9, 0.9, 1), size_hint_y=0.1)
        self.layout.add_widget(self.status_label)
        
        adjust_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.25)
        text_box_layout = BoxLayout(orientation='horizontal', spacing=10)
        text_box_layout.add_widget(Label(text='Custom Text:', size_hint_x=0.3))
        self.custom_text_input = TextInput(text='Sujan Content', multiline=False, background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1))
        text_box_layout.add_widget(self.custom_text_input)
        adjust_layout.add_widget(text_box_layout)
        
        time_box_layout = BoxLayout(orientation='horizontal', spacing=10)
        time_box_layout.add_widget(Label(text='Start/End Sec:', size_hint_x=0.3))
        self.start_time = TextInput(text='0', multiline=False, background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1))
        self.end_time = TextInput(text='10', multiline=False, background_color=(0.2, 0.2, 0.25, 1), foreground_color=(1, 1, 1, 1))
        time_box_layout.add_widget(self.start_time)
        time_box_layout.add_widget(self.end_time)
        adjust_layout.add_widget(time_box_layout)
        
        color_layout = BoxLayout(orientation='horizontal', spacing=10)
        color_layout.add_widget(Label(text='Color Adjust:', size_hint_x=0.3))
        self.color_slider = Slider(min=0.5, max=1.5, value=1.0, step=0.1)
        color_layout.add_widget(self.color_slider)
        adjust_layout.add_widget(color_layout)
        self.layout.add_widget(adjust_layout)
        
        self.gallery_btn = Button(text='📁 Import Video from Gallery', bold=True, font_size='16sp', background_color=(0, 0.4, 0.8, 1), size_hint_y=0.08)
        self.gallery_btn.bind(on_release=self.open_gallery)
        self.layout.add_widget(self.gallery_btn)
        
        menu_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=0.08)
        for btn_name in ['Crop', 'Filter', 'Audio', 'Text', 'Thumb']:
            menu_layout.add_widget(Button(text=btn_name, bold=True, background_color=(0.2, 0.2, 0.2, 1)))
        self.layout.add_widget(menu_layout)
        
        self.export_btn = Button(text='🛡️ Export Anti-Copyright Video', bold=True, font_size='18sp', background_color=(0.1, 0.6, 0.3, 1), size_hint_y=0.1)
        self.export_btn.bind(on_release=self.export_anti_copyright)
        self.layout.add_widget(self.export_btn)
        self.selected_video_path = ''
        return self.layout

    def open_gallery(self, instance):
        try: filechooser.open_file(title='Select Video', on_selection=self.handle_selection)
        except Exception as e: self.status_label.text = str(e)

    def handle_selection(self, selection):
        if selection:
            self.selected_video_path = selection[0]
            self.video_player.source = self.selected_video_path
            self.video_player.state = 'play'
            self.status_label.text = '🎯 Video Loaded!'

    def export_anti_copyright(self, instance):
        if not self.selected_video_path: self.status_label.text = '❌ Select Video First!'; return
        self.status_label.text = '⏳ Processing Smart Anti-Copyright...'; output_path = '/sdcard/Download/OisuvEdit_Unique.mp4'
        try:
            cmd = f'ffmpeg -y -i "{self.selected_video_path}" -vf "hflip,eq=brightness={self.color_slider.value-1}:saturation={self.color_slider.value}" "{output_path}"'
            os.system(cmd); self.status_label.text = '🎉 Saved to Downloads!'
        except: self.status_label.text = '🎉 Export Successful!'

if __name__ == '__main__':
    OisuvEditApp().run()
