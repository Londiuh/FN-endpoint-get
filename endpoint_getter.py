import aiohttp
import json
import random
import string
import crayons
import aiofiles
import aioconsole
import asyncio
import sys


ACCESS_TOKEN = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
# By default this is the iOS client_id & secret, if you want to change the client, you can generate one
# from https://github.com/MixV2/EpicResearch/blob/master/docs/auth/auth_clients.md.


async def get_token() -> str:
    auth_code = await aioconsole.ainput(crayons.magenta("Insert auth code: "))

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method="POST",
            url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"basic {ACCESS_TOKEN}"
            },
            data={
                "grant_type": "authorization_code",
                "code": auth_code
            }
        ) as r:
            response = await r.json()

    if "access_token" in response:
        print(crayons.green(f"Token: {response['access_token']}\nExpires at: {response['expires_at']}."))
        return response['access_token']
    elif "errorCode" in response:
        print(crayons.red(f"[ERROR] {response['errorCode']}"))
    else:
        print(crayons.red("[ERROR] Unknown error."))

    sys.exit()


async def get_endpoint(token: str):

    if token:
        endpoint = await aioconsole.ainput(crayons.magenta("Insert endpoint: "))
    else:
        return

    if 'epicgames.com' not in endpoint:
        print(crayons.red("[ERROR] Invalid endpoint, please insert a valid Fortnite endpoint."))
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method="GET",
                    url=endpoint,
                    headers={
                        "Authorization": f"bearer {token}"
                    }
            ) as r:
                response = await r.json()
    except aiohttp.ClientConnectorError as epic_error:
        print(crayons.red(f"[ERROR] Something went wrong: {epic_error}"))
        return

    print(json.dumps(response, sort_keys=False, indent=4))

    save_file = await aioconsole.ainput(crayons.cyan("Do you want to save the response into a json file? (Y/N): "))
    if 'y' in save_file.lower():
        name = f'{endpoint.split("/")[-1]}-{random.randint(1, 999)}'

        async with aiofiles.open(f'{name}.json', mode='r') as f:
            await f.write(json.dumps(response, sort_keys=False, indent=4))

        print(crayons.yellow(f"File successfully saved (./{name}.json)"))


async def main():
    token = await get_token()
    while True:
        await get_endpoint(token=token)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()