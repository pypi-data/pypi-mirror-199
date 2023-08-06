try:
    import dxcam
    from ninja_tools.bbox import BBOX
except ImportError:
    raise 'pip install ninjatools[all]  to use fast capture!'


class FastCapture:
    def __init__(self, color="BGR"):
        self.camera = dxcam.create(output_color=color)

    def capture(self, bbox: BBOX = None):
        if bbox:
            return self.camera.grab(region=bbox())

        return self.camera.grab()
