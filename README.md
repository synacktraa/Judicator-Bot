# Judicator Bot, created for Open Source discord server
<p align="center"><img src="https://i.imgur.com/ySjnID2.jpg" width="300" height="400"></p>

## Functionality
 - Gives user a role according to his reaction on specified message.
 - Sends styled message to specified resource channel.
 - Censorship on server.
 - Slash commands support.
 - Buttons interactions. (In developing)

## Commands
 - /help | Shows all available commands.
 - /ping | Simple ping-pong game.
 - /hello | Greets the user.
 - /logout | Turns off the bot.
 - /stats | Shows the detailed information about bot.
 - /post | Sends message in block to specific channel.
 - /channels | Shows available channels for source command.
 - /clear | Deletes specific number of messages.

## Deploy to Heroku
 > We are using [Heroku](https://www.heroku.com) as hosting for this bot.

 List of repository secrets you need to properly deploy your bot to heroku:
 ```
 1. DISCORD_TOKEN
 2. GUILD_ID
 3. HEROKU_API_KEY
 4. HEROKU_APP_NAME
 5. HEROKU_EMAIL
 ```
 To store discord token and guild id on the hosting usage of `secrets.py` is enough.
 
 For local tests you should also use `setup_secrets.py`, it will save your token and id on your system.
 
 To add more secret variables modify `secrets.py` and `setup_secrets.py`. 
