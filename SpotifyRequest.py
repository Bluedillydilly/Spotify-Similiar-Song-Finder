"""

"""
import sys
sys.path.insert(1, '/home/dc/projects/python/')
import Kmeans
import numpy as np
from SpotifyAuth import bearAuthHeader
from requests import get
from json import loads
from audioFeaturesHelper import ignoreFeatures, listFeatures, maxValues
from math import ceil
from time import time

class SpotifyRequester:
    BASE = "https://api.spotify.com/v1/"

    def __init__(self):
        self.auth = bearAuthHeader()

    def request(self, baseMod="", baseModVal="", params=""):
        url = (self.BASE+baseMod).format(baseModVal)
        return loads(get(url, params=params, headers=self.auth).text)

    def entirePlaylistSongs(self, playlistID):
        count = 0
        allSongIDs = []
        while True:
            batch = self.playlistRequest(playlistID, offset=count)
            if not batch['items']:
                break
            for song in batch['items']:
                allSongIDs.append(song['track']['id'])
            count +=1
        return allSongIDs

    def playlistRequest(self, playlistID, offset=0):
        return self.request(baseMod="playlists/{}/tracks", baseModVal=playlistID, params={"offset":100*offset})

    def songRequest(self, songIDs):
        """
        Max of 50 ids
        """
        return self.request(baseMod="tracks", params={"ids":songIDs})

    def audioFeatures(self, songIDs):
        """
        Max of 100 ids
        """
        return self.request(baseMod="audio-features", params={"ids":",".join(songIDs)})

    def audioFeaturesPruned(self, songIDs):
        """
        Max of 100 ids
        """
        result = []
        for i in range(ceil(len(songIDs)/100)):
            batch =  self.audioFeatures(songIDs[i*100:(i+1)*100])['audio_features']
            for song in batch:
                for bad in ignoreFeatures:
                    song.pop(bad)
            result +=batch
        return result

    def songName(self,IDs):
        return list(y for x in [[t['name'] for t in 
            self.songRequest(','.join(IDs[s*50:(s+1)*50]), )['tracks']] for s in 
            range(ceil(len(IDs)/50))] for y in x)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 SpotifyRequest.py PLAYLIST_ID")
        exit()
    print("START")
    total = time()

    start = time()
    sp = SpotifyRequester()
    print("Time to create Requester (easy): {}".format(time()-start))

    PLAY_LIST_ID = sys.argv[1]
    start = time()
    allSongsID = sp.entirePlaylistSongs(PLAY_LIST_ID)
    print("Time to get all song ids of the playlist: {}".format(time()-start))

    start = time()
    feats = sp.audioFeaturesPruned(allSongsID)
    print("Time to get all needed audio features of all songs of interest: {}".format(time()-start))
    
    featList = listFeatures(feats)

    start = time()
    kResult = Kmeans.runKmeansTuned(np.array(featList), PRINT=1, RAN=maxValues())
    print("Centroids: ", kResult[0])
    print("Labels: ", kResult[1])
    print("Time to cluster: {}".format(time()-start))
    
    print("Total time til completion: {}".format(time()-total))
