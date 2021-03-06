import discord
from discord.ext import commands
from helpers import fetch_sv_data
from config import sv_dir
import json


class AdminCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.message_channel = ""

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await fetch_sv_data(guild)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def sv(self, ctx):
        guild = ctx.message.guild
        await fetch_sv_data(guild)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_announcments_channel(self, ctx, *, message=''):
        with open(f'{sv_dir}/{ctx.message.guild.name}tempt.txt', 'w+') as wr:
            wr.write(message)
        await ctx.send(f"channel set to {message}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        sv_text_channel_dict = {}
        keys = []
        values = []
        with open(f'{sv_dir}/{ctx.message.guild.name}tempt.txt', "r") as rd:
            self.message_channel = rd.read()
        with open(f"{sv_dir}/{ctx.message.guild.name}.json", "r") as rd:
            sv_data = json.loads(rd.read())["text"]
        for elem in sv_data:
            keys.append(elem.split(" => ")[0])
            values.append(elem.split(" => ")[1])
        for x in range(0, len(keys)):
            sv_text_channel_dict[keys[x]] = values[x]
        channel = self.client.get_channel(int(sv_text_channel_dict[self.message_channel]))
        embed_var = discord.Embed(title=f"{message}", color=0x00ff00)
        await channel.send(embed=embed_var)


def setup(client):
    client.add_cog(AdminCog(client))
