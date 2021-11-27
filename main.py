import discord
from discord.ext import commands
import sheetsAPI
import json

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="!", intents=default_intents)

# dictionnary that matches names in the sheet with discord users
nameDict = {
    'CheeseNan':['CheeseNan','0193'], 
    'Luciana':['LordOmar','3525'], 
    'Spac3fiend':[ 'Spac3fiend','2689'], 
    'Karasaki':[ '私は元気','9185'], 
    'Seybolt':[ 'Seybolt','8574'], 
    'Aa':[ 'PbZeppelin','9231'], 
    'Medvind':[ 'Sir Medvind','1788'], 
    'm1lk':[ 'm1lk','9697'], 
    'keep4mid':[ 'twentythree','6614'], 
    'Kona':[ 'Kona','2404'], 
    'gunder':[ 'Monkey D. Jesus','2780'],
    'Lavrik':[ 'Chalt(Lavrik)','1668'], 
    'BREKFAST':[ 'Brekfast','5879'], 
    'Lurfan':[ 'Definitely not someone','1918'], 
    'Tivox':[ 'CHRlS','8742'], 
    'bebciok':[ 'bebciu','5931'], 
    'necredome':[ 'necredome','9999'], 
    'Veratz':[ 'Verac','7008'], 
    'Zeta':[ 'Zean_Zeko','0460'], 
    'Arrow':[ 'arrow','0341'], 
    'Yuri':[ 'Galatz','6763'], 
    'Panduki':[ 'Panduki','0596'], 
    'Luffy':[ 'Monkey D. Jesus','2780'], 
    'Koharu':[ 'SoupBananas','6694'], 
    'Rytse':[ 'Rytse Saika','1053'], 
    'Irene':[ 'Taurus','5141'], 
    'Lu':[ 'Lu','7543'], 
    'Etoinette':[ 'Shellfish','8544']
}

# get values from the sheet
values = sheetsAPI.getValues()

@bot.event
async def on_ready():
    print("bot is ready!")

# pings the members that haven't raided yet
@bot.command(name="remind")
async def ping(ctx, arg):
    values = sheetsAPI.getValues()
    # check if command is in bot command channel
    if ctx.channel.id == 856612203595956274:
        # add 1 if >7 because of the mid-raid damage column
        arg = int(arg)
        if arg > 0 and arg < 15:
            if (arg > 7):
                arg += 1
            pingString = ''
            pingList = []
            for line in values:
                # check if cell is empty (try) or if number in cell <3
                # in both cases add user to the pinglist
                try:
                    if int(line[arg]) < 3:
                        pingList.append(nameDict[line[0]])
                except:
                    pingList.append(nameDict[line[0]])
            # searching for the user and putting all mentions in 1 string
            for name, discriminator in pingList:
                try:
                    user = discord.utils.get(ctx.guild.members, name = name, discriminator = discriminator)
                    pingString += user.mention + ' '
                except:
                    await ctx.channel.send(f'User with name {name} and discriminator {discriminator} not found. In game name: {list(nameDict.keys())[list(nameDict.values()).index([name, discriminator])]}')
            # add ':catdepressed:' custom emote
            pingString += '<:catdepressed:811005091745890304>'
            # send message in alts channel
            channel = bot.get_channel(845349597014655026)
            await channel.send(pingString)
        else:
            await ctx.channel.send('Wrong argument: raid day number between 1 and 14.')

bot.run(json.load(open('botToken.json'))['TOKEN'])