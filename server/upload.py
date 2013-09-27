import soundcloud
import sys

def upload(wubFile,commentText):
	client = soundcloud.Client(client_id='',client_secret='', username='', password='')
	track = client.post('/tracks', track={'title': commentText, 'asset_data': open(wubFile, 'rb'), 'downloadable': True, 'streamable': True})
	print track.permalink_url

if __name__=="__main__":
	upload(sys.argv[1],sys.argv[2])
