from lib import VRDUtil
from lib import VRDConfig
import os, cv2, math
import numpy as np

class CCGenerator():

	def __init__(self, config):
		self.config = config
		self.vrdutil = VRDUtil.VRDUtil(config)


	def calculateColorCorrelations(self, frames):
		ccs = []
		for frame in frames:
			ccs.append(self.calculateColorCorrelation(frame))
		return ccs

	def calculateColorCorrelation(self, frame):
		#Reduce frame to 16x16 pixles. These are the "blocks" we are using and this is how we compute them.
		thumb = cv2.resize(frame, (16, 16))

		cc = {
			"rgb": 0,
			"rbg": 0,
			"grb": 0,
			"gbr": 0,
			"brg": 0,
			"bgr": 0
		}

		for row in thumb:
			for pixel in row:
				blue = pixel[0]
				green = pixel[1]
				red = pixel[2]

				if red == green == blue:
					pass
				elif red >= green >= blue:
					cc["rgb"] += 1
				elif red >= blue >= green:
					cc["rbg"] += 1
				elif green >= red >= blue:
					cc["grb"] += 1
				elif green >= blue >= red:
					cc["gbr"] += 1
				elif blue >= red >= green:
					cc["brg"] += 1
				elif blue >= green >= red:
					cc["bgr"] += 1


		ccSum = 0
		for key, value in cc.items():
			ccSum += value

		ccbin = ""
		normalizedCC = {}
		for key, value in cc.items():
			if value > 0:
				normalizedCC[key] = value / ccSum
				ccbin += format(round((value / ccSum) * 100), '07b')
			else:
				normalizedCC[key] = 0
				ccbin += format(0, '07b')

		ccbin = ccbin[7:]


		return { "cc": normalizedCC, "frame": thumb, "bin": ccbin }


	def run(self, videoFilePath):
		path, fileName = os.path.split(videoFilePath)

		frames = self.vrdutil.readFramesFromDrive("assets/processed/"+fileName+"/Folded")
		if frames == False:
			return False

		ccs = self.calculateColorCorrelations(frames)
		
		#for cc in ccs:
		#	print(cc["bin"])

		self.vrdutil.storeColorCorrelationOnDrive(ccs, "assets/fingerprints/"+fileName+"/CC")

		return ccs