from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.core.window import Window
import json
import os

Window.clearcolor = (0.4, 0.49, 0.92, 1)

class TimerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pomodoro_time = 25 * 60
        self.pomodoro_running = False
        self.pomodoro_event = None
        
        self.kronometre_time = 0
        self.kronometre_running = False
        self.kronometre_event = None
        
        self.sayac_time = 10 * 60
        self.sayac_running = False
        self.sayac_event = None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Başlık
        layout.add_widget(Label(text='⏱️ SAYAÇ', font_size='28sp', size_hint_y=0.1, bold=True))
        
        # Tip seçimi
        tip_layout = GridLayout(cols=3, size_hint_y=0.12, spacing=10)
        self.pomodoro_btn = Button(text='🍅 Pomodoro', background_color=(0.4, 0.49, 0.92, 1))
        self.kronometre_btn = Button(text='⏱️ Kronometre', background_color=(0.7, 0.7, 0.7, 1))
        self.sayac_btn = Button(text='⏳ Geri Sayım', background_color=(0.7, 0.7, 0.7, 1))
        
        self.pomodoro_btn.bind(on_press=self.show_pomodoro)
        self.kronometre_btn.bind(on_press=self.show_kronometre)
        self.sayac_btn.bind(on_press=self.show_sayac)
        
        tip_layout.add_widget(self.pomodoro_btn)
        tip_layout.add_widget(self.kronometre_btn)
        tip_layout.add_widget(self.sayac_btn)
        layout.add_widget(tip_layout)
        
        # Pomodoro bölümü
        self.pomodoro_layout = BoxLayout(orientation='vertical', spacing=15)
        
        mode_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=10)
        self.calisma_btn = Button(text='Çalışma', background_color=(0.4, 0.49, 0.92, 1))
        self.kisa_btn = Button(text='Kısa Mola', background_color=(0.7, 0.7, 0.7, 1))
        self.uzun_btn = Button(text='Uzun Mola', background_color=(0.7, 0.7, 0.7, 1))
        
        self.calisma_btn.bind(on_press=lambda x: self.set_pomodoro_mode('calisma'))
        self.kisa_btn.bind(on_press=lambda x: self.set_pomodoro_mode('kisa'))
        self.uzun_btn.bind(on_press=lambda x: self.set_pomodoro_mode('uzun'))
        
        mode_layout.add_widget(self.calisma_btn)
        mode_layout.add_widget(self.kisa_btn)
        mode_layout.add_widget(self.uzun_btn)
        self.pomodoro_layout.add_widget(mode_layout)
        
        self.pomodoro_label = Label(text='25:00', font_size='72sp', bold=True)
        self.pomodoro_layout.add_widget(self.pomodoro_label)
        
        pomodoro_btns = GridLayout(cols=3, size_hint_y=None, height=60, spacing=10)
        self.pomodoro_start_btn = Button(text='Başlat', background_color=(0.15, 0.68, 0.38, 1))
        self.pomodoro_pause_btn = Button(text='Duraklat', background_color=(0.95, 0.61, 0.07, 1), disabled=True)
        self.pomodoro_reset_btn = Button(text='Sıfırla', background_color=(0.91, 0.3, 0.24, 1))
        
        self.pomodoro_start_btn.bind(on_press=self.start_pomodoro)
        self.pomodoro_pause_btn.bind(on_press=self.pause_pomodoro)
        self.pomodoro_reset_btn.bind(on_press=self.reset_pomodoro)
        
        pomodoro_btns.add_widget(self.pomodoro_start_btn)
        pomodoro_btns.add_widget(self.pomodoro_pause_btn)
        pomodoro_btns.add_widget(self.pomodoro_reset_btn)
        self.pomodoro_layout.add_widget(pomodoro_btns)
        
        layout.add_widget(self.pomodoro_layout)
        
        # Kronometre bölümü
        self.kronometre_layout = BoxLayout(orientation='vertical', spacing=15)
        self.kronometre_label = Label(text='00:00:00', font_size='72sp', bold=True)
        self.kronometre_layout.add_widget(self.kronometre_label)
        
        kronometre_btns = GridLayout(cols=3, size_hint_y=None, height=60, spacing=10)
        self.kronometre_start_btn = Button(text='Başlat', background_color=(0.15, 0.68, 0.38, 1))
        self.kronometre_pause_btn = Button(text='Duraklat', background_color=(0.95, 0.61, 0.07, 1), disabled=True)
        self.kronometre_reset_btn = Button(text='Sıfırla', background_color=(0.91, 0.3, 0.24, 1))
        
        self.kronometre_start_btn.bind(on_press=self.start_kronometre)
        self.kronometre_pause_btn.bind(on_press=self.pause_kronometre)
        self.kronometre_reset_btn.bind(on_press=self.reset_kronometre)
        
        kronometre_btns.add_widget(self.kronometre_start_btn)
        kronometre_btns.add_widget(self.kronometre_pause_btn)
        kronometre_btns.add_widget(self.kronometre_reset_btn)
        self.kronometre_layout.add_widget(kronometre_btns)
        
        # Sayaç bölümü
        self.sayac_layout = BoxLayout(orientation='vertical', spacing=15)
        
        input_layout = GridLayout(cols=2, size_hint_y=None, height=60, spacing=10)
        self.dakika_input = TextInput(text='10', multiline=False, input_filter='int', font_size='20sp')
        self.saniye_input = TextInput(text='0', multiline=False, input_filter='int', font_size='20sp')
        input_layout.add_widget(Label(text='Dakika:'))
        input_layout.add_widget(self.dakika_input)
        input_layout.add_widget(Label(text='Saniye:'))
        input_layout.add_widget(self.saniye_input)
        self.sayac_layout.add_widget(input_layout)
        
        self.sayac_label = Label(text='10:00', font_size='72sp', bold=True)
        self.sayac_layout.add_widget(self.sayac_label)
        
        sayac_btns = GridLayout(cols=3, size_hint_y=None, height=60, spacing=10)
        self.sayac_start_btn = Button(text='Başlat', background_color=(0.15, 0.68, 0.38, 1))
        self.sayac_pause_btn = Button(text='Duraklat', background_color=(0.95, 0.61, 0.07, 1), disabled=True)
        self.sayac_reset_btn = Button(text='Sıfırla', background_color=(0.91, 0.3, 0.24, 1))
        
        self.sayac_start_btn.bind(on_press=self.start_sayac)
        self.sayac_pause_btn.bind(on_press=self.pause_sayac)
        self.sayac_reset_btn.bind(on_press=self.reset_sayac)
        
        sayac_btns.add_widget(self.sayac_start_btn)
        sayac_btns.add_widget(self.sayac_pause_btn)
        sayac_btns.add_widget(self.sayac_reset_btn)
        self.sayac_layout.add_widget(sayac_btns)
        
        self.kronometre_layout.opacity = 0
        self.kronometre_layout.disabled = True
        self.sayac_layout.opacity = 0
        self.sayac_layout.disabled = True
        
        self.add_widget(layout)
    
    def show_pomodoro(self, instance):
        self.pomodoro_btn.background_color = (0.4, 0.49, 0.92, 1)
        self.kronometre_btn.background_color = (0.7, 0.7, 0.7, 1)
        self.sayac_btn.background_color = (0.7, 0.7, 0.7, 1)
        
        self.pomodoro_layout.opacity = 1
        self.pomodoro_layout.disabled = False
        self.kronometre_layout.opacity = 0
        self.kronometre_layout.disabled = True
        self.sayac_layout.opacity = 0
        self.sayac_layout.disabled = True
    
    def show_kronometre(self, instance):
        self.kronometre_btn.background_color = (0.4, 0.49, 0.92, 1)
        self.pomodoro_btn.background_color = (0.7, 0.7, 0.7, 1)
        self.sayac_btn.background_color = (0.7, 0.7, 0.7, 1)
        
        self.kronometre_layout.opacity = 1
        self.kronometre_layout.disabled = False
        self.pomodoro_layout.opacity = 0
        self.pomodoro_layout.disabled = True
        self.sayac_layout.opacity = 0
        self.sayac_layout.disabled = True
    
    def show_sayac(self, instance):
        self.sayac_btn.background_color = (0.4, 0.49, 0.92, 1)
        self.pomodoro_btn.background_color = (0.7, 0.7, 0.7, 1)
        self.kronometre_btn.background_color = (0.7, 0.7, 0.7, 1)
        
        self.sayac_layout.opacity = 1
        self.sayac_layout.disabled = False
        self.pomodoro_layout.opacity = 0
        self.pomodoro_layout.disabled = True
        self.kronometre_layout.opacity = 0
        self.kronometre_layout.disabled = True
    
    def set_pomodoro_mode(self, mode):
        if not self.pomodoro_running:
            self.calisma_btn.background_color = (0.4, 0.49, 0.92, 1) if mode == 'calisma' else (0.7, 0.7, 0.7, 1)
            self.kisa_btn.background_color = (0.4, 0.49, 0.92, 1) if mode == 'kisa' else (0.7, 0.7, 0.7, 1)
            self.uzun_btn.background_color = (0.4, 0.49, 0.92, 1) if mode == 'uzun' else (0.7, 0.7, 0.7, 1)
            
            times = {'calisma': 25*60, 'kisa': 5*60, 'uzun': 15*60}
            self.pomodoro_time = times[mode]
            self.update_pomodoro_display()
    
    def update_pomodoro_display(self):
        mins = self.pomodoro_time // 60
        secs = self.pomodoro_time % 60
        self.pomodoro_label.text = f'{mins:02d}:{secs:02d}'
    
    def start_pomodoro(self, instance):
        self.pomodoro_running = True
        self.pomodoro_start_btn.disabled = True
        self.pomodoro_pause_btn.disabled = False
        self.pomodoro_event = Clock.schedule_interval(self.tick_pomodoro, 1)
    
    def pause_pomodoro(self, instance):
        self.pomodoro_running = False
        self.pomodoro_start_btn.disabled = False
        self.pomodoro_pause_btn.disabled = True
        if self.pomodoro_event:
            self.pomodoro_event.cancel()
    
    def reset_pomodoro(self, instance):
        self.pause_pomodoro(instance)
        self.pomodoro_time = 25 * 60
        self.update_pomodoro_display()
    
    def tick_pomodoro(self, dt):
        self.pomodoro_time -= 1
        self.update_pomodoro_display()
        if self.pomodoro_time <= 0:
            self.pause_pomodoro(None)
    
    def update_kronometre_display(self):
        hours = self.kronometre_time // 3600
        mins = (self.kronometre_time % 3600) // 60
        secs = self.kronometre_time % 60
        self.kronometre_label.text = f'{hours:02d}:{mins:02d}:{secs:02d}'
    
    def start_kronometre(self, instance):
        self.kronometre_running = True
        self.kronometre_start_btn.disabled = True
        self.kronometre_pause_btn.disabled = False
        self.kronometre_event = Clock.schedule_interval(self.tick_kronometre, 1)
    
    def pause_kronometre(self, instance):
        self.kronometre_running = False
        self.kronometre_start_btn.disabled = False
        self.kronometre_pause_btn.disabled = True
        if self.kronometre_event:
            self.kronometre_event.cancel()
    
    def reset_kronometre(self, instance):
        self.pause_kronometre(instance)
        self.kronometre_time = 0
        self.update_kronometre_display()
    
    def tick_kronometre(self, dt):
        self.kronometre_time += 1
        self.update_kronometre_display()
    
    def update_sayac_display(self):
        mins = self.sayac_time // 60
        secs = self.sayac_time % 60
        self.sayac_label.text = f'{mins:02d}:{secs:02d}'
    
    def start_sayac(self, instance):
        dakika = int(self.dakika_input.text or 0)
        saniye = int(self.saniye_input.text or 0)
        self.sayac_time = dakika * 60 + saniye
        self.update_sayac_display()
        
        self.sayac_running = True
        self.sayac_start_btn.disabled = True
        self.sayac_pause_btn.disabled = False
        self.sayac_event = Clock.schedule_interval(self.tick_sayac, 1)
    
    def pause_sayac(self, instance):
        self.sayac_running = False
        self.sayac_start_btn.disabled = False
        self.sayac_pause_btn.disabled = True
        if self.sayac_event:
            self.sayac_event.cancel()
    
    def reset_sayac(self, instance):
        self.pause_sayac(instance)
        self.sayac_time = 10 * 60
        self.update_sayac_display()
    
    def tick_sayac(self, dt):
        self.sayac_time -= 1
        self.update_sayac_display()
        if self.sayac_time <= 0:
            self.pause_sayac(None)


class NotlarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notlar = []
        self.load_data()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text='📝 NOTLAR', font_size='28sp', size_hint_y=0.08, bold=True))
        
        self.baslik_input = TextInput(hint_text='Not başlığı', multiline=False, size_hint_y=None, height=50, font_size='18sp')
        self.icerik_input = TextInput(hint_text='Not içeriği...', size_hint_y=0.25, font_size='16sp')
        
        layout.add_widget(self.baslik_input)
        layout.add_widget(self.icerik_input)
        
        ekle_btn = Button(text='Not Ekle', size_hint_y=None, height=50, background_color=(0.4, 0.49, 0.92, 1), font_size='18sp')
        ekle_btn.bind(on_press=self.not_ekle)
        layout.add_widget(ekle_btn)
        
        self.liste_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.55)
        layout.add_widget(self.liste_layout)
        
        self.add_widget(layout)
        self.notlari_goster()
    
    def load_data(self):
        if os.path.exists('notlar.json'):
            with open('notlar.json', 'r', encoding='utf-8') as f:
                self.notlar = json.load(f)
    
    def save_data(self):
        with open('notlar.json', 'w', encoding='utf-8') as f:
            json.dump(self.notlar, f, ensure_ascii=False, indent=2)
    
    def not_ekle(self, instance):
        baslik = self.baslik_input.text
        icerik = self.icerik_input.text
        
        if baslik and icerik:
            self.notlar.append({'baslik': baslik, 'icerik': icerik})
            self.save_data()
            self.baslik_input.text = ''
            self.icerik_input.text = ''
            self.notlari_goster()
    
    def notlari_goster(self):
        self.liste_layout.clear_widgets()
        for i, not_item in enumerate(self.notlar):
            not_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
            
            text_layout = BoxLayout(orientation='vertical', spacing=5)
            text_layout.add_widget(Label(text=not_item['baslik'], bold=True, size_hint_y=0.4, halign='left'))
            text_layout.add_widget(Label(text=not_item['icerik'][:50] + '...', size_hint_y=0.6, halign='left'))
            
            sil_btn = Button(text='Sil', size_hint_x=0.2, background_color=(0.91, 0.3, 0.24, 1))
            sil_btn.bind(on_press=lambda x, idx=i: self.not_sil(idx))
            
            not_layout.add_widget(text_layout)
            not_layout.add_widget(sil_btn)
            self.liste_layout.add_widget(not_layout)
    
    def not_sil(self, idx):
        del self.notlar[idx]
        self.save_data()
        self.notlari_goster()


class YapilacaklarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gorevler = []
        self.load_data()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text='✅ YAPILACAKLAR', font_size='28sp', size_hint_y=0.08, bold=True))
        
        ekle_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.gorev_input = TextInput(hint_text='Yeni görev...', multiline=False, font_size='18sp')
        ekle_btn = Button(text='Ekle', size_hint_x=0.25, background_color=(0.4, 0.49, 0.92, 1), font_size='18sp')
        ekle_btn.bind(on_press=self.gorev_ekle)
        
        ekle_layout.add_widget(self.gorev_input)
        ekle_layout.add_widget(ekle_btn)
        layout.add_widget(ekle_layout)
        
        self.liste_layout = BoxLayout(orientation='vertical', spacing=8)
        layout.add_widget(self.liste_layout)
        
        self.add_widget(layout)
        self.gorevleri_goster()
    
    def load_data(self):
        if os.path.exists('gorevler.json'):
            with open('gorevler.json', 'r', encoding='utf-8') as f:
                self.gorevler = json.load(f)
    
    def save_data(self):
        with open('gorevler.json', 'w', encoding='utf-8') as f:
            json.dump(self.gorevler, f, ensure_ascii=False, indent=2)
    
    def gorev_ekle(self, instance):
        baslik = self.gorev_input.text
        if baslik:
            self.gorevler.append({'baslik': baslik, 'tamamlandi': False})
            self.save_data()
            self.gorev_input.text = ''
            self.gorevleri_goster()
    
    def gorevleri_goster(self):
        self.liste_layout.clear_widgets()
        for i, gorev in enumerate(self.gorevler):
            gorev_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
            
            checkbox = CheckBox(active=gorev['tamamlandi'], size_hint_x=0.15)
            checkbox.bind(active=lambda x, val, idx=i: self.gorev_tamamla(idx, val))
            
            label = Label(text=gorev['baslik'], size_hint_x=0.65, halign='left')
            if gorev['tamamlandi']:
                label.color = (0.5, 0.5, 0.5, 1)
            
            sil_btn = Button(text='Sil', size_hint_x=0.2, background_color=(0.91, 0.3, 0.24, 1))
            sil_btn.bind(on_press=lambda x, idx=i: self.gorev_sil(idx))
            
            gorev_layout.add_widget(checkbox)
            gorev_layout.add_widget(label)
            gorev_layout.add_widget(sil_btn)
            self.liste_layout.add_widget(gorev_layout)
    
    def gorev_tamamla(self, idx, tamamlandi):
        self.gorevler[idx]['tamamlandi'] = tamamlandi
        self.save_data()
        self.gorevleri_goster()
    
    def gorev_sil(self, idx):
        del self.gorevler[idx]
        self.save_data()
        self.gorevleri_goster()


