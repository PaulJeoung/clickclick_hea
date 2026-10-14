from pynput import mouse

class PositionCapturer:
    def __init__(self, callback):
        self.listener = None
        self.callback = callback

    def start(self):
        self.stop()

        def on_click(x, y, button, pressed):
            if pressed:
                btn_name = "left" if button == mouse.Button.left else "right"
                self.callback(int(x), int(y), btn_name)
                return False  # 1회 감지 후 리스너 자동 해제

        self.listener = mouse.Listener(on_click=on_click)
        self.listener.daemon = True
        self.listener.start()

    def stop(self):
        if self.listener and self.listener.is_alive():
            self.listener.stop()
        self.listener = None