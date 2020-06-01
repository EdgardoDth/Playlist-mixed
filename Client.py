import random

class Client(object):
	def __init__(self, spotify):
		self.spotify = spotify
		self.playList = {}
		self.selectionPlayList = []
		self.songsToPlay = []
		self.device = None
		self.savedSongs = []

	def setDevice(self, device):
		self.device = device

	def getSpotify(self):
		return self.spotify

	def savedTracks(self):
		save = self.spotify.current_user_saved_tracks(limit=50)
		total = save['total']
		limit = len(save['items'])
		while len(self.savedSongs) < total:
			for i in range(limit):
				self.savedSongs.append(save['items'][i]['track']['id'])
			save = self.spotify.current_user_saved_tracks(limit=50, offset=len(self.savedSongs))
			print(limit)

		for i in range(len(self.savedSongs)):
			print(self.savedSongs[i])

	def setPlayList(self):
		playList = self.spotify.current_user_playlists(limit=50)
		total = 0
		if playList['total'] < playList['limit']:
			total = playList['total']
		else:
			total = playList['limit']

		for i in range(total):
			self.playList[i] = (playList['items'][i]['name'], playList['items'][i]['id'], playList['items'][i]['tracks']['total'])

	def printPlayList(self):
		print("\tList of playlists...")
		for key, value in self.playList.items():
			print(key, ".", value[0])
		print()

	def selectPlayList(self):
		self.printPlayList()
		option = 1
		selection = 0
		while True:
			if len(self.selectionPlayList) == len(self.playList):
				break
			selection = (int)(input("Select a playList to play: "))
			if selection in range(0, len(self.playList)):
				if not self.findPlayList(selection):
					self.selectionPlayList.append(self.playList[selection])
			option = input("Wanna add another 1, exit x: ")
			if option == 'x':
				break

		print("\tPlayList selected...")
		for i in range(len(self.selectionPlayList)):
			print("--> " + self.selectionPlayList[i][0])


	def findPlayList(self, selection):
		name = self.playList[selection][1]
		for i in range(len(self.selectionPlayList)):
			if name == self.selectionPlayList[i][1]:
				return True
		return False

	def playMixed(self):
		songSelectedPos = None
		totalPlaylist = len(self.selectionPlayList)
		totalSongs = 0

		sp = {}
		for i in range(totalPlaylist):
			id = self.selectionPlayList[i][1]
			sp[id] = self.getTracks(id)

		if len(self.selectionPlayList) > 1:
			sp = self.findDifference(sp)

		for key in sp:
			totalSongs += len(sp[key])

		i = 0
		while i < totalSongs:
			sel = random.randint(0, totalPlaylist-1)
			songSelectedPos = random.randint(0, len(sp[self.selectionPlayList[sel][1]])-1)
			songId = sp[self.selectionPlayList[sel][1]][songSelectedPos] #['track']['id']
			if songId == None:
				i += 1
			elif not self.findSong(songId):
				self.songsToPlay.append(songId)
				self.spotify.add_to_queue(songId)
				i += 1

	def getTracks(self, id):
		tracks = self.spotify.playlist_tracks(id, fields='items.track.id', limit=100, additional_types=('track',))
		total = self.spotify.playlist_tracks(id, fields='total', limit=1, additional_types=('track',))

		while len(tracks['items']) < total['total']:
			offs =  len(tracks['items'])
			aux = {}
			aux = self.spotify.playlist_tracks(id, fields='items.track.id', offset=offs,limit=100, additional_types=('track',))
			ran = self.spotify.playlist_tracks(id, fields='total', offset=offs,limit=1, additional_types=('track',))
			ranSize = ran['total'] - len(tracks['items'])

			for i in range(ranSize):
				tracks['items'].append(aux['items'][i])

		arrTracks = []
		for i in range(len(tracks['items'])):
			arrTracks.append(tracks['items'][i]['track']['id'])

		return arrTracks

	def findSong(self, id):
		if id in self.songsToPlay:
			return True
		return False

	def findDifference(self, sp):
		auxName = ''
		auxNameNext = ''
		if len(self.selectionPlayList) == 2:
			sp[self.selectionPlayList[0][1]] = list(set(sp[self.selectionPlayList[0][1]]).difference(sp[self.selectionPlayList[1][1]]))
			return sp

		for i in range(len(self.selectionPlayList)-1):
			auxName = self.selectionPlayList[i][1]
			aux = i+1
			if aux == len(self.selectionPlayList):
				aux = 0
			auxNameNext = self.selectionPlayList[aux][1]
			sp[auxName] = list(set(sp[auxName]).difference(sp[auxNameNext]))

		return sp
