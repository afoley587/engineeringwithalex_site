from ibm_watson.websocket import RecognizeCallback

class IBMRecognitionCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.final_hypothesis = ""

    def on_transcription(self, transcript):
        print("TRANSCRIPT:", transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(f"ON HYPOTHESIS {hypothesis}")
        self.final_hypothesis = hypothesis

    def on_data(self, data):
        print(f"ON DATA {data}")

    def on_close(self):
        print("Connection closed")