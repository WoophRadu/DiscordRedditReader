# DiscordRedditReader
DiscordRedditReader is a bot that takes posts from Reddit and puts them into Discord channels. 


## Features

 * Selective multi-linking: Bind any number of subreddits to any number of Discord channels.
 * Configurable post-checking interval: Fetch posts from Reddit every chosen X amount of time.
 * Logging: have a log of all the posts fetched, so you can better understand what's being put into your channels.
 * Custom command prefix: By default set to ```!```, you can change the command prefix to anything you like, so the bot doesn't interfere with your other bots.
 
### Planned features (not implemented yet):
 * Fetch on demand: get posts from Reddit on demand, using a command.
 * Reddit sorting fetch modes: get posts from New, Controversial, Top, or Hot (right now it's set to default to Hot)

## How to set up
Firstly, we need to be sure you have all the requirements. This will be different, depending if you're running Windows or Linux.

This bot is written in Python 3.9, so let's get that first.
### Windows installation
Go to https://www.python.org/ and grab the latest 3.9 x86 Windows version. Install it and make sure you check the box for ```Add Python 3.9 to PATH```.

Next, we'll clone this repository to your computer (we download the files). Here on GitHub, click the ```Clone or download``` green button, then choose ```Download ZIP```, then unpack the ZIP wherever you please. Alternatively, advanced users can use ```git``` to clone the repo, which I won't explain because you're already an advanced user ;)

### Linux installation
To install Python 3.9 on Linux, you'll need to follow some tutorial you find online, cus right now I can't be bothered to do that.

Next, we'll use git to clone the files to your computer. If you don't have git already installed, follow [this tutorial](https://git-scm.com/book/en/v1/Getting-Started-Installing-Git) to get it working on your linux machine. cd into a folder of your pleasing, then run this:
```
git clone https://github.com/WoophRadu/DiscordRedditReader.git
```
This will create a new folder named ```DiscordRedditReader``` in the folder you are cd'd into, containing all the files.

### Creating the Discord Bot account
Go to https://discordapp.com/developers/applications/me (be logged in while doing so) and click ```(+) New App```. ```App name``` will be the Bot's username, so choose that. Leave ```App description``` blank and maybe give the Bot an avatar by adding a picture to ```App icon```, then click ```Create App```. Scroll down a little bit, then click ```Create a Bot User```.

### Adding the Discord Bot to a server
Go to https://discordapp.com/developers/applications/me (be logged in while doing so) and click the app that represents your Bot. Scroll down a bit, then click ```Generate OAuth2 URL``` under the ```Bot``` paragraph. That is the link that you can give to server owners in order to add the bot to their server. If you access it yourself, you will be prompted to choose which server you want to add the Bot to. You need to have the "Administrator" permission in order to add a bot to a server.

### Linking DiscordRedditReader to your Discord Bot account
Go to https://discordapp.com/developers/applications/me (be logged in while doing so) and click the app that represents your Bot. Scroll down a bit, then, under the ```Bot``` paragraph you should see ```Token: click to reveal```. Click that, and you will be given the auth token for your bot account, which we'll paste into the configuration file, in the next step.

### Configuring DiscordRedditReader
You SHOULDN'T do this using Notepad. Get another text editor like Notepad++ or Atom. When you have that, go into the folder you chose when installing the bot, run ```run_win.bat``` for Windows or ```run_linux.sh``` for Linux. You should now find a new file called ```config.ini```. Open that with your text editor and configure the bot to your liking, using the instructions provided in the file. Save it when you're done.

Please DO NOT TOUCH ```default_config.ini```!

### Running DiscordRedditReader
If you're on Windows, double-click ```run_win.bat``` and you're good to go.

If you're on Linux, run this:
```
./run_linux.sh
```
That should be it.
## Thanks to

 * [PRAW](https://github.com/praw-dev/praw)
 * [discord.py](https://github.com/Rapptz/discord.py)
 * you
