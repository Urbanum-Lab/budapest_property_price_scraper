import asyncio
from proxybroker import Broker

ps = []


async def show(proxies):
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        ps.append(proxy)
        print('Found proxy: %s' % proxy)


proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTP', 'HTTPS'], limit=200),
    show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)

with open("src/utils/proxies.txt", "w") as outfile:
    for p in ps:
        outfile.write(p.host + ":" + str(p.port) + "\n")

print("We have proxies, yeaah!")
