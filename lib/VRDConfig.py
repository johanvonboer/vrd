class VRDConfig():
	def __init__(self):
		self.TH_MATCH_THRESHOLD = 0.8 #Matching threshold, which should be -1 to 1, but -1 would be a perfect negative of the image
		self.CC_MATCH_THRESHOLD = 4 #How many digits in the CC hash which may be un-matching 
		self.DOWNSAMPLE_TO_FPS = 0.5 #Number of frames per second to actually work with
		self.SCALE_TO_PIXELS = 100 #Always downsampled to a square, so this is both width and height
		self.SEGMENT_LENGTH = 5 #Segment length in frames. A segment is a part of the frame collection gathered from the downsampled frames
		self.ZOOM_FACTOR = 0.2 #How much to zoom in on the thumbnails and crop away, in percentage expressed as 1.0 = 100%
		self.CC_BLOCKS = 16 #Color correlation blocks to use.
		self.THUMBNAIL_SIZE = 32 #Size of the final scaled, zoomed, folded & grayscaled thumbnail (Th)