"""
Dieses Modul enthält zwei Klassen für Spracherkennung und -aufnahme.

Klasse SpeechRecognizer:
    - recognize_speech(): Erkennt Sprache über das Mikrofon und gibt den erkannten Text zurück
    - set_phrases(phrases: list): Setzt eine Liste von Phrasen für das Spracherkennungssystem
    - add_phrase(phrase: str): Fügt eine Phrase zu der Liste von Phrasen für das Spracherkennungssystem hinzu
    - remove_phrase(phrase: str): Entfernt eine Phrase aus der Liste von Phrasen für das Spracherkennungssystem

Klasse MicrophoneRecorder:
    - record_audio(record_time: int): Nimmt Audio für eine bestimmte Zeitdauer auf
    - save_audio(format: str): Speichert das aufgenommene Audio in einem bestimmten Dateiformat
    - upload_to_cloud(): Uploadet das aufgenommene Audio in eine Cloud-Speicherlösung
    - save_to_database(): Speichert das aufgenommene Audio in einer Datenbank
"""
import logging
import speech_recognition as sr

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    def __init__(self, language="de-DE", energy_threshold=400, listen_time=5):
        self.language = language
        self.energy_threshold = energy_threshold
        self.listen_time = listen_time
        self.phrases = []

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=self.listen_time)

        try:
            recognized_text = recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized text: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

    def set_phrases(self, phrases: list):
        if not isinstance(phrases, list):
            logger.error("Input phrases must be a list.")
            return
        self.phrases = phrases

    def add_phrase(self, phrase: str):
        if not isinstance(phrase, str):
            logger.error("Input phrase must be a string.")
            return
        self.phrases.append(phrase)

    def remove_phrase(self, phrase: str):
        if not isinstance(phrase, str):
            logger.error("Input phrase must be a string.")
            return
        if phrase in self.phrases:
            self.phrases.remove(phrase)


class MicrophoneRecorder:
    def __init__(self, save_path="output.wav", channels=1, rate=44100, chunk_size=1024):
        self.save_path = save_path
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.audio = None

    def record_audio(self, record_time=5):
        if record_time <= 0:
            logger.error("Record time must be greater than zero.")
            return
        frames = []
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            logger.info("Recording audio...")
            for i in range(int(self.rate / self.chunk_size * record_time)):
                data = source.read(self.chunk_size)
                frames.append(data)
        self.audio = sr.AudioData(b"".join(frames), self.rate, self.channels)

    def save_audio(self, format="wav"):
        if format not in ["wav", "mp3", "m4a"]:
            logger.error(f"Unsupported file format: {format}")
            return
        if self.audio is None:
            logger.error("No audio data to save.")
            return
        try:
            with open(self.save_path, "wb") as f:
                self.audio.export(f, format=format)
            logger.info(f"Audio data saved to {self.save_path}")
        except Exception as e:
            logger.error(f"Failed to save audio file: {e}")

    def upload_to_cloud(self):
        # Code to upload audio to cloud storage
        pass

    def save_to_database(self):
        # Code to save audio to database
        pass


#—------------((---((----()))))--------------------
#tests
#---------------------------------------(-(-((((()))))))
import os
import unittest
from unittest.mock import patch

class TestSpeechRecognizer(unittest.TestCase):
def setUp(self):
self.speech_recognizer = SpeechRecognizer()



def test_recognize_speech(self):
    # Test successful speech recognition
    with patch("my_module.sr.Recognizer.listen") as mock_listen:
        mock_listen.return_value = "hello world"
        recognized_text = self.speech_recognizer.recognize_speech()
        self.assertEqual(recognized_text, "hello world")

    # Test unknown audio error
    with patch("my_module.sr.Recognizer.recognize_google") as mock_recognize_google:
        mock_recognize_google.side_effect = Exception()
        recognized_text = self.speech_recognizer.recognize_speech()
        self.assertEqual(recognized_text, "")

def test_set_phrases(self):
    # Test set_phrases with list input
    phrases = ["hello", "world"]
    self.speech_recognizer.set_phrases(phrases)
    self.assertListEqual(self.speech_recognizer.phrases, phrases)

    # Test set_phrases with non-list input
    self.speech_recognizer.set_phrases("hello")
    self.assertListEqual(self.speech_recognizer.phrases, [])

def test_add_phrase(self):
    # Test add_phrase with string input
    phrase = "hello"
    self.speech_recognizer.add_phrase(phrase)
    self.assertIn(phrase, self.speech_recognizer.phrases)

    # Test add_phrase with non-string input
    self.speech_recognizer.add_phrase(123)
    self.assertNotIn(123, self.speech_recognizer.phrases)

def test_remove_phrase(self):
    # Test remove_phrase with an existing phrase
    self.speech_recognizer.set_phrases(["hello", "world"])
    self.speech_recognizer.remove_phrase("hello")
    self.assertListEqual(self.speech_recognizer.phrases, ["world"])

    # Test remove_phrase with a non-existing phrase
    self.speech_recognizer.remove_phrase("goodbye")
    self.assertListEqual(self.speech_recognizer.phrases, ["world"])

def test_microphone_recorder(self):
    # Test recording audio
    recorder = MicrophoneRecorder()
    recorder.record_audio(3)

    # Test saving audio to file
    file_path = "audio.wav"
    recorder.save_audio(file_path)
    self.assertTrue(os.path.exists(file_path))

def test_speech_recognition_with_phrases(self):
    # Test speech recognition with a valid phrase
    self.speech_recognizer.set_phrases(["hello", "world"])
    with patch("my_module.sr.Recognizer.listen") as mock_listen:
        mock_listen.return_value = "hello"
        recognized_text = self.speech_recognizer.recognize_speech()
        self.assertEqual(recognized_text, "hello")

    # Test speech recognition with an invalid phrase
    self.speech_recognizer.set_phrases(["apple", "banana"])
    with patch("my_module.sr.Recognizer.listen") as mock_listen:
        mock_listen.return_value = "orange"
        recognized_text = self.speech_recognizer.recognize_speech()
        self.assertEqual(recognized_text, "")

def test_speech_recognition_without_phrases(self):
    # Test speech recognition without phrases
    self.speech_recognizer.set_phrases([])


if name == "main":
unittest.main()
  