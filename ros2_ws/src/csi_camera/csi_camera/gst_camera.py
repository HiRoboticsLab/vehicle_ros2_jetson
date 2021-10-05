import gi
gi.require_version('Gst', '1.0')
import atexit
from gi.repository import GObject, Gst
import numpy as np

Gst.init(None)

class GstCamera(object):
    
    def __init__(self, sensor_mode=4, width=640, height=360, fps=30, capture_width=640, capture_height=360, flip_method=2):
        
        self.mainloop = GObject.MainLoop()
        
        print(sensor_mode)
        GST_STRING = \
            'nvarguscamerasrc sensor-mode={sensor_mode} ! '\
            'video/x-raw(memory:NVMM), '\
            'width=(int){capture_width}, height=(int){capture_height}, '\
            'format=(string)NV12, framerate=(fraction){fps}/1 ! '\
            'nvvidconv flip-method={flip_method} ! '\
            'video/x-raw, width=(int){width}, height=(int){height}, format=(string)BGRx ! '\
            'videoconvert ! '\
            'video/x-raw, format=(string)BGR ! '\
            'appsink name=sink'\
            .format(
                sensor_mode=sensor_mode,
                width=width, 
                height=height, 
                fps=fps, 
                capture_width=capture_width,
                capture_height=capture_height,
                flip_method=flip_method
            )
        print(GST_STRING)
        
        self.pipeline = Gst.parse_launch(GST_STRING)
        
        appsink = self.pipeline.get_by_name('sink')

        appsink.set_property('emit-signals', True)
        appsink.set_property('max-buffers', 1)
        appsink.connect('new-sample', self._on_new_sample)
        
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self._on_eos)
        self.bus.connect("message::error", self._on_error)
        
        self._on_image_callbacks = set()
        
        atexit.register(self.stop)
        
    
    def __del__(self):
        self.stop()
        
    def on_image(self, callback):
        self._on_image_callbacks.add(callback)
        
    def _on_new_sample(self, appsink):
        sample = appsink.emit('pull-sample')
        buf = sample.get_buffer()
        caps = sample.get_caps()
        height = caps.get_structure(0).get_value('height')
        width = caps.get_structure(0).get_value('width')
        (result, mapinfo) = buf.map(Gst.MapFlags.READ)

        image = np.ndarray(
            shape=(height, width, 3),
            buffer=buf.extract_dup(0, buf.get_size()),  # extract_dup to copy
            dtype=np.uint8
        )
        
        for cb in self._on_image_callbacks:
            cb(image)
            
        buf.unmap(mapinfo)
        
        return Gst.FlowReturn.OK
    
    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.mainloop.run()
        
    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.mainloop.quit()
        
    def _on_eos(self, bus, msg):
        self.stop()
    
    def _on_error(self, bus, msg):
        self.stop()