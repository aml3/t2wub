import subprocess
import random
import sys
import os
import AlchemyAPI
import xml.etree.ElementTree as ET


global BEAT_LENGTH
BEAT_LENGTH= 0.428571428571429

def text2wave(text):
    outputfile = "/tmp/output.wav"
    textemp = text.split(" ")
    text = []
    for word in textemp:
        if word == '':
            pass
        text += [word[i:i+15] for i in range(0,len(word),15)]
    l = len(text)
    file_list = [];
    dirname = os.path.dirname(os.path.realpath(__file__))
    for i,word in enumerate(text):
        subprocess.check_output([dirname + "/get_word.sh", word])
        subprocess.call(["sleep", ".1"])
        subprocess.call(["sox", "/tmp/output.mp3", "/tmp/word%d.wav"%i])
        pad_wave(i+0.5, l+4, "/tmp/word%d.wav"%i)
        file_list.append("word%d_padded"%i)
    subprocess.call(["sox", "-m"]+["/tmp/word%d_padded.wav"%i for i in range(l)]+[outputfile, "norm"])
    # clean up
    subprocess.call(["rm", "/tmp/output.mp3"])
    return (outputfile, l+4)

def pad_wave(start, total, filename):
    global BEAT_LENGTH
    subprocess.call(("sox %s %s_padded.wav pad %f %f"%(filename, filename[:-4], 
            start*BEAT_LENGTH, (total-start)*BEAT_LENGTH-sound_length(filename))
            ).split(' '))

def sound_length(filename):
    return float(subprocess.check_output(['soxi', '-D', filename]))

def melodify(filename, numbeats, sentiment):
    collection = [["E2", "A3", "C3", "E3", "A4", "C4", "E4"],#minor
                  ["F2", "G2", "A3", "B3", "F3", "G3", "A4", "B4"],#dissonant
                  ["G2", "C3", "E3", "G3", "C4", "E2", "E4"]]#major
    notes = collection[int(sentiment+1)]
    newname = "/tmp/melody_output.wav"
    dirname = os.path.dirname(os.path.realpath(__file__))
    for i in range(numbeats):
        subprocess.call(("sox %s -r 16k /tmp/synth%d.wav synth .42857 sawtooth %s"%
            (filename, i, random.choice(notes))).split(" "))
        pad_wave(i, numbeats, "/tmp/synth%d.wav"%i)
    subprocess.call(["sox", "-m"]+["/tmp/synth%d_padded.wav"%i for 
                i in range(numbeats)]+["/tmp/tempmelody.wav", "norm"])
    subprocess.call(("sox %s/samples/pink_noise.wav /tmp/noise.wav trim 0.0 %f"%(dirname, sound_length("/tmp/tempmelody.wav"))).split(" "))
    subprocess.call(("sox -m /tmp/tempmelody.wav /tmp/noise.wav /tmp/melody.wav").split(" "))
    subprocess.call((dirname + "/vocoder -q %s %s %s"%(filename, "/tmp/melody.wav", "/tmp/tempvoice.wav")).split(" "))
    #subprocess.call(("sox /tmp/melody2.wav -c 2 %s"%newname).split(" "))
    subprocess.call(("sox %s /tmp/tempvoice2.wav"%filename).split(" "))
    subprocess.call(("sox -r 16k --norm -m -v 0.4 /tmp/tempvoice2.wav /tmp/tempvoice.wav -c 2 %s"%newname).split(" "))
    return newname

def dubstepify(filename, numbeats, outfilename, sentimental_value):
    global BEAT_LENGTH
    dirname = os.path.dirname(os.path.realpath(__file__))
    totalwubfiles = 14
    wubnumbers = range(totalwubfiles+1) + [0 for i in range(totalwubfiles/3)]
    wubabilities = open(dirname+"/samples/wub_sentiments", 'r').read().strip().split("\n")
    wubabilities = {i: (3 if int(wubabilities[i])==sentimental_value else 1) 
                        for i in range(len(wubabilities))}
    wubnumbers = [val for val in wubnumbers for i in range(wubabilities[val])]
    missing = (numbeats)%4
    numbeats += (4-missing)
    for i in range(0, numbeats-2, 2):
        subprocess.call(("sox %s/samples/wub%d.wav /tmp/wub%d.wav gain -n"%
            (dirname, random.choice(wubnumbers), i)).split(" "))
        pad_wave(i, numbeats, "/tmp/wub%d.wav"%i)

    subprocess.call(["sox", "-m"]+["/tmp/wub%d_padded.wav"%i for 
                i in range(0, numbeats-2, 2)]+["/tmp/tempwub.wav", "norm"])
    subprocess.call(("sox -m -v 0.5 /tmp/tempwub.wav -v 0.6 %s/samples/loop1.wav /tmp/loop.wav trim 0 %f rate 16k"%(dirname, BEAT_LENGTH*(numbeats))).split(" "))
    subprocess.call(("sox -m /tmp/loop.wav %s /tmp/finaloutput.wav"%filename).split(" ")) 
    subprocess.call(["lame", "/tmp/finaloutput.wav", outfilename+".mp3"])

def sentiment_analysis(text):
	alchemyObj = AlchemyAPI.AlchemyAPI()
	alchemyObj.loadAPIKey("api_key.txt");

	sent = False 
	score = 0	
	result = alchemyObj.TextGetTextSentiment(text);
	print text 
	root = ET.fromstring(result) 
	for entry in root.iter('docSentiment'):
		print entry
		for e in entry:
			print e
			if e.tag == "mixed":
				sent = bool(e.text)
			elif e.tag == "score":
				score = float(e.text)
	print score, sent
	return (sent, score)

if __name__ == "__main__": 
    inputfile = sys.argv[1]
    text = open(inputfile, 'r').read().strip()
    mixed, sentimental_value = sentiment_analysis(text)
    filename, numbeats = text2wave(text)
    newfilename = melodify(filename, numbeats, 0 if mixed or sentimental_value == 0 else sentimental_value / abs(sentimental_value))
    dubstepify(newfilename, numbeats, inputfile, sentimental_value)
