from io import BytesIO
from pathlib import Path
from datetime import datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.utils import platform
from qr_logic import payload, generate

NAVY=(.09,.17,.30,1); WHITE=(1,1,1,1)
class QRApp(App):
    def build(self):
        self.title='Smart QR Generator'; self.result=None
        Window.clearcolor=(.94,.96,.98,1)
        if platform not in ('android','ios'): Window.size=(480,800)
        scroll=ScrollView(do_scroll_x=False)
        root=BoxLayout(orientation='vertical',padding=dp(20),spacing=dp(10),size_hint_y=None)
        root.bind(minimum_height=root.setter('height')); scroll.add_widget(root)
        def label(text,height=26,size=14):
            w=Label(text=text,color=NAVY,font_size=dp(size),size_hint_y=None,height=dp(height),halign='left',valign='middle'); w.bind(size=lambda obj,s:setattr(obj,'text_size',s)); root.add_widget(w); return w
        def field(hint,text='',password=False):
            w=TextInput(hint_text=hint,text=text,multiline=False,password=password,size_hint_y=None,height=dp(44),padding=[dp(10),dp(10)],foreground_color=NAVY); root.add_widget(w); return w
        def spinner(values):
            w=Spinner(text=values[0],values=values,size_hint_y=None,height=dp(44),background_normal='',background_color=NAVY); root.add_widget(w); return w
        def button(text,callback):
            w=Button(text=text,size_hint_y=None,height=dp(46),background_normal='',background_color=NAVY); w.bind(on_release=callback); root.add_widget(w)
        label('UTILITIES / PROJECT 08',24,12); label('Smart QR Generator',42,26)
        label('Content type'); self.kind=spinner(['Text','Website','Email','Phone','Wi-Fi'])
        self.value=field('Enter text or content'); self.password=field('Wi-Fi password',password=True); self.security=spinner(['WPA','WEP','nopass'])
        def toggle(*args):
            wifi=self.kind.text=='Wi-Fi'; self.value.hint_text={'Wi-Fi':'Network name (SSID)','Website':'https://example.com','Email':'name@example.com','Phone':'+911234567890'}.get(self.kind.text,'Enter text')
            for w in (self.password,self.security): w.height=dp(44) if wifi else 0; w.opacity=int(wifi); w.disabled=not wifi
        self.kind.bind(text=toggle); toggle()
        label('QR color (hex)'); self.color=field('#172B4D','#172B4D')
        label('Image size / pixels'); self.size_choice=spinner(['512','256','1024','2048'])
        label('Error correction'); self.level=spinner(['M','L','Q','H'])
        button('Generate QR Code',self.create)
        self.preview=Image(size_hint_y=None,height=dp(240)); root.add_widget(self.preview)
        button('Save PNG',self.save); self.status=label('Ready. Generated locally.',80,13)
        return scroll
    def create(self,*args):
        self.result=None; self.preview.texture=None
        try:
            data=payload(self.kind.text,self.value.text,self.password.text,self.security.text)
            self.result=generate(data,int(self.size_choice.text),self.color.text,self.level.text)
            buf=BytesIO(); self.result.save(buf,format='PNG'); buf.seek(0); self.preview.texture=CoreImage(buf,ext='png').texture
            self.status.text='QR generated. Test with your camera before sharing.'
        except Exception as exc: self.status.text=str(exc)
    def save(self,*args):
        if self.result is None: self.status.text='Generate a QR code first.'; return
        try:
            folder=Path(self.user_data_dir) / 'exports' if platform=='android' else Path.home()/'SmartQRExports'
            folder.mkdir(parents=True,exist_ok=True); path=folder / datetime.now().strftime('QR_%Y%m%d_%H%M%S_%f.png'); self.result.save(path); self.status.text=f'Saved: {path}'
        except OSError as exc: self.status.text=str(exc)
if __name__=='__main__': QRApp().run()