class VerimlilikApp(App):
    def build(self):
        sm = ScreenManager()
        
        timer_screen = TimerScreen(name='timer')
        notlar_screen = NotlarScreen(name='notlar')
        yapilacaklar_screen = YapilacaklarScreen(name='yapilacaklar')
        
        sm.add_widget(timer_screen)
        sm.add_widget(notlar_screen)
        sm.add_widget(yapilacaklar_screen)
        
        # Ana layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Üst menü
        menu = GridLayout(cols=3, size_hint_y=0.08, spacing=5, padding=5)
        
        timer_btn = Button(text='⏱️ Sayaç', background_color=(0.4, 0.49, 0.92, 1))
        notlar_btn = Button(text='📝 Notlar')
        yapilacaklar_btn = Button(text='✅ Yapılacaklar')
        
        timer_btn.bind(on_press=lambda x: self.change_screen(sm, 'timer', [timer_btn, notlar_btn, yapilacaklar_btn]))
        notlar_btn.bind(on_press=lambda x: self.change_screen(sm, 'notlar', [timer_btn, notlar_btn, yapilacaklar_btn]))
        yapilacaklar_btn.bind(on_press=lambda x: self.change_screen(sm, 'yapilacaklar', [timer_btn, notlar_btn, yapilacaklar_btn]))
        
        menu.add_widget(timer_btn)
        menu.add_widget(notlar_btn)
        menu.add_widget(yapilacaklar_btn)
        
        main_layout.add_widget(menu)
        main_layout.add_widget(sm)
        
        self.menu_buttons = [timer_btn, notlar_btn, yapilacaklar_btn]
        
        return main_layout
    
    def change_screen(self, sm, screen_name, buttons):
        sm.current = screen_name
        for btn in buttons:
            btn.background_color = (0.7, 0.7, 0.7, 1)
        
        idx = {'timer': 0, 'notlar': 1, 'yapilacaklar': 2}[screen_name]
        buttons[idx].background_color = (0.4, 0.49, 0.92, 1)


if __name__ == '__main__':
    VerimlilikApp().run()
