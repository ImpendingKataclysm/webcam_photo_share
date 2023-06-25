import time

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from file_sharer import FileSharer

Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    """
    A Kivy Screen for displaying video from the user's webcam. Includes a button
    for stopping and starting the recording, and a button for capturing an
    image from the recording.
    """
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
        Screen where the user can generate a shareable link.
        :return:
        """
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f"files/{current_time}.png"
        camera = self.ids.camera
        camera.export_to_png(file_path)
        self.manager.current = 'image_screen'


class ImageScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
