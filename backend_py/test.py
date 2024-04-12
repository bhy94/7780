import asyncio
import aiomysql

async def main():
    loop = asyncio.get_running_loop()
    await asyncio.sleep(1000)

asyncio.run(main())