"""

"""

featureRange = {
    "danceability":(0,1),
    "energy":(0,1),
    "key":(-1,8),
    "loudness":(-60,0),
    "mode":(0,1),
    "speechiness":(0,1),
    "acousticness":(0,1),
    "instrumentalness":(0,1),
    "liveness":(0,1),
    "valence":(0,1),
    "tempo":(0,250),
    #"time_signature":(0,6),
    #"duration_ms":(0,2*60*60*1000)
}

ignoreFeatures = [
    "type", "uri", "track_href", "analysis_url"
]

def maxValues():
    return [featureRange[key][1] for key in featureRange.keys()]

def minValues():
    return [featureRange[key][0] for key in featureRange.keys()]

def rangeValues():
    return [featureRange[key] for key in featureRange.keys()]

def listFeatures(featureDictList):
    """
    Parameters:
        featureDictList - a list of dictionary objects that contain audioFeatures of a song.

    Output:
        2d array of features. List of lists of song features
    """
    allFeatures = []
    for song in featureDictList:
        songInfo = []
        for key in featureRange.keys():
            songInfo.append(song[key])
        allFeatures.append(songInfo)
    return allFeatures