#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2023-03-26 02:07:04 (ywatanabe)"
import os
import warnings

import openai
import speech_recognition as sr
import whisper
from gtts import gTTS


def s2t_unpaid(lpath_wav, language="EN"):
    """
    Speech to Text using a Google's product.

    Example:
        from scripts import audio, ml
        tmp_wav="/tmp/tmp.wav"
        audio.rec_wav_unlim(spath=tmp_wav)
        said = ml.s2t_unpaid(tmp_wav, language="EN")
        print(said)
        audio.play_audio(tmp_wav)
    """

    # print("\nText-to-speech ...\n")
    r = sr.Recognizer()
    with sr.AudioFile(lpath_wav) as source:
        audio = r.record(source)
    try:
        said_text = r.recognize_google(audio, language=language)
        # print(f"\nYou said:\n{said_text}\n")
        return said_text
    except Exception as e:
        print(e)


class ChatGPT(object):
    def __init__(
        self,
        system_setting="Please answer in a conversational manner as if you are my friend. "
        "I would be grateful if your response would be less than 20 words.",
    ):
        self.counter = 0
        openai.api_key = os.getenv("OPENAI_API_KEY") # "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"
        self.chat_history = []
        self.chat_history.append(
            {
                "role": "system",
                "content": system_setting,
            }
        )

    def __call__(self, text):
        self.counter += 1
        if text is None:
            text = ""
        try:
            self.chat_history.append({"role": "user", "content": text})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.chat_history,
                request_timeout=10,
                # max_tokens=30,
            )
            out_text = response["choices"][0]["message"]["content"]
            self.chat_history.append({"role": "assistant", "content": out_text})

            return out_text
        except Exception as e:
            print(e)
            out_text = "I could not catch you well."
            self.chat_history.append({"role": "assistant", "content": out_text})
            return out_text


# def t2t_chatGPT(text):
#     """
#     Text to text using ChatGPT by OpenAI.

#     Example:
#         from scripts import ml
#         out = ml.t2t_chatGPT("Please help me learn English.")
#         print(out)
#     """
#     openai.api_key = "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"
#     time_lim_sec = 10

#     try:
#         add_text = " Please answer in 20 words or less as if you are my friend."
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": text + add_text},
#             ],
#             request_timeout=time_lim_sec,
#             max_tokens=30,
#         )
#         responded_text = response["choices"][0]["message"]["content"]
#         return responded_text
#     except Exception as e:
#         print(e)
#         return "I could not catch you well."


def t2s(text, spath="/tmp/t2s.mp3", print_save=False):
    """
    Text to Speech using a Google's product.

    Example:
        from scripts import audio, ml
        # import utils
        text = "This is the test of my t2s function."
        spath="/tmp/t2s.mp3"
        ml.t2s(text, spath=spath)
        audio.play_audio(spath)
    """
    speech = gTTS(text=text, lang="en", slow=False)
    speech.save(spath)
    if print_save:
        print(f"Saved to: {spath}")


class Whisper(object):
    """
    Speach to text using Whisper by OpenAI.

    from scripts import audio, ml

    spath = "/tmp/test.wav"
    audio.rec_wav_unlim(spath=spath, fs=44100)

    mywhisper = Whisper()
    mywhisper(spath)
    """

    def __init__(
        self,
    ):
        self.model = whisper.load_model("base")

    def __call__(self, lpath):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result = self.model.transcribe(lpath)
        return result["text"]
