
import asyncio
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

PANEL_LOGIN = os.getenv("PANEL_LOGIN")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD")

if PANEL_LOGIN is None \
        or PANEL_PASSWORD is None:
    raise Exception("Missing environment variables")


async def main() -> None:
    PANEL_URL = f"http://3x-ui:2053/"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            PANEL_URL + "login",
            json={"username": "admin", "password": "admin"},
        )
        resp.raise_for_status()

        resp = await client.post(
            PANEL_URL + "panel/setting/updateUser",
            json={"oldUsername": "admin",
                  "oldPassword": "admin",
                  "newUsername": PANEL_LOGIN,
                  "newPassword": PANEL_PASSWORD
                  }
        )

        resp = await client.post(
            PANEL_URL + "login",
            json={"username": PANEL_LOGIN, "password": PANEL_PASSWORD},
        )
        resp.raise_for_status()
        if not resp.json()["success"]:
            raise Exception("Something went wrong")

    print("All done")


if __name__ == "__main__":
    asyncio.run(main())
