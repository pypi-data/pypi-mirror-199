#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2023-03-26 02:06:06 (ywatanabe)"

import audio2numpy as a2n
import numpy as np
import soundcard as sc
from scipy.io import wavfile
import threading
import readchar


class ThreadWithReturnValue(threading.Thread):
    """
    Example:
        t = ThreadWithReturnValue(
            target=func, args=(,), kwargs={key: val}
        )
        t.start()
        out = t.join()

    """

    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
    ):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


def load_wav_as_arr(lpath):
    fs, arr = wavfile.read(lpath)
    return fs, arr


def save_arr_as_wav(arr, spath, fs=44100, dtype=np.int16, does_print=False):
    arr = arr.astype(np.float64)
    # with warnings.catch_warnings():
    #     warnings.simplefilter("ignore", RuntimeWarning)
    arr /= arr.max()
    amp = np.iinfo(dtype).max
    arr *= amp
    wavfile.write(spath, fs, arr.astype(dtype))
    if does_print:
        print(f"Saved to: {spath}")


def play_arr(arr, fs=44100):
    """
    Example:
        fs = 44100
        arr = rec_arr(rec_sec=5, fs=fs)
        play_arr(arr, fs=fs)
    """
    # speakers = sc.all_speakers()
    default_speaker = sc.default_speaker()
    # print(default_speaker)
    default_speaker.play(arr / np.max(arr), samplerate=fs)


def play_audio(lpath, fs=None):
    """
    Example:
        fs = 44100
        spath="/tmp/test_rec_wav_unlim.wav"
        rec_wav_unlim(spath=spath, fs=fs)
        play_audio(spath)
    """
    arr, _fs = a2n.audio_from_file(lpath)
    fs = fs if fs is not None else _fs
    play_arr(arr, fs=fs)


def play_buzzer():
    play_audio("./data/buzzer.wav")


def rec_as_arr(rec_sec=5, fs=44100):
    """
    Example:
        arr = rec_as_arr(rec_sec=5, fs=44100)
        play_arr(arr, fs=fs)
    """
    # mics = sc.all_microphones()
    default_mic = sc.default_microphone()
    # print(default_mic)
    play_buzzer()
    arr = default_mic.record(samplerate=fs, numframes=fs * rec_sec)
    return arr


def rec_as_arr_unlim(fs=44100, print_press_q_message=True):
    """
    Records microphone input unlimitedly.

    Example:
        fs = 44100
        arr_unlim = rec_as_arr_unlim(fs=fs)
        play_arr(arr_unlim, fs=fs)
    """

    def _wait_space():
        pressed_key = None
        while pressed_key != " ":
            pressed_key = readchar.readchar()
        event.set()

    def _rec_as_arr_unlim():
        default_mic = sc.default_microphone()
        chunk_size = 2**14

        arr_unlim = []
        play_buzzer()

        with default_mic.recorder(samplerate=fs) as mic:
            while not event.is_set():
                data = mic.record(numframes=chunk_size)
                arr_unlim.append(data)
        return np.vstack(arr_unlim).astype(np.float64)

    if print_press_q_message:
        print("\nSPACE: Stop recording.\nSPACE -> Ctrl + C: Stop the session.\n")

    event = threading.Event()
    t1 = ThreadWithReturnValue(target=_wait_space)
    t2 = ThreadWithReturnValue(target=_rec_as_arr_unlim)

    t1.start()
    t2.start()

    return t2.join()


def rec_as_wav(spath="/tmp/test_rec_as_wav_unlim.wav", rec_sec=5, fs=44100):
    """
    Example:
        rec_sec = 5
        fs = 44100
        spath="/tmp/test_rec_as_wav.wav"
        arr = rec_as_wav(spath=spath, rec_sec=rec_sec, fs=fs)
    """
    play_buzzer()
    arr = rec_as_arr(rec_sec=rec_sec, fs=fs)
    save_arr_as_wav(arr, spath, fs=fs)


def rec_as_wav_unlim(
    spath="/tmp/test_rec_as_wav_unlim.wav", fs=44100, print_press_q_message=True
):
    """
    Example:
        fs = 44100
        spath="/tmp/test_rec_as_wav_unlim.wav"
        rec_as_wav_unlim(spath=spath, fs=fs)
    """
    arr = rec_as_arr_unlim(fs=fs, print_press_q_message=print_press_q_message)
    save_arr_as_wav(arr, spath=spath, fs=fs)


if __name__ == "__main__":
    fs = 44100
    arr_unlim = rec_as_arr_unlim(fs=fs)
    play_arr(arr_unlim, fs=fs)
