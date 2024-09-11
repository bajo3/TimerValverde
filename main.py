import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.image import Image

class TimerApp(App):
    def build(self):
        self.seconds = 0
        self.running = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Logo del gimnasio
        self.logo = Image(source='logo.png', size_hint=(1, 0.9))
        layout.add_widget(self.logo)

        # Label para mostrar el tiempo
        self.timer_label = Label(text='00:00:00', font_size=58)
        layout.add_widget(self.timer_label)

        # Botón para iniciar/pausar
        self.start_pause_button = Button(text='Start', on_press=self.start_pause)
        layout.add_widget(self.start_pause_button)

        # Botón para reiniciar
        reset_button = Button(text='Reset', on_press=self.reset_timer)
        layout.add_widget(reset_button)

        return layout

    def update_time(self, dt):
        if self.running:
            self.seconds += dt
            minutes, seconds = divmod(self.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            self.timer_label.text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

    def start_pause(self, instance):
        if self.running:
            self.start_pause_button.text = 'Start'
            self.running = False
        else:
            self.start_pause_button.text = 'Pause'
            self.running = True
            Clock.schedule_interval(self.update_time, 1)

    def reset_timer(self, instance):
        self.seconds = 0
        self.timer_label.text = '00:00:00'
        self.start_pause_button.text = 'Start'
        self.running = False

if __name__ == '__main__':
    TimerApp().run()
