import os
import subprocess
import uuid
from typing import List

from dataclasses import dataclass

from telegram import Voice
from voicekit.library_voicekit import stt_wav_to_string


def message_to_text(update, context, send_back_voice=True):
    if update.message.voice:
        tmp_name = str(uuid.uuid4())
        tmp_ogg = tmp_name + ".ogg"
        tmp_wav = tmp_name + ".wav"

        voice_obj = update.message.voice
        voice_file = Voice(voice_obj.file_id, voice_obj.file_unique_id, voice_obj.duration, bot=context.bot)
        voice_file.get_file(timeout=100).download(tmp_ogg)

        process = subprocess.run(["ffmpeg", "-i", tmp_ogg, tmp_wav])
        if process.returncode != 0:
            raise Exception("Can not convert .ogg to .wav!")

        text = stt_wav_to_string(tmp_wav)

        if send_back_voice:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"\"{text}\"")

        os.remove(tmp_ogg)
        os.remove(tmp_wav)

        return text

    return update.message.text


@dataclass
class AnswerOption:
    letter: str
    text: str
    is_correct: bool


@dataclass
class CaseAction:
    is_up: bool
    amount: int


@dataclass
class Case:
    body: str
    choices: List[CaseAction]
