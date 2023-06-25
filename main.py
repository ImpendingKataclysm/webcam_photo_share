import time
import webbrowser

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from file_sharer import FileSharer

Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    """
    Kivy Screen for displaying video from the user's webcam. Includes a button
    for stopping and starting the recording, and a button for capturing an
    image from the recording. When the image is captured, it is saved as a
    PNG image file under the current timestamp.
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.file_path = None

    def start(self):
        """
        Starts the webcam recording, changes the camera texture to the current
        recording, and changes the text of the button to 'stop'.
        :return:
        """
        camera = self.ids.camera
        button = self.ids.camera_btn
        camera.play = True
        button.text = 'Stop Camera'
        camera.texture = camera._camera.texture

    def stop(self):
        """
        Stops the webcam recording, reverts the camera texture to an empty screen,
        and changes the text of the button to 'start'.
        :return:
        """
        camera = self.ids.camera
        button = self.ids.camera_btn
        camera.play = False
        button.text = 'Start Camera'
        camera.texture = None

    def capture(self):
        """
        Captures the current frame of the webcam recording and saves it as a
        PNG image file under the current timestamp, then displays the image
        Screen where the user can generate a shareable link to the image.
        :return:
        """
        # Save image under timestamp
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        self.file_path = f"files/{current_time}.png"
        camera = self.ids.camera
        camera.export_to_png(self.file_path)

        # Display image screen with captured image
        self.manager.current = 'image_screen'
        image_screen = self.manager.current_screen.ids.img
        image_screen.source = self.file_path


class ImageScreen(Screen):
    """
    Kivy Screen for displaying the image captured from the user's webcam and
    generating a shareable link to it.
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.url = None

    def create_link(self):
        """
        Access image file path, uploads it to FileStack and displays the url to
        the image in the Label widget.
        :return:
        """
        file_path = App.get_running_app().root.ids.camera_screen.file_path
        file_sharer = FileSharer(file_path)
        self.url = file_sharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """
        Copies the current image url to the clipboard if a shareable link has
        been generated.
        :return:
        """
        if self.url:
            Clipboard.copy(self.url)

    def open_link(self):
        """
        Open the shareable link to the image if it has been generated.
        :return:
        """
        if self.url:
            webbrowser.open(self.url)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
