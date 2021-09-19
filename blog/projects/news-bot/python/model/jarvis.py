import speech_recognition as sr
import pyttsx3
from model.newsApi import NewsApiImpl

from queue import Queue, Full

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from model.ibm_recognizers import IBMRecognitionCallback
import pyaudio
from threading import Thread

class Jarvis:
    def __init__(
      self, news_api_key, 
      ibm_username="", ibm_password="", 
      ibm_api_key="", ibm_api_url="https://api.us-east.speech-to-text.watson.cloud.ibm.com",
      recognizer_type = "sr_google"
    ):
        self.recognizer    = sr.Recognizer()
        self.news_fetcher  = NewsApiImpl(news_api_key)
        self.ibm_api_key   = ibm_api_key
        self.ibm_api_url   = ibm_api_url
        self.recognizer_type = recognizer_type

        self.speech_engine = self.__init_engine(
            voice="com.apple.speech.synthesis.voice.daniel"
        )

        self.bytes_heard     = []
        self.files_responded = []
    
    def __init_engine(
            self, 
            voice="com.apple.speech.synthesis.voice.samantha",
            rate=150
        ):
        engine = pyttsx3.init() 
        engine.setProperty('rate', rate)
        engine.setProperty('voice', voice)
        return engine

    def __init_watson(self, audio_source):
        authenticator = IAMAuthenticator(self.ibm_api_key)
        spech_to_text = SpeechToTextV1(authenticator=authenticator)
        spech_to_text.set_service_url(self.ibm_api_url)
        return spech_to_text

    def __recognize_audio(self, audio):
      try:
        return self.recognizer.recognize_google(audio)
      except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
      except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return None

    def __recognize_audio_callback(self, audio_source, callback):
       self.watson_ws_speech_to_text.recognize_using_websocket(
          audio=audio_source,
          content_type='audio/l16; rate=16000',
          recognize_callback=callback,
          interim_results=True,
          background_audio_suppression=0.6,
          inactivity_timeout=2
        )

    def __text_to_speech(self, translated):
      self.speech_engine.say(translated)
      self.speech_engine.runAndWait()

    def fetch_news(self, kind="good"):
        if (kind == "good"):
            return self.news_fetcher.get_happy_news()
        return self.news_fetcher.get_random_article()

    def act(self):
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... one second please!")
            self.recognizer.adjust_for_ambient_noise(source)
            while(True):
                translated = None
                print("I am waiting for your next order")
                audio = self.recognizer.listen(source)
                translated = self.__recognize_audio(audio)
                if (translated): 
                    print(f"Translated {translated}")
                    if ("goodbye" in translated): 
                      self.__text_to_speech("goodbye")
                      return
                    else:
                      self.__text_to_speech("oh hello")
                      new_command = self.act_ibm_websockets()
                      if ("knock") in new_command:
                        self.__text_to_speech("oh gosh whos there")
                        is_there = self.act_ibm_websockets()
                        self.__text_to_speech(f"{is_there} who")
                        final_act = self.act_ibm_websockets()
                        self.__text_to_speech("please stop")
                    # if ("news" in translated):
                    #     article = self.fetch_news()
                    #     self.__text_to_speech(article)
    
    def pyaudio_to_ibm_audio(self, data_in, frame_count, time_info, status):
          try:
            self.queue.put(data_in)
          except Full:
            pass
          return (None, pyaudio.paContinue)
    
    def act_ibm_websockets(self):
        chunk        = 1024
        buf_max_size = chunk * 10
        self.queue   = Queue(maxsize=int(round(buf_max_size / chunk)))
        audio_source = AudioSource(self.queue, True, True)
    
        self.watson_ws_speech_to_text = self.__init_watson(audio_source)
    
        pyaudio_audio  = pyaudio.PyAudio()
        pyaudio_stream = pyaudio_audio.open(
          format=pyaudio.paInt16,
          channels=1,
          rate=16000,
          input=True,
          frames_per_buffer=chunk,
          stream_callback=self.pyaudio_to_ibm_audio,
          start=False
        )
        pyaudio_stream.start_stream()
        stateful_callback = IBMRecognitionCallback()
        try:
          self.__recognize_audio_callback(audio_source, stateful_callback)
          print("ALL GOOD HERE")
        except:
          print("CAUGHT")
          # pyaudio_stream.stop_stream()
          print("Stream stopped")
          pyaudio_stream.close()
          print("Stream closed")
          pyaudio_audio.terminate()
          print("Audio terminated")
          audio_source.completed_recording()
        translated = stateful_callback.final_hypothesis
        print(f"WATSON THINKS YOU SAID {translated}")
        return translated
        # self.__text_to_speech(f"I think you said {translated}")
        # if ("news" in translated):
        #     article = self.fetch_news()
        #     self.__text_to_speech(article)
