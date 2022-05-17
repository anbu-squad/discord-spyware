# discord-spyware
The spyware uses the discord api to save the data for complete anonymity. You don't have to create a server for the client and bother about security.

## Disclaimer
I do not take responsibility for wrong use of the discord-spyware. It's made for educational purposes only.

## Set up
### Script
You'll need to install some libaries first:
```
pip install -U discord.py
pip install -U psutil
pip install pynput
```
### Discord
So first you need to create an account on Discord if you don't have one yet. Then you need to [create an application](https://discord.com/developers/applications) and copy the token of your bot.
![Application](https://poshbot.readthedocs.io/en/latest/guides/backends/discord-new-application.png)
![Bot](https://files.realpython.com/media/discord-bot-add-bot.4735c88ff16b.png)
![Token](https://cdn.writebots.com/wp-content/uploads/2021/12/discord-bot-token-11.jpg)

Now you need to paste the token in our `config.py` file where the variable is called `TOKEN`. After you pasted the token i would recommend to create a server with four channels and then invite the bot into that server. 

You'll see that there are three more variables in `config.py` where you can paste the id of three of the channels you just created.

The `INFOCHANNEL` variable should be the channel where the bot sends a message with the hostname of the computer every time the program starts.

The `LOG` variable should be the channel where all the keystrokes should be send.

The `APP` variable should be the channel where all the processes which were opened and closed in the last minute should be sent.

You can use your fourth channel to interact with the bot to keep everything else clean and arranged.

## Commands

You can see all commands when you use `$help` in a discord channel. For more information on a command you can use `$help [command]`.

## Why Discord?
I'm going to explain this question with an example. Let's just assume I'm going to attack my dogs computer so I somehow need to install the spyware on his computer. I set up my script as explained above and made an `.exe` with [pysinstaller](https://pyinstaller.org/en/stable/). There are multiple ways to install the `.exe` but I'll just install it manually. I put the spyware in his autorun folder so that it'll start up as soon as he boots up his Computer. At this point you would need a listener/server if you were using a reverse shell. The problem I encountered with the reverse shell is that it isn't completely anonymous. You are able to trace back the reverse shell which is not good if our spyware would be found. So I came up with the idea to use the [Discord-Api](https://discord.com/developers/docs/intro). On Discord you are able to create an account completely anonymous. You only need to verify an email-adress which could also be created anonymously with [Protonmail](https://protonmail.com/), for example. But you shouldn't forget to use a VPN and hide your client information (Device Name, Web Browser, and so forth...) because Discord saves all this information during the login and while your using their applictaion. Now all the data of my dog is sent to my Discord server and channels as soon as he boots up his computer.
