#!/home/ubuntu/python/queue_tel_bot/.venv/bin/python

import re
import asyncio
import json
import aiofiles
import aiohttp
import os
from queue_bot import settings


class Api:
    def __init__(self):
        self.headers = settings.headers

    async def _get_js_main(self):
        """
        Getting url a js file for futher token extraction

        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url="https://mon.declarant.by/") as resp:
                result = await resp.read()
                res = re.search(r'src="/ng[\w]*/main.[\w]*.js', result.decode("utf-8"))
                await asyncio.sleep(3)
                return "https://mon.declarant.by/" + res.group().split("/", 1)[1]
        
    async def _get_checkpoint_token(self):
        """
        Getting a token from a js file, for further use when getting statistics

        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            url = await self._get_js_main()
            async with session.get(url) as resp:
                result = await resp.read()
                res = re.search(r'this.token="[\w-]*"', result.decode("utf-8"))
                await asyncio.sleep(3)
                return res.group().split('"')[1]

    async def get_checkpoint(self):
        self._checkpoint_token = await self._get_checkpoint_token()
        url = f"https://belarusborder.by/info/checkpoint?token={self._checkpoint_token}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                response = await resp.json()
                if os.path.exists(settings.BASE_DIR / "checkpoint"):
                    async with aiofiles.open(
                        settings.BASE_DIR
                        / "checkpoint"
                        / "statistic"
                        / "checkpoint.json",
                        "w+",
                    ) as file:
                        await file.write(json.dumps(response, indent=2))
                else:
                    os.mkdir(settings.BASE_DIR / "checkpoint")
                    os.mkdir(settings.BASE_DIR / "checkpoint" / "statistic")
                    async with aiofiles.open(
                        settings.BASE_DIR
                        / "checkpoint"
                        / "statistic"
                        / "checkpoint.json",
                        "w+",
                    ) as file:
                        await file.write(json.dumps(response, indent=2))
        await asyncio.sleep(2)

    async def checkpoint_id(self):
        async with aiofiles.open(
            settings.BASE_DIR / "checkpoint" / "statistic" / "checkpoint.json", "r"
        ) as file:
            res = json.loads(await file.read())
            return list(
                {"id": checkpoint["id"], "name": checkpoint["name"]}
                for checkpoint in res["result"]
            )

    async def _get_token(self):
        """
        Return token for a request to receive a response about a checkpoint
        Temporary value test

        """
        token = "test"
        return token

    async def get_statistic(self):
        token = self._checkpoint_token
        for chec_id in await self.checkpoint_id():
            url = f"https://belarusborder.by/info/monitoring/statistics?token={token}&checkpointId={chec_id['id']}"
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as resp:
                    response = await resp.json()
                    async with aiofiles.open(
                        settings.BASE_DIR
                        / "checkpoint"
                        / "statistic"
                        / (chec_id["name"].lower() + ".json"),
                        "w+",
                    ) as file:
                        await file.write(json.dumps(response, indent=2))
            await asyncio.sleep(1)

    async def api_get(self):
        token = await self._get_token()
        for check_id in await self.checkpoint_id():
            url = f"https://belarusborder.by/info/monitoring-new?token={token}&checkpointId={check_id['id']}"
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as resp:
                    response = await resp.json()
                    file_name = response["info"]["name"].lower()
                    async with aiofiles.open(
                        settings.BASE_DIR / "checkpoint" / (file_name + ".json"), "w+"
                    ) as file:
                        await file.write(json.dumps(response, indent=2))
            await asyncio.sleep(1)


async def main():
    api = Api()
    await api.get_checkpoint()
    await api.api_get()
    await asyncio.sleep(5)
    await api.get_statistic()


asyncio.run(main())
