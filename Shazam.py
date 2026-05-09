from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile as wavfile
from scipy.fftpack import fft
import warnings

def loadWav(wavPath):
    with warnings.catch_warnings(action="ignore"): #ignore that stupid warning
        sampleRate, data = wavfile.read(wavPath)
    return data, sampleRate

def printAllMetaData(): #Only used when testing
    print("Sample Rate: ", sampleRate)
    print("Duration: ", duration)
    print("Is Mono? ->", isMono)
    print("data: ", data)

def printAllPlotRelatedVariables(): #Also only used when testing
    print("Time Axis: ", timeAxis) #Does not print fully in some IDE's
    print("Mono: ", mono)

def printAllClipRelatedVariables():
    print("Clip Time Axis: ",clipTimeAxis)
    print("Clip: ",clip)

def printAllFrequncyDomainRelatedVariables():
    print("Raw Frequency data", freqDataRaw)
    print("Frequency data: ", freqData)
    print("Frequency range", frequencyRange)

def checkIsMono(data):
        x,y = data.shape
        return y == 1

def getDurationSec(data, sampleRate):
    return round(len(data)/sampleRate,0)

def convertToMono(data):
        if(checkIsMono(data)):
            return data
        monoData = data.mean(axis=1)
        return monoData

def extractClip(data, sampleRate, clipTimestampSec, clipDurationSec):

    clipTimestampSample = sampleRate * clipTimestampSec

    clipDurationSample = sampleRate * clipDurationSec

    clipEndSample = clipTimestampSample + clipDurationSample

    return data[clipTimestampSample:clipEndSample]
    #spaced out lines so it doesn't look like an eyesore

#______LOADING______
wavPath = 'goofyAhh.wav'
#TODO take input for this field instead
data, sampleRate = loadWav(wavPath)

#______METADATA______
duration = getDurationSec(data, sampleRate)
isMono = checkIsMono(data)

printAllMetaData()
#TODO remove this line when done testing

#______MONO CONVERSION______
mono = convertToMono(data)
monoDataLength = mono.shape[0]

timeAxis = np.linspace(0,monoDataLength,monoDataLength) #Horizontal axis

printAllPlotRelatedVariables()
#TODO remove this line when done testing

plt.plot(timeAxis,mono)
plt.show()

#______CLIPPING______

clipTimestampSec = 5
clipDurationSec = 4
#TODO replace the values with input functions when testing concludes

clip = extractClip(mono, sampleRate, clipTimestampSec, clipDurationSec)
clipLength = clip.shape[0]

clipTimeAxis = np.linspace(0,clipLength,clipLength)

plt.plot(clipTimeAxis,clip)
plt.show()

printAllClipRelatedVariables()
#TODO remove this line when done testing

#______FAST FOURIER TRANSFORM______
freqDataRaw = fft(clip)
freqData = 2/clipLength * np.abs(freqDataRaw[0:np.int64(clipLength/2)])

#______FREQUENCY DOMAIN & VISUALISATION______
frequencyRange = np.int64(clipLength/2)
frequency = np.linspace(0,frequencyRange,frequencyRange)
plt.plot(frequency,freqData)
plt.show()

printAllFrequncyDomainRelatedVariables()
#TODO remove this line when done testing








