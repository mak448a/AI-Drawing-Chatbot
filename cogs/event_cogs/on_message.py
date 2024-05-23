import logging

from helper_utils.utils import config, FakeCtx, generate_message

from discord.ext import commands
from discord import app_commands


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(self.bot.user.id) not in message.content:
            return
        if not config["chatbot"]:
            return
        if message.author == self.bot.user:
            return

        cleaned_message = message.content.replace(f"<@{self.bot.user.id}>", "")

        async with message.channel.typing():
            msg = await generate_message(cleaned_message)

        msg1 = msg.split("<draw>")[0]

        # Check if the model wants to draw something
        if "<draw>" in msg:
            await message.channel.send(msg1)
        else:
            await message.channel.send(msg)

        if "<draw>" in msg and "</draw>" in msg:
            # Parse the draw tag
            prompt = msg.split("<draw>")[1].split("</draw>")[0]

            logging.debug(
                f"{message.author.mention} is generating ```{prompt}``` with "
                f"{config['image_model']}!"
            )

            await self.bot.get_cog(
                "Horde"
            ).imagine_horde(  # Get cog Horde (cogs/horde.py) and then call imagine_horde
                FakeCtx(message),  # NOQA
                prompt=prompt,
                model=app_commands.Choice(
                    name=config["image_model"], value=config["image_model"]
                ),
            )


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
