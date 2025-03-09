import discord
import os
from openai import OpenAI

token = os.getenv("SECRET_KEY")#secret hai mai kyu btauu??? 

#OPEN AI ke CREDITS KHATAM HOGAY open router ko utha liya free mai bahut models deta yeh 
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("open_ai_key"),
)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if self.user != message.author and self.user in message.mentions:
            try:
                completion = openai_client.chat.completions.create(
                    model="google/gemini-2.0-flash-lite-preview-02-05:free",  # aur koi bi daal skta hu lekin free wala 
                    messages=[{"role": "user", "content": message.content}]
                )

                response = completion.choices[0].message.content[:2000] # discord message limit is 2000 characters

                if response:  # response mila ya nhi
                    await message.channel.send(response)
                else:
                    await message.channel.send("I didn't get a response. Try again!")

            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send("Oops! Something went wrong while processing your request.")

# bot ko set kr diya
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
