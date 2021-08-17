import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt

ipd.Audio('/Users/alex/Desktop/engineeringwithalex.m4a')

filename1 = '/Users/alex/Desktop/engineeringwithalex.m4a'
plt.figure(figsize=(15,4))
data1,sample_rate1 = librosa.load(filename1, sr=22050, mono=True, offset=0.0, duration=50, res_type='kaiser_best')
librosa.display.waveplot(data1,sr=sample_rate1, max_points=50000.0, x_axis='time', offset=0.0, max_sr=1000)
