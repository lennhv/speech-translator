
import time
import logging
import argparse

import pyttsx3
from googletrans import Translator, constants
import speech_recognition as sr

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


class VoiceTranslator:
    source_lang = None
    dest_lang = None
    voice_speed = None
    voice_volume = 0.5
    voice_gender = 'neutro'
    voice_profile = None
    speech_enable = True
    voice_engine = None
    translator_engine = Translator()
    recognition_speech_engine = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            log.debug("%s: %s", k, v)
            setattr(self, k, v)

    def _get_voice_profile(self):
        """ if the speech to text is enable
            search the best voice profile based on
            the gender configured
        """
        if not self.speech_enable:
            return
        for voice in self.voice_engine.getProperty('voices'):
            if self.voice_gender not in voice.gender.lower():
                continue
            # specific language region
            langs = [l.lower() for l in voice.languages]
            # neutral language
            _langs = [l.split('_')[0] for l in langs]
            if self.dest_lang.lower() in langs:
                self.voice_profile = voice.id
                break
            elif dest_lang.lower().split('_')[0] in _langs:
                # not break because is searching for the best match
                # voice profile
                self.voice_profile = voice.id

    def _get_voice_engin_conf(self):
        if not self.speech_enable:
            log.info("Voice engine is not enabled")
            return
        log.info("voice profile: %s", self.voice_profile)
        log.info("voice volume: %s", self.voice_volume)
        log.info("voice speed: %s", self.voice_speed)

    def setup_voice_engine(self):
        """ setup voice engine for the
            speech to text if is enabled
        """
        if not self.speech_enable:
            return
        self.voice_engine = pyttsx3.init()
        self._get_voice_profile()
        self.voice_engine.setProperty('voice', self.voice_profile)
        self.voice_engine.setProperty('rate', self.voice_speed)

    def speech_to_text(self, phrase):
        """ speech a text with a especific voice
        """
        if not self.speech_enable:
            log.debug("speech to textnot enabled", phrase)
            return
        log.debug("speech to text: %s", phrase)
        self.voice_engine.say(phrase)
        self.voice_engine.runAndWait()

    def translator(self, text):
        """translate a text 
        """
        t = self.translator_engine.translate(text,
                                             src=self.source_lang, dest=self.dest_lang)
        translated_text = t.text
        log.debug("translated text: %s", translated_text)
        return translated_text

    def listener(self, recognizer, audio):
        """received audio data and recognize it using Speech Recognition
        """
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = self.recognition_speech_engine.recognize_google(audio)
            ttext = self.translator(text)
            self.speech_to_text(ttext)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

    def configure_speech_recongnition(self):
        self.recognition_speech_engine = sr.Recognizer()
        self.mic = sr.Microphone()
        with self.mic as source:
            # calibrate mic
            log.debug("adjust for ambient noise")
            self.recognition_speech_engine.adjust_for_ambient_noise(source)
            log.debug("ambient noise calibrated")

    def run(self):
        self.setup_voice_engine()
        self._get_voice_engin_conf()
        self.configure_speech_recongnition()
        speech_listener = self.recognition_speech_engine.\
            listen_in_background(self.mic, self.listener)
        log.info("Listening...")
        while True:
            try:
                time.sleep(0.01)
            except KeyboardInterrupt:
                log.info("stop listening")
                speech_listener(wait_for_stop=False)
                if self.speech_enable:
                    self.voice_engine.stop()
                # wair for fishish listen thread
                for _ in range(20):
                    time.sleep(0.1)
                break

