import random

from pincer import Client, command
from pincer.objects import Intents, MessageContext
from pincer.exceptions import TimeoutError


class Bot(Client):

    @command()
    async def guess(self, ctx: MessageContext, biggest_number: int):

        await ctx.reply(f"Starting the guessing game! Pick a number between 0 and {biggest_number}.")
        channel = await self.get_channel(ctx.channel_id)
        number = random.randint(0, biggest_number)

        try:
            async for next_message, in self.loop_for('on_message', loop_timeout=60):
                if next_message.author.bot:
                    continue

                if not next_message.content.isdigit():
                    await channel.send(f"{next_message.content} is not a number. Try again!")
                    continue

                guessed_number = int(next_message.content)

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
    bot = Bot("XXXYOURBOTTOKENHEREXXX", intents=Intents.GUILD_MESSAGES)
    bot.run()
