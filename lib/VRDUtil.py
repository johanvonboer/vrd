from lib import VRDConfig
import os
from os import listdir
from os.path import isfile, join
import sys
import numpy as np
import cv2
import math
import time
import pickle
from matplotlib import pyplot as plt
import shutil


class VRDUtil:
    def __init__(self):
        self.config = VRDConfig.VRDConfig()

    def getInputFile(self, file):
        if file != "":
            return file

        if len(sys.argv) < 2:
            #inputFile = "../assets/bbb.avi"
            print("No input file supplied")
            sys.exit()
        else:
            inputFile = sys.argv[1]

        path, fileExtension = os.path.splitext(inputFile)
        fileExtension = fileExtension.lower()

        if fileExtension == ".avi" or fileExtension == ".mpeg" or fileExtension == ".mp4" or fileExtension == ".mpg" or fileExtension == ".mov":
            fileType = "video"
        else:
            fileType = "image"

        if fileType == "video":
            cap = cv2.VideoCapture(inputFile)
            archiveFiles = os.listdir("../assets/video")
        else:
            archiveFiles = os.listdir("../assets/image")

        
        return inputFilea


    def getHammingDistance(self, a, b):
        hits = 0
        #for key, value in a:
        #    if a[key] == b[key]:
        #        hits = hits + 1

        for key in range(len(a)):
            if a[key] == b[key]:
                hits = hits + 1

        return hits


    def storeFramesOnDrive(self, frames, path = "frames"):

        if os.path.isdir(path) == False:
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)

        print("Writing frames to drive ("+str(len(frames))+")")
        zeroPadding = len(str(len(frames)))
        i = 0
        for frame in frames:
            i = i + 1
            cv2.imwrite(path+"/frame"+str(i).rjust(zeroPadding, "0")+".jpg", frame)
            
            
    def readFramesFromDrive(self, path = "frames"):
        print("Reading frames ("+path+")")
        frames = []
        frameFiles = os.listdir(path)
        frameFiles.sort()
        for f in frameFiles:
            frame = cv2.imread(path+"/"+f)
            frames.append(frame)
        return frames


    def matplotFrames(self, frames):
        rgbFrames = []
        for frame in frames:
            rgbFrame = frame[...,::-1]
            #rgbFrame = frame
            rgbFrames.append(rgbFrame)

        fig=plt.figure(figsize=(8, 8))
        columns = 4
        rows = 4
        for i in range(1, columns*rows +1):
            fig.add_subplot(rows, columns, i)
            plt.imshow(rgbFrames[i])
        plt.show()
        
        
    def plotCompareFrames(self, fa, fb):
        fig=plt.figure(figsize=(8, 8))
        fig.add_subplot(1, 2, 1)
        plt.imshow(fa)
        fig.add_subplot(1, 2, 2)
        plt.imshow(fb)
        plt.show()
        
    def storeKeyPointsOnDrive(self, keyPointsCollection, path = "./assets/processed"):
        if os.path.isdir(path) == False:
            os.makedirs(path)

        print("Writing ORB key points to drive ("+str(len(keyPointsCollection))+")")
        zeroPadding = len(str(len(keyPointsCollection)))
        i = 0
        for fkp in keyPointsCollection:
            i = i + 1
            kpList = []
            for keyPoint in fkp["kp"]:
                
                #print(kpItem)
                #keyPoint = kp["kp"]
                kpList.append([keyPoint.pt[0], keyPoint.pt[1], keyPoint.size])
                
                #This is for writing JSON, which is more readable, but also much slower...
                #kpList.append({
                #        "x": keyPoint.pt[0],
                #        "y": keyPoint.pt[1],
                #        "s": keyPoint.size
                #    })
            
            with open(path+"/frame"+str(i).rjust(zeroPadding, "0")+".json", "wb") as fp:
                pickle.dump(kpList, fp)
                #json.dump(kpList, fp)
                
                
    def storeColorCorrelationOnDrive(self, ccs, path):
        if os.path.isdir(path) == False:
            os.makedirs(path)

        print("Writing color correlation to drive")

        zeroPadding = len(str(len(ccs)))
        i = 0
        for cc in ccs:
            i = i + 1
            with open(path+"/frame"+str(i).rjust(zeroPadding, "0")+"-cc.txt", "w") as fp:
                fp.write(cc["bin"])
                
    def readColorCorrelationFromDrive(self, path):
        print("Reading CCs ("+path+")")
        frames = []
        frameFiles = os.listdir(path)
        frameFiles.sort()
        for f in frameFiles:
            with open(path+"/"+f, "r") as fp:
                cc = fp.read()
            frames.append(cc)
        return frames


    def getReferenceVideosList(self):
        fingerprintsPath = "assets/fingerprints"
        files = [f for f in listdir(fingerprintsPath) if os.path.isdir(join(fingerprintsPath, f))]
        return files