import glfw
from OpenGL.GL import *

class Window:
    def __init__(self, width: int=800, height: int=600, title: str="Unnamed Window", multisample_rate: int=None):
        self.DO_MULTISAMPLE = multisample_rate is not None

        # initialize glfw if not already
        if not glfw.init():
            raise Exception("GLFW can't be initialized")
        
        # save params
        self.width = width
        self.height = height

        # if multisample, set window hint
        if self.DO_MULTISAMPLE:
            glfw.window_hint(glfw.SAMPLES, multisample_rate)

        # create window
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created")
        
        # enable multisample if needed
        if self.DO_MULTISAMPLE:
            print('Multisampling enabled.')
            glEnable(GL_MULTISAMPLE)
        
        # set resize callback
        glfw.set_window_size_callback(self.window, self.window_resize)

        # switch context
        glfw.make_context_current(self.window)

    def get_framebuffer_size(self):
        return glfw.get_framebuffer_size(self.window)

    def set_viewport(self, width, height):
        glViewport(0, 0, width, height)

    def set_ortho(self, left, right, bottom, top, z_near, z_far):
        glOrtho(left, right, bottom, top, z_near, z_far)

    def window_resize(self, width, height):
        self.width = width
        self.height = height
        self.set_viewport(width, height)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def poll_events(self):
        glfw.poll_events()

    def terminate(self):
        glfw.terminate()
