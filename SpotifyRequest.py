"""

"""
import sys
sys.path.insert(1, '/home/dc/projects/python/')
from kmeans import Kmeans
from SpotifyAuth import bearAuthHeader
from requests import get
from json import loads
from audioFeatures import ignoreFeatures, listFeatures, maxValues
from math import ceil
import numpy as np
from time import time

class SpotifyRequest:
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
        #url = (self.BASE+"playlists/{}/tracks").format(playlistID)
        #return loads(get(url, headers=self.auth).text)

    def songRequest(self, songIDs):
        """
        Max of 50 ids
        """
        return self.request(baseMod="tracks", params={"ids":songIDs})
        #url = self.BASE + "tracks"
        #return loads(get(url, params={"ids":songIDs}, headers=self.auth).text)

    def audioFeatures(self, songIDs):
        """
        Max of 100 ids
        """
        return self.request(baseMod="audio-features", params={"ids":",".join(songIDs)})
        #url = self.BASE + "audio-features"
        #return loads(get(url, params={"ids":songIDs}, headers=self.auth).text)

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 SpotifyRequest.py PLAYLIST_ID")
        exit()
    print("START")
    total = time()

    start = time()
    sp = SpotifyRequest()
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
