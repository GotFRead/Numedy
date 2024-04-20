
import asyncio
import service



async def main():
    await service.Service().start()

if __name__ == '__main__':
    asyncio.run(main())