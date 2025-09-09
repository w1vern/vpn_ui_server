
import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
PANEL_PORT = os.getenv("PANEL_PORT")
WEB_PATH = os.getenv("WEB_PATH")

if LOGIN is None \
        or PASSWORD is None \
        or PANEL_PORT is None \
        or WEB_PATH is None:
    raise Exception("Missing environment variables")

PANEL_PORT = int(PANEL_PORT)


async def main() -> None:
    PANEL_URL = f"http://3x-ui:2053/"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            PANEL_URL + "login",
            json={"username": "admin", "password": "admin"},
        )
        resp.raise_for_status()
        print(resp.json())
        print("----------------------")

        resp = await client.post(
            PANEL_URL + "panel/setting/updateUser",
            json={"oldUsername": "admin",
                  "oldPassword": "admin",
                  "newUsername": LOGIN,
                  "newPassword": PASSWORD
                  }
        )
        print(resp.json())
        print("----------------------")

        resp = await client.post(
            PANEL_URL + "login",
            json={"username": LOGIN, "password": PASSWORD},
        )
        resp.raise_for_status()
        print(resp.json())
        print("----------------------")

        resp = await client.post(PANEL_URL + "panel/setting/all")
        print(resp.json())
        print("----------------------")
        settings = resp.json()["obj"]

        settings["webBasePath"] = f"/{WEB_PATH}/"
        settings["webPort"] = PANEL_PORT
        resp = await client.post(
            PANEL_URL + "panel/setting/update",
            json=settings,
        )
        print(resp.json())
        print("----------------------")

        resp = await client.post(PANEL_URL + "panel/setting/all")
        print(resp.json())
        print("----------------------")

        resp = await client.post(
            PANEL_URL + "panel/setting/restartPanel"
        )
        print(resp.json())
        print("----------------------")

    print("All done")


if __name__ == "__main__":
    asyncio.run(main())
