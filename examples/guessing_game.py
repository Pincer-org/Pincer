import random

from pincer import Client, command
from pincer.objects import Intents, MessageContext


class Bot(Client):

    @command()
    async def guess(self, ctx: MessageContext, biggest_number: int):

        await ctx.reply(f"Starting the guessing game! Picker a number between 0 and {biggest_number}.")
        channel = await self.get_channel(ctx.channel_id)
        number = random.randint(0, biggest_number)

        try:
            async for next_message, in self.loop_for('on_message'):
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
                    self.game_running = False

        except TimeoutError:
            channel.send("Game timed out")


if __name__ == "__main__":
    bot = Bot("XXXYOURBOTTOKENHEREXXX", intents=Intents.GUILD_MESSAGES)
    bot.run()
