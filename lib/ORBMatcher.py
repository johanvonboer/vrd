from lib import VRDUtil
import os, json


class ORBMatcher():
	def __init__(self, config):
		self.config = config
		self.VRDUtil = VRDUtil.VRDUtil(config)

	def orbMatchVideos(self, qVideo, rVideo):
		print(qVideo)
		print(rVideo)
		pass

	def run(self, videoFilePath):
		path, fileName = os.path.split(videoFilePath)
		queryFrames = self.VRDUtil.readKeyPointsFromDrive("assets/fingerprints/"+fileName+"/ORB")

		videos = self.VRDUtil.getReferenceVideosList()
		processedVideos = 0

		for video in videos:
			rvPath, rvFilename = os.path.split(video)
			rVideo = self.VRDUtil.readKeyPointsFromDrive("assets/fingerprints/"+rvFilename+"/ORB")
			significantFrameMatches = self.orbMatchVideos(queryFrames, rVideo)
			if len(significantFrameMatches) > 0:
				out = {
					"qVideo": fileName,
					"rVideo": video,
					"matches": significantFrameMatches
				}
				jsonMatches = json.dumps(out)
				print("output:"+jsonMatches+"\n")

			processedVideos += 1
			print("Processed videos:"+str(processedVideos))