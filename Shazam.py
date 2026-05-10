from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile as wavfile
import warnings
import os

def chooseWav():
    #Local folder that the script is in
    folder = os.path.dirname(os.path.abspath(__file__))

    # present all .wav files in the local folder
    wav_files = [
        f for f in os.listdir(folder) #equivalent of running l in BASH
        if f.lower().endswith(".wav") #f.lower() for consistency sake
    ]

    print("Start by selecting the file you want to analyze")
    print("Before you is a selection of files from the local folder")
    print(wav_files)
    print("Note that for selecting files outside this list you have to input the full file path")
    print("Name is case sensitive, do NOT add quotes on the name it automatically converts into a string")
    return input("Please input the file name: ")

def loadWav(wavPath):
    with warnings.catch_warnings(action="ignore"):  # ignore that stupid warning
        sampleRate, data = wavfile.read(wavPath)
    return data, sampleRate

def timeInput(message):
    print("This is time related input you can optionally specify time in seconds or minutes or both")
    inpSec = int(input(message + "in seconds: "))
    print("input 0 if you don't want to specify in minutes")
    inpMin = int(input(message + "in minutes: "))
    #Originally intended to also take input in hours but by that point the code would die trying to analyze a >1 hour file
    return int(inpSec + 60*inpMin)

def getAppropriateHorizontalAxis(dataRange, dataSteps):
    return np.linspace(0, dataRange, dataSteps)

def plotGraph(dataRange, dataSteps, signal, label, frequencyMode):

    if frequencyMode:
        dataRange = np.int64(20000) #20000 cause it's highest frequency heard by human ear
        dataSteps = np.int64(sampleRate*2+1)

    plt.plot(getAppropriateHorizontalAxis(dataRange, dataSteps), signal)
    plt.title(label)
    plt.grid(True)

    if frequencyMode:
        plt.xlabel("Frequency / Hz")
        plt.ylabel("Amplitude")
    else:
        plt.xlabel("Time / Sec")
        plt.ylabel("Amplitude")

def defineSubplot(subplot, dataRange, dataSteps, signal, label, color):
        subplot.plot(getAppropriateHorizontalAxis(dataRange, dataSteps), signal, color)
        subplot.set_title(label)
        subplot.set_xlabel("Time / Sec")
        subplot.set_ylabel("Amplitude")
        subplot.grid(True)

def getDurationSec(data):
    return len(data) / sampleRate

def convertToMono(data):
    if (data.ndim == 1):
        return data
    monoData = data.mean(axis=1)
    return monoData

def extractClip(data, clipStart, clipDur):
    clipStartSample = np.int64(sampleRate * clipStart)

    clipDurSample = np.int64(sampleRate * clipDur)

    clipEndSample = clipStartSample + clipDurSample

    return data[clipStartSample:clipEndSample], clipDurSample
    # spaced out lines so it doesn't look like an eyesore

def fourierTransform(signal):
    return np.abs(np.fft.rfft(signal))
    #fft : complex -> fft of  those complex numbers
    #rfft: takes only real numbers to save memory. audio only consists of real numbers anyways

def windowAlgorithm(data, windowStep):
    #Init variables
    bestSimScore = 0
    simScorePlot = []
    bestMatch = []
    bestMatchTimestamp = 0
    windowLengthSec = clipDurationSec
    windowStart = 0
    windowEnd = windowLengthSec
    flag = True

    while(flag):

        # Extract a clip (the window itself)
        windowData, windowLengthSamples = extractClip(data, windowStart, windowLengthSec)
        windowFFT = fourierTransform(windowData)
        if freqData.shape[0] == windowFFT.shape[0]:
            simScore = np.dot(freqData, windowFFT) / (np.linalg.norm(freqData) * np.linalg.norm(windowFFT))
            simScorePlot.append(simScore)

            #Update the best similarity score
            if simScore > bestSimScore:
                bestSimScore = simScore
                bestMatch = windowData
                bestMatchTimestamp = windowStart

            #Increment window by step
            windowStart = windowStart + windowStep
            windowEnd = min(fullDuration, windowEnd + windowStep)

        else:
            flag = False
    
    return bestMatch,bestMatchTimestamp,bestSimScore,simScorePlot

# ______LOADING______
wavPath = chooseWav()

data, sampleRate = loadWav(wavPath)
fullDuration = getDurationSec(data)

print("Clip duration = ", int(fullDuration), "s")
print("sample rate = ", sampleRate, "Hz")

# ______MONO CONVERSION______
mono = convertToMono(data)

plotGraph(fullDuration, mono.shape[0], mono, "Original Signal", False)
plt.show()

# ______CLIPPING______
clipTimestampSec = timeInput("Please input the clip timestamp ")
print("clip time stamp starting from ", clipTimestampSec, " second(s) chosen")

clipDurationSec = timeInput("Please input the clip duration ")
print("clip duration of ",clipDurationSec," second(s) chosen")

clip, clipLengthSamples = extractClip(mono, clipTimestampSec, clipDurationSec)

# ______FAST FOURIER TRANSFORM______

freqData = fourierTransform(clip)

# ______SLIDING WINDOW ALGORITHM______

bestMatch,bestMatchTimestamp,bestSimScore,simScorePlot = windowAlgorithm(mono, 3)

#______PLOT SIMILARITY VS TIME______
plotGraph(round(fullDuration),len(simScorePlot),simScorePlot,"Similarity Score vs time",False)

plt.axvline(bestMatchTimestamp,color="green", label = "Best match timestamp")
plt.axvline(clipTimestampSec,color="red", label = "Clip timestamp")

plt.legend()
plt.show()

#______DIRECT COMPARISON______
bestMatchDurationSamples = len(bestMatch)
bestMatchDuration = bestMatchDurationSamples/sampleRate

fig, ax = plt.subplots(2, 1, figsize=(10, 6))

defineSubplot(ax[0],clipDurationSec, clipLengthSamples, clip, "Clipped Signal", "purple")
defineSubplot(ax[1],bestMatchDuration, bestMatchDurationSamples, bestMatch, "Best Match Signal", "red")

fig.subplots_adjust(hspace=0.5)
plt.show()