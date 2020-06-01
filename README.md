This script shows all playlist from a user of spotify and let you mixed many of them so all the tracks are added to queue and play in a device where you have spotify installed.

Firts of all:

1. Create or log in with you spotify account in spotify developer.
2. Click in "Create a Client id"
3. Select a:
    - Name for this
    - A description
    - Desktop app
    - Non-commercial(if yoy want)
    - Accept the terms
4. In your application copy:
    - Choose a Redirect URIs
        * You can choose somethin like: 'https://www.google.mx/', this is needed for give you a token in the Url browser

5. In the folder where you cloned the project, export the following:
    - Client ID and paste it in terminal    
		* export SPOTIPY_CLIENT_ID=''
    - Client secret and paste it in terminal
		* export SPOTIPY_CLIENT_SECRET=''
    - Copy your Redirect URIs and paste it in terminal
		* export SPOTIPY_REDIRECT_URI='https://www.google.mx/'

6. Run the main file adding your usernarme from your spotify account
    - python main.py "username"
7. A browser will open with the URL that you put in Redirect URIs. Spotify gives you a code, that code has to be copy and paste in the terminal


Using the program:

If the credentials goes well, the program shows the list of devices availables so you can choose one.

The terminal shows you to a current song and artist if are playing some track in yours devices.

Next, a list of all your playlist is put in the terminal. Here is when you choose all list has to be mixed by the script and add to the queue.
