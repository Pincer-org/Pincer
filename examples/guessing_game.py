import random

from pincer import Client, command
from pincer.objects import Intents, MessageContext
from pincer.exceptions import TimeoutError

import logging
logging.basicConfig(level=logging.DEBUG)


class Bot(Client):

    @command(guild=881531065859190804)
    async def guess(self, ctx: MessageContext, biggest_number: int):

        await ctx.reply(f"Starting the guessing game! Pick a number between 0 and {biggest_number}.")
        channel = await self.get_channel(ctx.channel_id)
        number = random.randint(0, biggest_number)

        try:
            async for next_message, in self.loop_for('on_message', loop_timeout=60):
                if next_message.author.bot:
                    continue

                try:
                    guessed_number = int(next_message.content)
                except ValueError:
                    await channel.send(f"{next_message.content} is not a number. Try again!")
                    continue

                if guessed_number > number:
                    await channel.send("Number is too high!")
                elif guessed_number < number:
                    await channel.send("Number is too low!")
                else:
                    await next_message.react("🚀")
                    await channel.send("Number is correct!")
                    break

        except TimeoutError:
            await channel.send("You took too long! The game timed out.")


if __name__ == "__main__":
    bot = Bot("ODgxNTgzMzc5NTA0NTgyNzI3.YSu8gA.kUPT7OsIwGLH5MrAzLxI1px6wuY", intents=Intents.GUILD_MESSAGES)
    bot.run()
