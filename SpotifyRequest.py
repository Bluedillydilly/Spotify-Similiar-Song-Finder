"""

"""
import sys
sys.path.insert(1, '/home/dc/projects/python/twitter')
from SpotifyAuth import *
from requests import get
from json import loads
from audioFeatures import ignoreFeatures, listFeatures
from math import ceil

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
    sp = SpotifyRequest()
    #print(get("https://api.spotify.com/v1/audio-features", 
    #params={"ids":",".join(["5FI7poC3O5ELlYLmUFQ5sC","682TDtMAq9UcKN0QqVN019"])}, headers=sp.auth).text)
    feats = sp.audioFeaturesPruned(["5FI7poC3O5ELlYLmUFQ5sC","682TDtMAq9UcKN0QqVN019"])
    print(feats)
    featList = listFeatures(feats)
    print(featList)
