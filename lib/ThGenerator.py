from lib import VRDUtil
from lib import VRDConfig
import os, cv2, math
import numpy as np

class ThGenerator():

    def __init__(self, config):
        self.config = config
        self.vrdutil = VRDUtil.VRDUtil(config)

    def captureFrames(self, videoFilePath):
        inputFile = self.vrdutil.getInputFile(videoFilePath)
        cap = cv2.VideoCapture(inputFile)
        fps = cap.get(cv2.CAP_PROP_FPS)

        frameStep = round(fps / self.config.DOWNSAMPLE_TO_FPS)
    
        framePosition = 0
        captureCount = 0
        frames = []

        print("Capturing frames")
        while(True):
            # Capture frame-by-frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, framePosition)
            framePosition = framePosition + frameStep
            captureCount = captureCount + 1
            ret, frame = cap.read()

            if ret != True:
                break

            frames.append(frame)

        cap.release()

        if len(frames) < self.config.SEGMENT_LENGTH:
            print("Skipping this video since it's too short")
            return False

        return frames


    #This creates groups (or "segments") of frames with SEGMENT_LENGTH number of frames in each group/segment
    def segmentFrames(self, frames):
        print("Segmenting frames")
        segments = []
        segment = []
        segmentCounter = 0
        for f in frames:
            segmentCounter = segmentCounter + 1
            segment.append(f)
            if segmentCounter == self.config.SEGMENT_LENGTH:
                segments.append(segment)
                segment = []
                segmentCounter = 0

        return segments

    def makeKeyFrames(self, segments):
        print("Making keyframes")
        refShape = segments[0][1].shape
        keyFrames = []
        for segment in segments:
            keyFrame = np.zeros(refShape, dtype=np.uint16)
            for frame in segment:
                if frame is None:
                    print("'None' frame found")
                else:
                    keyFrame += np.floor_divide(frame, self.config.SEGMENT_LENGTH)
                    keyFrame = keyFrame.astype(dtype=np.uint8, casting="unsafe")
            keyFrames.append(keyFrame)
        return keyFrames


    def zoomFrames(self, frames):
        print("Zoom/cropping frames")
        width = frames[0].shape[0]
        height = frames[0].shape[1]
        x = round(width * self.config.ZOOM_FACTOR)
        y = round(height * self.config.ZOOM_FACTOR)
        w = round(width * (1.0 - self.config.ZOOM_FACTOR))
        h = round(height * (1.0 - self.config.ZOOM_FACTOR))
    
        croppedFrames = []
        for frame in frames:
            croppedFrame = frame[y:y+h, x:x+w]
            croppedFrames.append(croppedFrame)
        
        return croppedFrames


    def scaleFrames(self, frames, scale_to_pixels_x = None, scale_to_pixels_y = None):
        print("Scaling frames")

        if scale_to_pixels_x == None:
            scale_to_pixels_x = self.config.SCALE_TO_PIXELS*2
        if scale_to_pixels_y == None:
            scale_to_pixels_y = self.config.SCALE_TO_PIXELS

        thumbs = []
        for f in frames:
            thumb = cv2.resize(f, (scale_to_pixels_x, scale_to_pixels_y))
            thumbs.append(thumb)

        return thumbs

    def foldFrames(self, frames):
        print("Folding frames")
        width = frames[1].shape[0]
        height = frames[1].shape[1]
        halfWidth = math.floor(width / 2)
        halfHeight = math.floor(height / 2)
        foldedFrames = []
        for frame in frames:
        
            leftSide = frame[0:width, 0:halfHeight]
            rightSide = frame[0:width, halfHeight:height]
            rightSide = np.fliplr(rightSide)

            foldedFrame = np.zeros_like(leftSide, dtype=np.uint8)
            foldedFrame = np.floor_divide(leftSide, 2) + np.floor_divide(rightSide, 2)
        
            foldedFrames.append(foldedFrame)

        return foldedFrames

    def convertToGray(self, frames):
        print("Converting to grayscale")
        #FIXME: Does this function follow this specification? :
        #"First, Kv is divided into bGn-blocks, for each block, the
        #pixel values are normalized in accordance to the mean value divided by the
        #standard deviation and then scaled to the 8-bit grayscale from [0 : 1] to
        #[0 : 255]."
    
        grayscaleFrames = []
        for frame in frames:
            frame = frame.astype(np.uint8)
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                grayscaleFrames.append(gray)
            except:
                print(frame)
        
        return grayscaleFrames


    def run(self, videoFilePath):
        path, fileName = os.path.split(videoFilePath)

        frames = self.captureFrames(path+"/"+fileName)
        if frames == False:
            return False
        #storeFramesOnDrive(frames, videoDirectory+"/processed/"+fileName+"/Original")
        segments = self.segmentFrames(frames)
        frames = self.makeKeyFrames(segments)
        self.vrdutil.storeFramesOnDrive(frames, "assets/processed/"+fileName+"/Kv")
        frames = self.zoomFrames(frames)
        #storeFramesOnDrive(frames, "../assets/processed/ThinkNanoThinkAmes_aav1949.MP4/Zoomed")
        frames = self.scaleFrames(frames)
        #storeFramesOnDrive(frames, "../assets/processed/ThinkNanoThinkAmes_aav1949.MP4/Scaled")
        frames = self.foldFrames(frames)
        ccFrames = frames
        self.vrdutil.storeFramesOnDrive(ccFrames, "assets/processed/"+fileName+"/Folded")
        #storeFramesOnDrive(frames, "../assets/processed/ThinkNanoThinkAmes_aav1949.MP4/Folded")
        frames = self.scaleFrames(frames, 32, 32)
        #storeFramesOnDrive(frames, "../assets/processed/ThinkNanoThinkAmes_aav1949.MP4/Thumbs-color")
        frames = self.convertToGray(frames)
        self.vrdutil.storeFramesOnDrive(frames, "assets/fingerprints/"+fileName+"/Th")

        return frames

