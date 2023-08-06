# Simple Message Bot

This bot is designed to send a custom direct message to a user on discord.

## Example

```python
import asyncio
from message import send_direct_message


async def my_script():
    # Your script code goes here
    await send_direct_message(TOKEN, USER_ID, "Hello, World!")


async def main():
    await my_script()

asyncio.run(main())

```

### Why
I wanted an easy way to get remote notfications from scripts 
