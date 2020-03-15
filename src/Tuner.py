import sys
import numpy as np
from PyQt5 import Qt
import pyqtgraph as pg
import pyaudio as pa
from argparse import Namespace
from music import Note

flags = Namespace(
    chunk=4096,
    fftWindow=8192,
)


def getDeviceNumber(p) -> (int, int):
    n = p.get_device_count()
    # USB input device is preferred
    for i in range(n):
        device_info = p.get_device_info_by_index(i)
        if "USB" in device_info["name"] and device_info["maxInputChannels"] > 0:
            return i, device_info["maxInputChannels"]
    for i in range(n):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            return i, device_info["maxInputChannels"]
    raise ConnectionError("No sound input device found")


def openStream(rate: int):
    p = pa.PyAudio()
    device_index, n_channels = getDeviceNumber(p)
    stream = p.open(
        format=pa.paFloat32,
        channels=n_channels,
        rate=rate,
        input=True,
        frames_per_buffer=flags.chunk,
        input_device_index=device_index,
        start=False
    )
    return stream


class Tuner(Qt.QGuiApplication):
    def __init__(self,
                 stream,
                 rate: int,
                 lowest: Note = Note.C(2),
                 highest: Note = Note.C(8),
                 List=[]) -> None:
        super().__init__(List)
        self.rate = rate
        self.stream = stream
        self.lowest = lowest
        self.highest = highest
        self.fftWindow = flags.fftWindow
        self.savingRange = 44100  # 1 second
        self.timer = Qt.QTimer()
        self.timer.timeout.connect(self.update)
        self.app = Qt.QApplication(sys.argv)
        self.window = pg.GraphicsWindow(title="PyTuner")
        self.window.setGeometry(5, 115, 1910, 1070)

        sp_labels = [(np.log10(Note(i).freq), Note(i).name()) for i in range(-48, 94)]
        sp_x_axis = pg.AxisItem(orientation='bottom')
        sp_x_axis.setTicks([sp_labels])
        self.spectrum_plot = self.window.addPlot(
            title="Sound spectrum",
            row=1, col=1,
            axisItems={'bottom': sp_x_axis}
        )
        self.spectrum_trace = None
        self.spectrum_trace2 = None
        self.spectrum_plot.setXRange(
            np.log10(self.lowest.freq),
            np.log10(self.highest.freq),
            padding=0.005
        )

        self.f = np.linspace(1, self.rate / 2, self.fftWindow // 2)
        self.input_data = np.zeros((self.savingRange,), dtype=float)
        self.spectral_data = np.zeros((self.fftWindow // 2,), dtype=float)

        self.draw_note_lines()
        self.start()

    def draw_note_lines(self):
        for i in range(-48, 94):
            if i % 12 in {0, 2, 4, 5, 7, 9, 11}:
                color = 'r'
            else:
                color = 'b'
            if i % 12 == 0:
                thickness = 0.5
            else:
                thickness = 0.35
            inf_line = pg.InfiniteLine(
                movable=True,
                angle=90,
                label=Note(i).name(),
                pen=pg.mkPen(color, width=thickness))
            inf_line.setPos([np.log10(Note(i).freq), 0])
            self.spectrum_plot.addItem(inf_line)

    def update(self) -> None:
        try:
            wf_data = self.stream.read(flags.chunk, exception_on_overflow=False)
            wf_data = np.frombuffer(wf_data, dtype=float)
            if np.size(wf_data) == 0:
                return
            self.input_data = np.hstack((self.input_data[wf_data.shape[0]:], wf_data))

            input_last = self.input_data[:self.fftWindow]
            # Normalization
            input_last = input_last / np.sqrt((np.sum(np.square(input_last)) + 1e-6))
            self.spectral_data = np.fft.fft(input_last)
            self.spectral_data = np.abs(self.spectral_data[:self.fftWindow // 2])
            if np.sum(self.spectral_data) > 0:
                self.spectrum_trace2 = self.spectrum_trace
                self.spectrum_trace = self.spectrum_plot.plot(pen='m', width=3)
                self.spectrum_trace.setData(self.f, self.spectral_data)
                self.spectrum_plot.setLogMode(x=True, y=True)
                self.spectrum_plot.setYRange(-13, 2, padding=0.001)
                self.spectrum_plot.setXRange(np.log10(Note.C(4).freq), np.log10(Note.C(8).freq), padding=0.005)
                if self.spectrum_trace2 is not None:
                    self.spectrum_plot.removeItem(self.spectrum_trace2)
        except IOError:
            pass  # underflow, waiting for data

    def start(self) -> None:
        self.stream.start_stream()
        self.timer.start(10)
