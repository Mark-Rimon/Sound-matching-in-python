from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile as wavfile
from scipy.fftpack import fft
import warnings


def loadWav(wavPath):
    with warnings.catch_warnings(action="ignore"):  # ignore that stupid warning
        sampleRate, data = wavfile.read(wavPath)
    return data, sampleRate


def printAllMetaData():  # Only used when testing
    print("Sample Rate: ", sampleRate, "Hz")
    print("Duration: ", fullDuration, "s")
    print("Is Mono? ->", isMono)
    print("data: ", data)


def printAllPlotRelatedVariables():  # Also only used when testing
    print("Mono: ", mono)


def printAllClipRelatedVariables():
    print("Clip: ", clip)
    print("Clip Timestamp: ", clipTimestampSec, "s")
    print("CLip Duration: ", clipDurationSec, "s")


def printAllFrequncyDomainRelatedVariables():
    print("Raw Frequency data", freqDataRaw)
    print("Frequency data: ", freqData)
    print("Frequency range", frequencyRange)


def getAppropriateHorizontalAxis(dataRange, dataSteps):
    return np.linspace(0, dataRange, dataSteps)


def plotTimeDomain(t, y, label):
    plt.plot(t, y)
    plt.title(label)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()


def plotFrequencyDomain(t, y, label):
    plt.plot(t, y)
    plt.title(label)
    plt.xlabel("Frequency / Hz")
    plt.ylabel("Amplitude")
    plt.show()


def checkIsMono(data):
    x, y = data.shape
    return y == 1


def getDurationSec(data, sampleRate):
    return len(data) / sampleRate, 0
    # no need to round as doing so will stretch x-axis unnecessarily


def convertToMono(data):
    if (checkIsMono(data)):
        print("wasmono")
        return data
    print("wasnotmono")
    monoData = data.mean(axis=1)
    return monoData


def extractClip(data, sampleRate, clipTimestampSec, clipDurationSec):
    clipTimestampSample = np.int64(sampleRate * clipTimestampSec)

    clipDurationSample = np.int64(sampleRate * clipDurationSec)

    clipEndSample = clipTimestampSample + clipDurationSample

    return data[clipTimestampSample:clipEndSample], clipDurationSample
    # spaced out lines so it doesn't look like an eyesore


def slidingWindow(data, sampleRate, clipTimeStampSec, clipDurationSec, windowSteps):
    signalDuration = len(data)
    windowLengthSec = clipDurationSec
    clip, clipLength = extractClip(data, sampleRate, clipTimeStampSec, clipDurationSec)
    clipFFT = fft(clip)
    clipData = 2 / clipLength * np.abs(freqDataRaw[0:np.int64(clipLength / 2)])

    for i in range(signalDuration / windowSteps):
        window, windowLength = extractClip(data, sampleRate, i * windowSteps, clipDurationSec)
        windowFFT = fft(window)
        windowData = windowData = 2 / windowLength * np.abs(freqDataRaw[0:np.int64(windowLength / 2)])

    return


# ______LOADING______
wavPath = 'goofyAhh.wav'
# TODO take input for this field instead

data, sampleRate = loadWav(wavPath)
# FAHHHHHHHHHHHHHHH 🔥🔥🔥

# ______METADATA______
fullDuration = getDurationSec(data, sampleRate)
isMono = checkIsMono(data)

printAllMetaData()
# TODO remove this line when done testing

# ______MONO CONVERSION______
mono = convertToMono(data)
monoDataLength = mono.shape[0]

printAllPlotRelatedVariables()
# TODO remove this line when done testing

plotTimeDomain(getAppropriateHorizontalAxis(fullDuration, monoDataLength), mono, "Original Signal")

# ______CLIPPING______

clipTimestampSec = 5
clipDurationSec = 4
# TODO replace the values with input functions when testing concludes

clip, clipLength = extractClip(mono, sampleRate, clipTimestampSec, clipDurationSec)
plotTimeDomain(getAppropriateHorizontalAxis(clipDurationSec, clipLength), clip, "Clipped Signal")

printAllClipRelatedVariables()
# TODO remove this line when done testing

# ______FAST FOURIER TRANSFORM______

def fourierTransform(signal, signalDuration):
    fourierSignal = fft(signal)
    returnFFTSignal = 2/signalDuration * np.abs(fourierSignal[0:np.int64(signalDuration/2)])
    return returnFFTSignal

freqDataRaw = fft(clip)
freqData = 2 / clipLength * np.abs(freqDataRaw[0:np.int64(clipLength / 2)])

# ______FREQUENCY DOMAIN & VISUALISATION______
frequencyRange = np.int64(clipLength / 2)
frequency = np.linspace(0, sampleRate / 2, frequencyRange)

plotFrequencyDomain(getAppropriateHorizontalAxis(sampleRate / 2, frequencyRange), freqData, "Frequency Domain Signal")
printAllFrequncyDomainRelatedVariables()
# TODO remove this line when done testing

# ______SLIDING WINDOW ALGORITHM______

def windowAlgorithm(data, sampleRate, windowStep):
    #Init variables
    windowLengthSec = clipDurationSec
    windowStart = 0
    windowEnd = windowLengthSec
    while(windowLengthSec < fullDuration):

        # Extract a clip (the window itself)
        windowDuration = windowEnd - windowStart
        extractClip(data, sampleRate, windowStart, windowDuration)
        #TODO add fft step here

        #Increment window by step
        windowStart = windowStart + windowStep
        windowEnd = min(fullDuration, windowEnd + windowStep)

