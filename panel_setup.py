
import asyncio
import httpx
from dotenv import load_dotenv
import os

load_dotenv()


PANEL_LOGIN = os.getenv("PANEL_LOGIN")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD")
PANEL_PORT = os.getenv("PANEL_PORT")
PANEL_PATH = os.getenv("PANEL_PATH")

if PANEL_LOGIN is None \
        or PANEL_PASSWORD is None \
        or PANEL_PORT is None \
        or PANEL_PATH is None:
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
                  "newUsername": PANEL_LOGIN,
                  "newPassword": PANEL_PASSWORD
                  }
        )
        print(resp.json())
        print("----------------------")

        resp = await client.post(
            PANEL_URL + "login",
            json={"username": PANEL_LOGIN, "password": PANEL_PASSWORD},
        )
        resp.raise_for_status()
        print(resp.json())
        print("----------------------")

        resp = await client.post(PANEL_URL + "panel/setting/all")
        print(resp.json())
        print("----------------------")
        settings = resp.json()["obj"]

        settings["webBasePath"] = f"/{PANEL_PATH}/"
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
