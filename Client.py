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

	def setPlayList(self):
		playList = self.spotify.current_user_playlists(limit=50)
		total = 0
		if playList['total'] < playList['limit']:
			total = playList['total']
		else:
			total = playList['limit']

		for i in range(total):
			self.playList[i] = (playList['items'][i]['name'], playList['items'][i]['id'], playList['items'][i]['tracks']['total'])
		self.playList[total] = ('Liked songs', 'Liked songs', 'Liked songs')

	def printPlayList(self):
		print("\tList of playlists...")
		for key, value in self.playList.items():
			print(key, ".", value[0])
		print()

	def selectPlayList(self):
		self.printPlayList()
		option = 1
		selection = 0
		playListCount = len(self.playList)
		playListSelectedCount = 0

		while playListSelectedCount < playListCount:
			try:
				selection = (int)(input("Select a playList to play: "))
				if selection in range(0, playListCount):
					if not self.findPlayList(selection):
						self.selectionPlayList.append(self.playList[selection])
						playListSelectedCount += 1
				else:
					print("Select a valid number...")
				option = input("Wanna add another 1, exit x: ")
				if option == 'x':
					break
			except ValueError:
				print("Invalid selection")

		print("\n\tPlaylists selected...")
		for i in range(len(self.selectionPlayList)):
			print("--> " + self.selectionPlayList[i][0])

	def findPlayList(self, selection):
		id = self.playList[selection][1]
		slpLen = len(self.selectionPlayList)
		for i in range(slpLen):
			if id == self.selectionPlayList[i][1]:
				return True
		return False

	def plMixed(self):
		songSelectedPos = None
		totalPlaylist = len(self.selectionPlayList)
		totalSongs = 0

		#sp is a dictionary with playList and tracks
		sp = {}
		for i in range(totalPlaylist):
			id = self.selectionPlayList[i][1]
			if id == 'Liked songs':
				sp[id] = self.savedSongs
			else:
				sp[id] = self.getTracks(id)
		#remove duplicate songs
		if totalPlaylist > 1:
			sp = self.findDifference(sp)

		for key in sp:
			totalSongs += len(sp[key])

		i = 0
		while i < totalSongs:
			plSelected = random.randint(0, totalPlaylist-1)
			songSelectedPos = random.randint(0, len(sp[self.selectionPlayList[plSelected][1]]) - 1)
			songId = sp[self.selectionPlayList[plSelected][1]][songSelectedPos]
			if songId == None: #when a song is import locally
				i += 1
			elif not self.findSong(songId):
				self.songsToPlay.append(songId)
				self.spotify.add_to_queue(songId)
				i += 1

	def getTracks(self, id):
		tracks = self.spotify.playlist_tracks(id, fields='items.track.id', limit=100, additional_types=('track',))
		total = self.spotify.playlist_tracks(id, fields='total', limit=1, additional_types=('track',))
		#Due that the limit is 100 songs, you obtain in this
		#"while" the next songs of the playlist until it completes the total amount
		while len(tracks['items']) < total['total']:
			offs =  len(tracks['items'])
			aux = {}
			aux = self.spotify.playlist_tracks(id, fields='items.track.id', offset=offs,limit=100, additional_types=('track',))
			dif = total['total'] - offs
			#adding new tracks of the current playList
			for i in range(dif):
				tracks['items'].append(aux['items'][i])
		#create an array with only tracks id's
		arrTracks = []
		tLen = len(tracks['items'])
		for i in range(tLen):
			arrTracks.append(tracks['items'][i]['track']['id'])

		return arrTracks

	def findSong(self, id):
		if id in self.songsToPlay:
			return True
		return False

	def findDifference(self, sp):
		auxName = ''
		auxNameNext = ''
		#remove duplicate songs in playlists selected
		splLen = len(self.selectionPlayList) - 1

		for i in range(splLen):
			auxName = self.selectionPlayList[i][1]
			aux = i+1
			#get difference between the last and firts
			if aux == len(self.selectionPlayList):
				aux = 0
			auxNameNext = self.selectionPlayList[aux][1]
			sp[auxName] = list(set(sp[auxName]).difference(sp[auxNameNext]))

		return sp

	def savedTracks(self):
		save = self.spotify.current_user_saved_tracks(limit=50)
		total = save['total']
		limit = 50
		if len(save['items']) < 50:
			limit = len(save['items'])

		while len(self.savedSongs) < total:
			for i in range(limit):
				self.savedSongs.append(save['items'][i]['track']['id'])
			save = self.spotify.current_user_saved_tracks(limit=50, offset=len(self.savedSongs))
			if len(save['items']) < 50:
				limit = len(save['items'])
