import argparse
from api import VoiceTranslator


parser = argparse.ArgumentParser(description='Voice traslator.\nListen voice '\
    'from mic and traslate it, translated text can be speeched or only show text according with args passed',)

parser.add_argument('--source-lang',type=str, required= True,
                    help='Voice language, example `en` ot `en_US` for english, `es` or `es_MX` for spanish, etc.')

parser.add_argument('--dest-lang',type=str, required= True,
                    help='Language to traslate text, example `en_US` for english, `es_MX` for spanish, etc.')

parser.add_argument('--gender',type=str, default='male',
                    choices=['male', 'female', 'neutral'], help='Gender for the voice')

parser.add_argument('--no-speech-text', action='count', default=0)

parser.add_argument('--voice-speed',type=float, default=120.0,
                    help='Voice speed for speech text')

parser.add_argument('--voice-volume',type=float, default=0.7,
                    help='speech volume from 0.0 to 1.0')
args = parser.parse_args()


VoiceTranslator(
    source_lang = args.source_lang,
    dest_lang = args.dest_lang,
    voice_speed = args.voice_speed,
    voice_volume = args.voice_volume,
    voice_gender = args.gender,
    speech_enable = True if args.no_speech_text == 0 else False
).run()


