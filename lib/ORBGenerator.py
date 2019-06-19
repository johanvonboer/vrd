from lib import VRDUtil
from lib import VRDConfig
import os, cv2, math
import numpy as np

class ORBGenerator():

	def __init__(self, config):
		self.config = config
		self.VRDUtil = VRDUtil.VRDUtil(config)

	def computeORB(self, frame):
		#frame = cv2.imread('frames/frame170.jpg',0)

		# Initiate STAR detector
		orb = cv2.ORB_create()

		#Why is this being convertd to 8-bit unsigned here?
		frame = frame.astype(np.uint8)

		# find the keypoints with ORB
		kp = orb.detect(frame, None)

		# compute the descriptors with ORB
		keyPoints, des = orb.compute(frame, kp)

		#outImage = np.zeros_like(frame)
		#print(keyPoints)
		#for keyPoint in keyPoints:
		#    print(keyPoint.pt[0], keyPoint.pt[1], keyPoint.size)

		# draw only keypoints location,not size and orientation
		#keyPointFrame = cv2.drawKeypoints(frame,keyPoints,outImage,color=(0,255,0), flags=0)

		return keyPoints

	def computeORBs(self, frames):
		keyPointsCollection = []
		for frame in frames:
			keyPoints = self.computeORB(frame)
			keyPointsCollection.append(keyPoints)

		return keyPointsCollection

	def run(self, videoFilePath):
		path, fileName = os.path.split(videoFilePath)
		frames = self.VRDUtil.readFramesFromDrive("assets/processed/"+fileName+"/Kv")
		keyPointsCollection = self.computeORBs(frames)
		#print(keyPointsCollection)
		
		for kpFrame in keyPointsCollection:
			print("KPFRAME")
			for kp in kpFrame:
				print(kp)
				print(str(kp.angle))
				print(str(kp.class_id))
				print(str(kp.octave))
				print(str(kp.pt))
				print(str(kp.pt[0]))
				print(str(kp.pt[1]))
				print(str(kp.response))
				print(str(kp.size))

		self.VRDUtil.storeKeyPointsOnDrive(keyPointsCollection, "assets/fingerprints/"+fileName+"/ORB")