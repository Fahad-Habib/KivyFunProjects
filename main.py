from screeninfo import get_monitors
from PIL import Image

window_width = get_monitors()[0].width
window_height = get_monitors()[0].height
image = "Assets/grid.png"
w, h = Image.open(image).size

from kivy.config import Config

Config.set('graphics', 'shaped', 1)
Config.set('graphics', 'width', w)
Config.set('graphics', 'height', h)

from kivy.app import App
from kivy.graphics import Rectangle
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class CustomButton(Button):
    def __init__(self, dimensions, **kwargs):
        super(CustomButton, self).__init__(**kwargs)

        self.x_, self.y_ = dimensions
        self.clicked = False
        self.normal_color = (1, 1, 1, 0.8)
        self.on_hover_color = (0, 1, 1, 1)

        self.text = ''
        self.size = (180, 180)
        self.size_hint = (None, None)
        self.background_color = (1, 1, 1, 0.8)
        self.background_normal = ''
        self.background_down = ''

        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos):
        if self.collide_point(*pos):
            self.background_color = self.on_hover_color
        else:
            self.background_color = self.normal_color


class MainWindow(Screen):
    PLAYER = 0
    ICONS = {0: 'Assets/x.png', 1: 'Assets/o.png'}
    CANVAS = [[0, 0, 0] for _ in range(3)]
    GAME = [[2, 2, 2] for _ in range(3)]

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.buttons = [[0, 0, 0] for _ in range(3)]
        y = 0
        for i in range(3):
            x = 0
            for j in range(3):
                self.buttons[i][j] = CustomButton(pos=(x, y), dimensions=(i, j))
                self.buttons[i][j].bind(on_release=self.clicked)
                self.add_widget(self.buttons[i][j])
                x += 178 + 88
            y += 178 + 88

    def clicked(self, instance):
        if not instance.clicked:
            instance.normal_color = (1, 1, 1, 1)
            instance.on_hover_color = (1, 1, 1, 1)
            instance.clicked = True
            with self.canvas.after:
                self.CANVAS[instance.x_][instance.y_] = Rectangle(source=self.ICONS[self.PLAYER], size=(130, 130), pos=(25+(266.5*instance.y_), 25+(266.5*instance.x_)))
            self.GAME[instance.x_][instance.y_] = self.PLAYER
            self.PLAYER = (self.PLAYER + 1) % 2
            self.check()

    def check(self):
        game = self.GAME[::-1]

        for i in range(3):
            if game[i][0] == game[i][1] == game[i][2] != 2:
                self.end_game('r', i)
                return

        for i in range(3):
            if game[0][i] == game[1][i] == game[2][i] != 2:
                self.end_game('c', i)
                return

        if game[0][0] == game[1][1] == game[2][2] != 2:
            self.end_game('d', 0)
            return

        if game[2][0] == game[1][1] == game[0][2] != 2:
            self.end_game('d', 1)

    def end_game(self, t, n):
        if t == 'r':
            for i in range(3):
                self.buttons[2 - n][i].normal_color = (0, 1, 0, 1)
                self.buttons[2 - n][i].on_hover_color = (0, 1, 0, 1)
                self.buttons[2 - n][i].on_mouseover(None, (10000, 10000))
        elif t == 'c':
            for i in range(3):
                self.buttons[i][n].normal_color = (0, 1, 0, 1)
                self.buttons[i][n].on_hover_color = (0, 1, 0, 1)
                self.buttons[i][n].on_mouseover(None, (10000, 10000))
        elif t == 'd' and n == 0:
            for i in range(3):
                self.buttons[2-i][i].normal_color = (0, 1, 0, 1)
                self.buttons[2-i][i].on_hover_color = (0, 1, 0, 1)
                self.buttons[2-i][i].on_mouseover(None, (10000, 10000))
        elif t == 'd' and n == 1:
            for i in range(3):
                self.buttons[i][i].normal_color = (0, 1, 0, 1)
                self.buttons[i][i].on_hover_color = (0, 1, 0, 1)
                self.buttons[i][i].on_mouseover(None, (10000, 10000))


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

        self.add_widget(MainWindow(name='main'))


class ShapedWindow(App):
    def build(self):
        Window.size = (w, h)
        Window.left = (window_width / 2) - w / 2
        Window.top = (window_height / 2) - h / 2
        Window.shape_image = image
        Window.shape_mode = 'default'

        manager = ScreenManagement()
        return manager


if __name__ == '__main__':
    ShapedWindow().run()
