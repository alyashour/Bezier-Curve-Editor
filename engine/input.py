import glfw

class InputManager:
    def __init__(self, window):
        self.window = window
        self.mouse_clicks = []  # Store mouse clicks
        self.keys_pressed = set()  # Store currently pressed keys
        self.callbacks = {} # Store registered callbacks
        self.is_dragging = False

        # Subscribe glfw callbacks
        glfw.set_mouse_button_callback(window, self.process_mouse_btn_press)
        glfw.set_key_callback(window, self.process_keypress)
        glfw.set_cursor_pos_callback(window, self.process_mouse_move)

    def register_callback(self, event_name, callback, key_filter=None):
        """Attach a callback to an event.
        event_name: a string like "left_click", "key_press", etc.
        callback: a function to call when the event occurs.
        """
        if event_name not in self.callbacks:
            self.callbacks[event_name] = []

        if event_name == "key_press" and key_filter is not None:
            def wrapper(key, scancode, mods):
                if key == key_filter:
                    callback(key, scancode, mods)
            self.callbacks[event_name].append(wrapper)
            return

        self.callbacks[event_name].append(callback)
    
    def trigger_callbacks(self, event_name, *args, **kwargs):
        """Call all callbacks registered for event_name with provided arguments."""
        if event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(*args, **kwargs)

    def get_scaled_mouse_position(self, x, y):
        """ 
        Convert window coordinates to framebuffer coordinates. 
        This is needed on HDPI displays like mine. Also flips the y coordinates since 
        glfw coords start in the bottom left while opengl starts in the top left.
        """
        win_width, win_height = glfw.get_window_size(self.window)
        fb_width, fb_height = glfw.get_framebuffer_size(self.window)

        # Scale mouse coordinates to framebuffer size
        x_scaled = (x / win_width) * fb_width
        y_scaled = fb_height - (y / win_height) * fb_height  # Flip Y-axis

        return x_scaled, y_scaled

    # a lot of unused params because these are callbacks for glfw
    def process_mouse_btn_press(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = self.get_scaled_mouse_position(*glfw.get_cursor_pos(window))

            # Trigger any registered left_click callbacks, passing the position
            self.trigger_callbacks("left_click", x, y)

            self.is_dragging = True
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
            self.is_dragging = False
            x, y = self.get_scaled_mouse_position(*glfw.get_cursor_pos(window))
            self.trigger_callbacks("left_release", x, y)

    def process_mouse_move(self, window, x, y):
        x_scaled, y_scaled = self.get_scaled_mouse_position(x, y)
        self.trigger_callbacks("mouse_move", x_scaled, y_scaled)

    def process_keypress(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.trigger_callbacks("key_press", key, scancode, mods)
        elif action == glfw.RELEASE:
            self.keys_pressed.add(key)
            self.trigger_callbacks("key_release", key, scancode, mods)

    def get_mouse_clicks(self):
        """ Get scaled mouse click positions. """
        clicks = []
        for button, (x, y) in self.mouse_clicks:
            x_scaled, y_scaled = self.get_scaled_mouse_position(x, y)
            clicks.append((button, x_scaled, y_scaled))
        
        self.mouse_clicks.clear()
        return clicks

    def is_key_down(self, *keys):
        """Returns True if any of the provided keys are currently pressed."""
        for key in keys:
            if key in self.keys_pressed:
                return True
        return False
