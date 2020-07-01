# Python DSP tools
Multiple DSP tools in permanent development.
## Tool 1: Bokus (Mic) Multiband Filter
This subproject provides a multiband filter with the sole purpose of testing Python's performance for FIR filtering techniques.
### Features
* Up to 48 kHz sampling rate.
* Audio playback.
* Finite impulse response filters using windowing methods: Rectangular, Bartlett, Hann, Hamming and Blackman.
* Devil mode changing voice pitch to sound like a demon.
* Personalized GUI using Qt libraries.
* To be implemented: IIR filters. Goblin filters (to sound like a fairy tale cute character).
* To be implemented: input and output device selection.

![]()<p align="center"><img src="https://raw.githubusercontent.com/fedeboco/python-dsp/master/mic/assets/app-preview.png?raw=true"></p>

### Dependencies
* PyAudio
* PyQt (Pyside2)
* Numpy
* Optional: matplotlib (for testing filters)

### Pending
* Error control
* Butterworth filtering
* Goblin filtering
* Detailed settings

### PyAudio and PyQt install
```
pip install PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl
pip install PySide2
```
