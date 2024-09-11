import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

class TimerApp(App):
    def build(self):
        self.seconds = 0
        self.running = False
        self.clock_event = None  # Variable para almacenar el evento de Clock

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Caja para superponer elementos encima del fondo
        self.foreground_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(self.foreground_layout)

        # Logo del gimnasio
        self.logo = Image(source='logo.png', size_hint=(1, 0.3))  # Asegúrate de que 'logo.png' exista
        self.foreground_layout.add_widget(self.logo)

        # Label para mostrar el tiempo con sombra
        self.timer_label = Label(text='00:00:00', font_size=58, color=(1, 1, 1, 1))
        self.foreground_layout.add_widget(self.timer_label)

        # Botón para iniciar/pausar con animación y estilo
        self.start_pause_button = Button(text='Start',
                                         background_color=(0.1, 0.7, 0.3, 1),  # Verde
                                         color=(1, 1, 1, 1),  # Texto blanco
                                         font_size=24,
                                         size_hint=(1, 0.2),
                                         on_press=self.start_pause)
        self.foreground_layout.add_widget(self.start_pause_button)

        # Botón para reiniciar con estilo
        reset_button = Button(text='Reset',
                              background_color=(0.8, 0.1, 0.1, 1),  # Rojo
                              color=(1, 1, 1, 1),  # Texto blanco
                              font_size=24,
                              size_hint=(1, 0.2),
                              on_press=self.reset_timer)
        self.foreground_layout.add_widget(reset_button)

        return layout

    def update_time(self, dt):
        if self.running:
            self.seconds += 1  # Incrementa en 1 cada segundo
            minutes, seconds = divmod(self.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            self.timer_label.text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

    def start_pause(self, instance):
        if self.running:
            # Pausar el cronómetro
            self.start_pause_button.text = 'Start'
            anim = Animation(background_color=(1, 0.2, 0.2, 1), duration=0.2)
            anim.start(self.start_pause_button)
            self.running = False
            self.play_sound('pause_sound.mp3')  # Sonido de pausa
        else:
            # Reanudar el cronómetro
            self.start_pause_button.text = 'Pause'
            anim = Animation(background_color=(0.2, 1, 0.2, 1), duration=0.2)
            anim.start(self.start_pause_button)
            self.running = True
            if not self.clock_event:
                # Iniciar el evento de reloj solo si no está corriendo
                self.clock_event = Clock.schedule_interval(self.update_time, 1)
            self.play_sound('start_sound.mp3')  # Sonido de inicio

    def reset_timer(self, instance):
        # Reiniciar el cronómetro
        self.seconds = 0
        self.timer_label.text = '00:00:00'
        self.start_pause_button.text = 'Start'
        self.running = False
        if self.clock_event:
            Clock.unschedule(self.clock_event)  # Detenemos el intervalo cuando se reinicia
            self.clock_event = None
        self.play_sound('reset_sound.mp3')  # Sonido de reinicio
        anim = Animation(background_color=(0.1, 0.4, 1, 1), duration=0.2)
        anim.start(instance)

    def play_sound(self, sound_file):
        sound = SoundLoader.load(sound_file)
        if sound:
            sound.play()
        else:
            print(f"Error: No se pudo cargar el archivo de sonido {sound_file}")

if __name__ == '__main__':
    TimerApp().run()
