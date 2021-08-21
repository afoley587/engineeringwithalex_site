import speech_recognition as sr
import pyttsx3
from model.newsApi import NewsApiImpl

# from Queue import Queue, Full
# from ibm_watson import SpeechToTextV1
# from ibm_watson.websocket import RecognizeCallback, AudioSource
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from model.ibm_recognizers import IBMRecognitionCallback

class Jarvis:
    def __init__(
      self, news_api_key, 
      ibm_username="", ibm_password="", 
      ibm_api_key="", ibm_api_url="https://api.us-east.speech-to-text.watson.cloud.ibm.com"
    ):
        self.recognizer    = sr.Recognizer()
        self.news_fetcher  = NewsApiImpl(news_api_key)
        self.ibm_username  = ibm_username
        self.ibm_password  = ibm_password
        self.ibm_api_key   = ibm_api_key
        self.ibm_api_url   = ibm_api_url

        self.speech_engine = self.__init_engine(
            voice="com.apple.speech.synthesis.voice.daniel"
        )
        # self.watson_ws_speech_to_text = self.__init_watson()
    
    def __init_engine(
            self, 
            voice="com.apple.speech.synthesis.voice.samantha",
            rate=150
        ):
        engine = pyttsx3.init() 
        engine.setProperty('rate', rate)
        engine.setProperty('voice', voice)
        return engine

    # def __init_watson(self, audio_source, callback):
    #     authenticator = IAMAuthenticator(self.ibm_api_key)
    #     spech_to_text = SpeechToTextV1(authenticator=authenticator)
    #     spech_to_text.set_service_url(self.ibm_api_url)
    #     return spech_to_text

    def __recognize_audio(self, audio, recognizer='google'):
      try:
        if (recognizer == 'sr_google'):
          return self.recognizer.recognize_google(audio)
        elif (recognizer == 'sr_ibm'):
          return self.recognizer.recognize_ibm(
            audio, 
            username=self.ibm_username, 
            password=self.self.ibm_password
          )
        elif (recognizer == 'ws_ibm'):
          print("To implement")
      except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
      except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return None


    def fetch_news(self, kind="good"):
        if (kind == "good"):
            return self.news_fetcher.get_happy_news()
        return self.news_fetcher.get_random_article()


    def act(self):
        translated = None
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... one second please!")
            self.recognizer.adjust_for_ambient_noise(source)
            print("I am waiting for your next order")
            audio = self.recognizer.listen(source)
            translated = self.__recognize_audio(audio, recognizer='google')
        if (translated):
            self.speech_engine.say(f"I think you said {translated}")
            self.speech_engine.runAndWait()
            if ("news" in translated):
                article = self.fetch_news()
                self.speech_engine.say(article)
                self.speech_engine.runAndWait()
    
    # def __recognize_audio_callback(self, audio_source, callback):
    #    self.watson_ws_speech_to_text.recognize_using_websocket(
    #       audio=audio_source,
    #       content_type='audio/115; rate=44100',
    #       recognize_callback=callback,
    #       interim_results=True
    #     )
    # 
    # def pyaudio_to_ibm_audio(self, data_in, frame_count, time_info, status):
    #       try:
    #         self.queue.put(data_in)
    #       except Full:
    #         pass
    #       return (None, pyaudio.paContinue)
    #
    # def act_ibm_websockets(self):
    #     chunk        = 1024
    #     buf_max_size = chunk * 10
    #     self.queue   = Queue(maxsize=int(round(buf_max_size / chunk)))
    #     audio_source = AudioSource(q, True, True)
    # 
    #     self.watson_ws_speech_to_text = self.__init_watson(audio_source)
    # 
    #     pyaudio_audio  = pyaudio.PyAudio()
    #     pyaudio_stream = pyaudio_audio.open(
    #       format=pyaudio.paInt16,
    #       channels=1,
    #       rate=44100,
    #       input=True,
    #       frames_per_buffer=chunk,
    #       stream_callback=self.pyaudio_to_ibm_audio,
    #       start=False
    #     )
    #     pyaudio_stream.start_session()
    #     try:
    #       recognize_thread = Thread(
    #         target=self.__recognize_audio_callback, 
    #         args=(audio_source, IBMRecognitionCallback)
    #       )
    #     except KeyboardInterrupt:
    #       pyaudio_stream.stop_stream()
    #       pyaudio_stream.close()
    #       pyaudio_audio.terminate()
    #       audio_source.completed_recording()