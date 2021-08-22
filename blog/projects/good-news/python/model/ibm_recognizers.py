from ibm_watson.websocket import RecognizeCallback

class IBMRecognitionCallback(RecognizeCallback):
  def __init__(self):
    RecognizeCallback.__init__(self)
  
  def on_transcription(self, transcript):
    print(transcript)

  def on_connected(self):
    print("Connected")
  
  def on_close(self):
    print("Closed")

  def on_error(self, error):
    print(str(error))

  def on_inactivity_timeout(self, error):
    print(str(error))

  def on_listening(self):
    print("Listening")

  def on_hypothesis(self, hypothesis):
    print(hypothesis)
  
  def on_data(self, data):
    print(data)