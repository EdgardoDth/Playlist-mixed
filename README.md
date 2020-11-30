This script shows all playlist from a user of spotify and let you mixed many of them so all the tracks are added to queue and play in a device where you have spotify installed.

Firts of all:

1. Create or log in with you spotify account in spotify developer.
    - https://developer.spotify.com/dashboard/login
2. Click in "Create a Client id"
3. Select a:
    - Name for this
    - A description
    - Desktop app
    - Non-commercial(if you want)
    - Accept the terms
4. In your application copy:
    - Choose a Redirect URIs, is important see the URL added, otherwise, the URL is invalid
        * You can choose something like: 'https://www.google.mx/', this is needed for give you a token in the Url browser

5. In the folder where you cloned the project, export the following:
    - Client ID and paste it in terminal(this information is in you developer.spotify account)    
		* ```export SPOTIPY_CLIENT_ID='put-here-your-client-id'```
    - Client secret and paste it in terminal(this information is in you developer.spotify account)
		* ```export SPOTIPY_CLIENT_SECRET='put-here-your-client-secret'```
    - Copy your Redirect URIs and paste it in terminal(has to be the same URL that you put in the step 4)
		* ```export SPOTIPY_REDIRECT_URI='https://www.google.mx/'```

6. Run the main file adding your usernarme from your spotify account
    - ```python main.py "username"```
7. A browser will open, Spotify ask you if you wanna give permission. If you accepted, you will redirect to the URL that you put in Redirect URIs. Spotify gives you a code, that code has to be copy and paste in the terminal, only copy the code after the URL, in this example.
    - ```https://www.google.mx/?code=CODEtoCOPY```


Using the program:

If the credentials goes well, the program shows the list of devices availables so you can choose one.

The terminal shows you to a current song and artist if are playing some track in yours devices.

Next, a list of all your playlist is put in the terminal. Here is when you choose all list has to be mixed by the script and add to the queue.
