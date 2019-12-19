"""
	Functions related to the audio features of tracks.
	Functions like ranking of songs, etc.
"""
from audioFeaturesHelper import listFeatures, featureRange
from Kmeans import dists
from math import floor, log10

def topN(songs, feat: str, N=5, bottom=False):
	"""
		Params:
			songs: feature, Name tuple list of all songs of interest
			feat: feature of interest
			N: top N songs for the feat
	"""
	fi = list(featureRange.keys()).index(feat)
	songs.sort(reverse=not bottom,
		key= lambda tup: tup[0][fi])
	
	print("-"*75)
	p = "Bottom" if bottom else "Top"
	print(p, len(songs[:N]), "songs for", feat+":")
	for i in range(len(songs[:N])):
		print(str(i+1)+":", songs[i][1] + " "*(56-floor(log10(i+1))-len(songs[i][1])), 
			songs[i][0][fi])

def closestN(songs, target, N=5, far=False):
	"""
		poop
	"""
	distList = [dists(s[0], [target[0]]) for s in songs]
	pairs = list(zip(distList,[s[1] for s in songs]))
	pairs.sort(reverse=far,
		key= lambda tup: tup[0])
	print(pairs)

if __name__ == "__main__":
	from SpotifyRequest import SpotifyRequester

	PL_ID = "30Ljdq1ZGekPrqsNPKKWZH" # muy
	#PL_ID = "5EmJ0c7w1QJbJSZe1VTYWG" # outdated liked songs

	sp = SpotifyRequester()
	songIDs = sp.entirePlaylistSongs(PL_ID)
	songFeats = sp.audioFeaturesPruned(songIDs)
	featList = listFeatures(songFeats)
	
	paired = list(zip(featList,sp.songName(songIDs)))
	#for f in featureRange.keys():
		#topN(paired, f, bottom=0)

	closestN(paired, paired[0])