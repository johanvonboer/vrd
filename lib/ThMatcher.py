from lib import VRDConfig, VRDUtil
import numpy as np
import os

class ThMatcher():

    def __init__(self):
        self.config = VRDConfig.VRDConfig()
        self.VRDUtil = VRDUtil.VRDUtil()

    def getMeanPixelValue(self, frame):
        mp = np.zeros(frame[0].shape, dtype=np.uint64)
        for p in frame:
            mp += p
        mp = mp / len(frame)

        return mp


    def thFingerprint(self, qFrame, rFrame):

        qmpv = self.getMeanPixelValue(qFrame)
        rmpv = self.getMeanPixelValue(rFrame)
        
        #Get a frame in which each pixel is normalized against the mean
        resultFrame = np.zeros(qFrame.shape, dtype=np.int64)
        qFrame = qFrame.astype(np.int64)
        for i in range(len(qFrame)):
            qAvgPixel = qFrame[i] - qmpv
            rAvgPixel = rFrame[i] - rmpv
            computedPixel = qAvgPixel * rAvgPixel
            resultFrame[i] = computedPixel
    
        result = np.sum(resultFrame)
        return result
    
        
    def thMatchFrames(self, qFrame, rFrame):
        return self.thFingerprint(qFrame, rFrame) / np.sqrt(self.thFingerprint(qFrame, qFrame) * self.thFingerprint(rFrame, rFrame))

    def thMatchVideos(self, qVideo, rVideo):
        significantMatches = []
        
        queryFrameIndex = 0
        refFrameIndex = 0

        for qFrame in qVideo:
            queryFrameIndex += 1
            for rFrame in rVideo:
                refFrameIndex += 1
                matchRate = self.thMatchFrames(qFrame, rFrame)
                if matchRate > self.config.TH_MATCH_THRESHOLD:
                    significantMatches.append({
                            "qFrameIndex": queryFrameIndex,
                            "rFrameIndex": refFrameIndex,
                            "matchRate": matchRate,
                            "qFrameTimeOffset": self.getFrameTimeIndex(queryFrameIndex),
                            "rFrameTimeOffset": self.getFrameTimeIndex(refFrameIndex)
                        })

        return significantMatches

    def getFrameTimeIndex(self, frameIndex):
        offsetSeconds = round((1 / self.config.DOWNSAMPLE_TO_FPS) * frameIndex)

        return offsetSeconds


    def run(self, queryFrames):

        vu = VRDUtil.VRDUtil()
        videos = vu.getReferenceVideosList()
        processedVideos = 0

        for video in videos:
            rvPath, rvFilename = os.path.split(video)
            rVideo = vu.readFramesFromDrive("assets/fingerprints/"+rvFilename+"/Th")
            significantFrameMatches = self.thMatchVideos(queryFrames, rVideo)
            if len(significantFrameMatches) > 0:
                out = {
                    "qVideo": queryVideo,
                    "rVideo": video,
                    "matches": significantFrameMatches
                }
                jsonMatches = json.dumps(out)
                print("output:"+jsonMatches+"\n")

            processedVideos += 1
            print("Processed videos:"+str(processedVideos))