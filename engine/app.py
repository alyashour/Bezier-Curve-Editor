from abc import ABC, abstractmethod

import glfw

from .window import Window
from .renderer import Renderer
from .input import InputManager

class App(ABC):
    def __init__(self, window_width, window_height, window_name, multisample_rate=None):
        # create the window
        self.window = Window(window_width, window_height, window_name, multisample_rate)
        fb_width, fb_height = self.window.get_framebuffer_size() # have to use framebuffer size instead of window size because of hdpi scaling on hdpi monitors like mine
        self.window.set_viewport(fb_width, fb_height)
        self.window.set_ortho(0, fb_width, 0, fb_height, -1, 1)

        # create the renderer
        self.renderer = Renderer()

        # create the input manager
        self.input_manager = InputManager(self.window.window)

    @abstractmethod
    def draw(self):
        """Called each frame."""
        pass

    def should_close(self) -> bool:
        """
        Should return true when the app should close.
        """
        return self.input_manager.is_key_down(glfw.KEY_ESCAPE)

    def run(self):
        # main loop
        while not self.window.should_close():
            self.window.poll_events()

            # Process keyboard input
            if self.should_close():
                print("Exit key pressed. Exiting...")
                break  # Exit main loop

            # Render scene
            self.renderer.clear()

            self.draw()
            self.window.swap_buffers()

        self.window.terminate()

    def __call__(self):
        self.run()
