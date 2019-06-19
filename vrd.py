from lib import VRDConfig, VRDUtil, ThGenerator, ThMatcher, CCGenerator, ORBGenerator, MultiLevelMatcher
import json, sys, os, argparse

#  python -u vrd.py --input assets/video-reference-library/Zakatinspired.mp4 --working-dir VRD

parser = argparse.ArgumentParser()
parser.add_argument("--command", help="The command you would like to run. Options are: thGen, thMatch, ccGen, ccMatch, orbGen, ssmGen, ssmMatch, genAllRefVideos")
parser.add_argument("--input", help="Path to the input video file, which is required for most commands.")
parser.add_argument("--working-dir", help="Path to VRD working/root directory. Defaults to current directory.")
args = parser.parse_args()

cmd = args.command
queryVideo = args.input
path, fileName = os.path.split(queryVideo)

config = VRDConfig.VRDConfig()

if args.working_dir == None:
    config.workingDir = "."
else:
    config.workingDir = args.working_dir


if cmd == None:
    MultiLevelMatcher.MultiLevelMatcher(config).run(queryVideo)

if cmd == "fpAll":
    qFrames, ccFrames = ThGenerator.ThGenerator(config).run(queryVideo)
    ThMatcher.ThMatcher(config).run(qFrames)
    #CCGenerator.CCGenerator.run(ccFrames)
    #CCMatcher.CCMatcher().run()


if cmd == "ccGen":
    CCGenerator.CCGenerator(config).run(queryVideo)

if cmd == "ccMatch":
    ccMatcher = CCMatcher.CCMatcher(config)

if cmd == "thGen":
    ThGenerator.ThGenerator(config).run(queryVideo)

if cmd == "thMatch":
    vu = VRDUtil.VRDUtil(config)
    thMatcher = ThMatcher.ThMatcher(config)
    videos = vu.getReferenceVideosList()
    processedVideos = 0

    qvPath, qvFilename = os.path.split(queryVideo)
    qVideo = vu.readFramesFromDrive("assets/fingerprints/"+qvFilename+"/Th")

    for video in videos:
        rvPath, rvFilename = os.path.split(video)
        rVideo = vu.readFramesFromDrive("assets/fingerprints/"+rvFilename+"/Th")
        significantFrameMatches = thMatcher.thMatchVideos(qVideo, rVideo)
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


if cmd == "genAllRefVideos":
    refLibPath = "assets/video-reference-library"

    files = [f for f in listdir(refLibPath) if isfile(join(refLibPath, f))]

    thGen = ThGenerator(config)
    for file in files:

        #Check if already exists
        if os.path.exists("assets/fingerprints/"+file):
            print("Skippping existing: "+file)
        else:
            size = os.path.getsize(refLibPath+"/"+file)
            print("Processing: "+file+" ("+str(round(size/1024/1024))+"MB)")
            thGen.run(refLibPath+"/"+file)


