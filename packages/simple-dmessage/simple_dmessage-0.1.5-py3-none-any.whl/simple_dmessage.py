import discord


async def send_direct_message(token, user_id, message):
    intents = discord.Intents.default()
    async with discord.Client(intents=intents) as client:
        await client.login(token)
        user = await client.fetch_user(user_id)
        await user.send(message)
        # print(f"Direct message sent to user {user_id}: {message}")
