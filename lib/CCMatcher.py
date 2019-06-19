from lib import VRDUtil
import os, json


class CCMatcher():
	def __init__(self, config):
		self.config = config
		self.VRDUtil = VRDUtil.VRDUtil(config)


	def ccMatchFrames(self, qFrame, rFrame):
		distance = 0
		L = len(qFrame)
		for i in range(L):
			if qFrame[i] != rFrame[i]:
				distance += 1
		return distance

	def ccMatchVideos(self, qVideo, rVideo):
		significantMatches = []

		queryFrameIndex = 0
		refFrameIndex = 0

		for qFrame in qVideo:
			queryFrameIndex += 1
			for rFrame in rVideo:
				refFrameIndex += 1

				matchDistance = self.ccMatchFrames(qFrame, rFrame)

				if matchDistance <= self.config.CC_MATCH_THRESHOLD:
					significantMatches.append({
						"qFrameIndex": queryFrameIndex,
						"rFrameIndex": refFrameIndex,
						"matchDistance": matchDistance,
						"qFrameTimeOffset": self.VRDUtil.getFrameTimeIndex(queryFrameIndex),
						"rFrameTimeOffset": self.VRDUtil.getFrameTimeIndex(refFrameIndex)
					})

		return significantMatches


	def run(self, videoFilePath):
		path, fileName = os.path.split(videoFilePath)
		queryFrames = self.VRDUtil.readColorCorrelationFromDrive("assets/fingerprints/"+fileName+"/CC")

		videos = self.VRDUtil.getReferenceVideosList()
		processedVideos = 0

		for video in videos:
			rvPath, rvFilename = os.path.split(video)
			rVideo = self.VRDUtil.readColorCorrelationFromDrive("assets/fingerprints/"+rvFilename+"/CC")
			significantFrameMatches = self.ccMatchVideos(queryFrames, rVideo)
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