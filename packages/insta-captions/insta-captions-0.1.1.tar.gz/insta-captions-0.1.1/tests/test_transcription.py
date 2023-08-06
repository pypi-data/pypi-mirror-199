from src.transcription import read_from_wav, wav_to_text, transcribe
import unittest
from deepspeech import Model as dsm

models = {
    "english": "data/language_models/deepspeech-0.9.3-models.pbmm",
    "mandarin": "data/language_models/deepspeech-0.9.3-models-zh-CN.pbmm",
}

lm = {
    "english": "data/language_models/deepspeech-0.9.3-models.scorer",
    "mandarin": "data/language_models/deepspeech-0.9.3-models-zh-CN.scorer",
}

alphabeta = {
    "english": {"alpha": 0.931289039105002, "beta": 1.1834137581510284},
    "mandarin": {"alpha": 0.6940122363709647, "beta": 4.777924224113021},
}

beam_width = 100


class TestTranscribe(unittest.TestCase):

    """
    An empty wav file is not actually empty, it has metadata.
    This empty wav was grabbed from a website
    Audio in CD's usually stored at 44.1 kHz (44100) Hz
    The buffer is a binary hex, but it is 0 as the wav is empty
    """

    def test_empty_wav(self):
        rate, buffer = read_from_wav("tests/testempty.wav")
        self.assertEqual(rate, 44100)
        self.assertEqual(buffer, b"\x00")

    """
    The rate is different here as the audio of this example file,
    as well as audio streams from the microphone are 16000 Hz
    which is more useful to this project
    """

    def test_wav(self):
        rate, buffer = read_from_wav("data/audio/english_examples/8455-210777-0068.wav")
        self.assertEqual(rate, 16000)
        self.assertNotEqual(buffer, b"\x00")

    def test_empty_english_text(self):
        language = "english"
        model = dsm(models[language])
        model.enableExternalScorer(lm[language])

        model.setScorerAlphaBeta(alphabeta[language]["alpha"], alphabeta[language]["beta"])
        model.setBeamWidth(beam_width)

        text = wav_to_text(model, "tests/testempty16.wav")
        self.assertEqual(text, "")

    def test_empty_mandarin_text(self):
        language = "mandarin"
        model = dsm(models[language])
        model.enableExternalScorer(lm[language])
        model.setScorerAlphaBeta(alphabeta[language]["alpha"], alphabeta[language]["beta"])
        model.setBeamWidth(beam_width)

        text = wav_to_text(model, "tests/testempty16.wav")
        self.assertEqual(text, "")

    def test_english_text(self):
        language = "english"
        model = dsm(models[language])
        model.enableExternalScorer(lm[language])
        model.setScorerAlphaBeta(alphabeta[language]["alpha"], alphabeta[language]["beta"])
        model.setBeamWidth(beam_width)

        text = wav_to_text(model, "data/audio/english_examples/8455-210777-0068.wav")
        self.assertNotEqual(text, "")

    def test_mandarin_text(self):
        language = "mandarin"
        model = dsm(models[language])
        model.enableExternalScorer(lm[language])
        model.setScorerAlphaBeta(alphabeta[language]["alpha"], alphabeta[language]["beta"])
        model.setBeamWidth(beam_width)

        text = wav_to_text(model, "data/audio/chinese_examples/myname.wav")
        self.assertNotEqual(text, "")

    def test_english_integration(self):
        wavs = [
            "data/audio/english_examples/2830-3980-0043.wav",
            "data/audio/english_examples/4507-16021-0012.wav",
            "data/audio/english_examples/8455-210777-0068.wav",
        ]

        texts = transcribe(wavs, "english")
        self.assertEqual(len(texts), 3)
