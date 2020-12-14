import discord
import sys
import codecs
from discord.ext import commands
import logger
import logging
import configparser
import os.path
from shutil import copyfile
import time
import praw
import secrets

if sys.platform == "win32":
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=20, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')
logger.log("--- INITIALIZING ---")

config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read("config.ini")
else:
    try:
        copyfile("default_config.ini", "config.ini")
        logger.log("Config file config.ini not found, generating a new one from default_config.ini", "warning")
        time.sleep(1)
        config.read("config.ini")
    except:
        logger.log("FATAL: Neither config.ini , nor default_config.ini do not exist, cannot create bot. Exiting in 5 seconds.", "critical")
        time.sleep(5)
        sys.exit(1)

try:
    token = config["Login"]["token"]
    loglevel = int(config["Logging"]["level"])
    redditUser = config["RedditLogin"]["username"]
    redditPassword = config["RedditLogin"]["password"]
    redditID = config["RedditLogin"]["client_id"]
    redditSecret = config["RedditLogin"]["client_secret"]
    botCommandPrefix = config["Options"]["command_prefix"]
    fetchInterval = int(config["AutoFetch"]["fetch_interval"])
    skipSticky = config["AutoFetch"]["skip_sticky"]
    channelToSubreddit = dict()
    channelPostAmount = dict()
    for section in config.sections():
        if section[:7] == "Channel":
            channelID = config[section]["channel_id"]
            channelToSubreddit[channelID] = config[section]["subreddits"].split()
            channelPostAmount[channelID] = int(config[section]["post_amount"])
except:
    logger.log("Something wrong with the config. If you crash, delete it so we can regenerate it.", "error")

logging.Logger.setLevel(logging.getLogger(), loglevel)
logger.setlevel(loglevel)

if not (redditUser == "YourUsername" or redditPassword == "YourPassword" or redditID == "YourID" or redditSecret == "YourSecret"):
    reddit = praw.Reddit(client_id=redditID, client_secret=redditSecret, password=redditPassword, username=redditUser, user_agent='DiscordRedditSubmitter (coded by u/WoophRadu, src at github.com/WoophRadu/DiscordRedditSubmitter)')
    reddit.validate_on_submit = True
    logger.log("Logged into reddit as /u/" + redditUser)
else:
    logger.log("Some settings are default in config.ini , you need to change them in order to get the all the functionality working. Exiting in 5 seconds.", "critical")
    time.sleep(5)
    sys.exit(1)

description = '''A Discord bot that you can configure to automatically submit posts to reddit.'''
bot = commands.Bot(command_prefix=botCommandPrefix, description=description)

bindedChannels = list()

@bot.event
async def on_ready():
    logger.log("on_ready fired. You are in debug mode.", "debug")
    logger.log("Bot initialized. Logging in...")
    logger.log('Logged in as ' + bot.user.name + ' with ID [' + str(bot.user.id) + '] on:')
    for sv in bot.guilds:
        logger.log('\t[' + str(sv.id) + '] ' + str(sv.name) + ", bound subreddits to channels:")
        for channelID_i in channelToSubreddit.keys():
            channel = bot.get_channel(int(channelID_i))
            if channel in sv.channels:
                bindedChannels.append(channel)
                for subredditName in channelToSubreddit[channelID_i]:
                    logger.log("\t\t/r/" + subredditName + " -> #" + channel.name + " [" + channelID_i + "]")
    while True:
        logger.log("Time to get posts! Attempting to fetch posts from Reddit and post them to Discord...")
        for channel in bindedChannels:
            for subredditName in channelToSubreddit[str(channel.id)]:
                postCounter = 0
                for post in reddit.subreddit(subredditName).hot(limit=channelPostAmount[str(channel.id)]):
                    if post.stickied and (skipSticky in ["true", "True", "1", "yes", "Yes", "y", "Y", "enabled"]):
                        logger.log("Skipped a sticky post. This still counts towards the limit (post_amount). If you're not seeing enough posts, increase your post_amount.")
                    else:
                        postCounter += 1
                        embed = discord.Embed()
                        embed.title = post.title
                        embed.url = "https://www.reddit.com" + post.permalink
                        embed.description = post.selftext[:2040]
                        if not post.is_self:
                            if post.url.lower().endswith((".jpeg", ".jpg", ".png", ".gif")):
                                embed.set_thumbnail(url=post.url)
                                postTypeStr = "link (image)"
                            else:
                                embed.add_field(name="Link from post:", value=post.url, inline=True)
                                postTypeStr = "link"
                        else:
                            postTypeStr = "self-post (text)"
                        embed.colour = discord.Colour(0).from_rgb(255, 86, 0)
                        embed.set_author(name="/r/" + subredditName, url="https://www.reddit.com/r/" + subredditName,
                                         icon_url="https://www.reddit.com/favicon.ico")
                        embed.set_footer(text="/u/" + post.author.name + ", " + postTypeStr,
                                         icon_url=post.author.icon_img)
                        await channel.send(embed=embed)
                        time.sleep(0.51)  # Discord rate-limits to 2 actions / second
                logger.log("Found " + str(postCounter) + " posts in /r/" + subredditName + " \t->\tposted to channel #" + channel.name)
        logger.log("Done fetching posts for now! Check back in " + str(fetchInterval) + " seconds!")
        time.sleep(fetchInterval)


if token == "YourToken":
    logger.log("Bot login token is invalid. You need to go into config.ini and change the token under Login to your bot's token. Exiting in 5 seconds.", "critical")
    time.sleep(5)
    sys.exit(1)
else:
    try:
        bot.run(token)
    except Exception as e:
        logger.log("There was an error while connecting the bot to Discord. Your token might be invalid or you can't connect to Discord's servers. Check following error for details. Exiting in 5 seconds.", "critical")
        logger.exception(e)
        time.sleep(5)
        sys.exit(1)
