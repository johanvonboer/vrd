from lib import VRDConfig, VRDUtil, ThGenerator, ThMatcher, CCGenerator, ORBGenerator, CCMatcher, ORBMatcher

class MultiLevelMatcher():
	def __init__(self, config):
		self.config = config
		self.VRDUtil = VRDUtil.VRDUtil(config)


	def run(self, videoFilePath):
		ThGenerator.ThGenerator(self.config).run(videoFilePath)
		CCGenerator.CCGenerator(self.config).run(videoFilePath)
		ORBGenerator.ORBGenerator(self.config).run(videoFilePath)
		#SSMGenerator.SSMGenerator(self.config).rung(videoFilePath)

		#Runs a match aginst all Th-fingerprints in our library, returns the ones over a certain threshold
		ThMatcher.ThMatcher(self.config).run(videoFilePath)
		CCMatcher.CCMatcher(self.config).run(videoFilePath)
		ORBMatcher.ORBMatcher(self.config).run(videoFilePath)
