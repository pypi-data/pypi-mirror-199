#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2023-03-26 14:39:40 (ywatanabe)"

import os
import time

from vChatGPT.scripts import audio, ml, utils


def s2s(chatgpt):
    ID = utils.gen_ID()
    os.makedirs("/tmp/vChatGPT", exist_ok=True)

    # Records a microphone input
    spath_in_wav = f"/tmp/vChatGPT/input-{ID}.wav"
    audio.rec_as_wav_unlim(
        spath=spath_in_wav,
        print_press_q_message=True if chatgpt.counter == 0 else False,
    )
    time.sleep(0.1)

    # Speech to text
    # if "mywhisper" not in globals():
    #     mywhisper = utils.Whisper()
    # said = mywhisper(spath_in_wav)
    said = ml.s2t_unpaid(spath_in_wav, language="EN")
    print(said)

    # Text to text (using ChatGPT)
    # gpt_out = ml.t2t_chatGPT(said)
    gpt_out = chatgpt(said)
    print(gpt_out)
    print()

    # Text to speech
    spath_out_mp3 = f"/tmp/vChatGPT/output-{ID}.mp3"
    ml.t2s(gpt_out, spath=spath_out_mp3, print_save=False)

    # Plays the ChatGPT's output
    audio.play_audio_file(spath_out_mp3)


def main():
    chatgpt = ml.ChatGPT()
    while True:
        s2s(chatgpt)


if __name__ == "__main__":
    main()
