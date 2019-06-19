
class FrameProcessor():
	def __init__(self, config):
		self.config = config
        self.VRDUtil = VRDUtil.VRDUtil(config)

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
        self.vrdutil.storeFramesOnDrive(ccFrames, "assets/fingerprints/"+fileName+"/Folded")
        #storeFramesOnDrive(frames, "../assets/processed/ThinkNanoThinkAmes_aav1949.MP4/Folded")
        frames = self.scaleFrames(frames, 32, 32)
        #storeFramesOnDrive(frames, "../assets/processed/ThinkNanoThinkAmes_aav1949.MP4/Thumbs-color")
        frames = self.convertToGray(frames)
        self.vrdutil.storeFramesOnDrive(frames, "assets/fingerprints/"+fileName+"/Th")

        return frames