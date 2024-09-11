import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle

class TimerApp(App):
    def build(self):
        self.seconds = 0
        self.running = False
        self.clock_event = None  # Variable para almacenar el evento de Clock

        # Layout principal
        layout = FloatLayout()  # Cambiar a FloatLayout para permitir superposición libre

        # Imagen de fondo animada
        self.background_images = ['background.jpg', 'background2.jpg', 'background3.jpg']
        if self.background_images:
            self.background = Image(source=self.background_images[0],
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    size_hint=(1, 1))  # Ocupa todo el espacio disponible
            layout.add_widget(self.background)

        # Caja para superponer elementos encima del fondo
        self.foreground_layout = FloatLayout(size_hint=(1, 1))  # Ocupa todo el espacio disponible
        layout.add_widget(self.foreground_layout)

        # Logo del gimnasio
        self.logo = Image(source='logo.png', size_hint=(1, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.85})
        self.foreground_layout.add_widget(self.logo)

        # Crear un canvas para el fondo del cronómetro
        self.timer_bg = Label(size_hint=(None, None), size=(300, 120), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        with self.timer_bg.canvas.before:
            Color(0, 0, 0, 0.7)  # Fondo negro con algo de transparencia
            self.bg_rect = Rectangle(size=self.timer_bg.size, pos=self.timer_bg.pos)

        self.timer_bg.bind(size=self.update_bg_rect, pos=self.update_bg_rect)
        self.foreground_layout.add_widget(self.timer_bg)

        # Label para mostrar el tiempo con sombra
        self.timer_label = Label(text='00:00:00',
                                 font_size=58,
                                 color=(1, 1, 1, 1),
                                 size_hint=(None, None),
                                 size=(200, 100),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.foreground_layout.add_widget(self.timer_label)

        # Botón para iniciar/pausar con animación y estilo
        self.start_pause_button = Button(text='Start',
                                         background_color=(0.1, 0.7, 0.3, 1),  # Verde
                                         color=(1, 1, 1, 1),  # Texto blanco
                                         font_size=24,
                                         size_hint=(0.8, 0.1),
                                         pos_hint={'center_x': 0.5, 'center_y': 0.35},
                                         on_press=self.start_pause,
                                         border=(0, 0, 0, 0))  # Sin bordes
        self.foreground_layout.add_widget(self.start_pause_button)

        # Botón para reiniciar con estilo
        reset_button = Button(text='Reset',
                              background_color=(0.8, 0.1, 0.1, 1),  # Rojo
                              color=(1, 1, 1, 1),  # Texto blanco
                              font_size=24,
                              size_hint=(0.8, 0.1),
                              pos_hint={'center_x': 0.5, 'center_y': 0.2},
                              on_press=self.reset_timer,
                              border=(0, 0, 0, 0))  # Sin bordes
        self.foreground_layout.add_widget(reset_button)

        # Iniciar la animación de fondo
        if self.background_images:
            Clock.schedule_interval(self.change_background, 5)  # Cambia de fondo cada 5 segundos

        return layout

    def update_bg_rect(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size

    def update_time(self, dt):
        if self.running:
            self.seconds += 1  # Incrementa en 1 cada segundo
            minutes, seconds = divmod(self.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            self.timer_label.text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

    def start_pause(self, instance):
        if self.running:
            self.start_pause_button.text = 'Start'
            anim = Animation(background_color=(1, 0.2, 0.2, 1), duration=0.2)
            anim.start(self.start_pause_button)
            self.running = False
            if self.clock_event:
                Clock.unschedule(self.clock_event)  # Detenemos el intervalo de tiempo
                self.clock_event = None
            self.play_sound('pause_sound.mp3')  # Sonido de pausa
        else:
            self.start_pause_button.text = 'Pause'
            anim = Animation(background_color=(0.2, 1, 0.2, 1), duration=0.2)
            anim.start(self.start_pause_button)
            self.running = True
            # Iniciar el cronómetro solo si no está ya corriendo
            if not self.clock_event:
                self.clock_event = Clock.schedule_interval(self.update_time, 1)
            self.play_sound('start_sound.mp3')  # Sonido de inicio

    def reset_timer(self, instance):
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

    def change_background(self, dt):
        if self.background_images:
            current_index = self.background_images.index(self.background.source)
            next_index = (current_index + 1) % len(self.background_images)
            self.background.source = self.background_images[next_index]

if __name__ == '__main__':
    TimerApp().run()
