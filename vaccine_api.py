import asyncio
import logging
import re
from datetime import date

import aiohttp

from location import Location
from priority_area import PriorityArea

logger = logging.getLogger("vaccine_api")

class VaccineApi:
    def __init__(self, location: Location, priority_area: PriorityArea, session: aiohttp.ClientSession):
        """
        Parameters
        ----------
        location : Location
            The user's location.
        priority_area: PriorityArea
            The user's priority group.
        """
        self.location = location
        self.priority_area = priority_area
        self.session = session

    async def __request(self, command: str, url: str) -> str:
        """
        Utility method for requesting through FlareSolver's api.
        """
        async with self.session.post("http://localhost:8191/v1", json={
            "cmd": command,
            "url": url,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }) as response:
            return await response.text()

    async def __get(self, url: str) -> str:
        """
        Http GET method using FlareSolver's api.
        """
        return await self.__request("request.get", url)

    async def __sessions_create(self) -> None:
        await self.__request("sessions.create", None)

    async def __sessions_destroy(self) -> None:
        await self.__request("sessions.destroy", None)

    async def find_available_slots(self, date: date) -> int:
        """
        Finds the available vaccination spots.

        Parameters
        ----------
        date : Date
            The date to check for availability.
        Returns
        -------
        int
            The number of available slots.
        """
        logger.info(f"Searching for vaccination slots: [{self.location}, {self.priority_area}, {date}]")
        url = f"https://nygh.vertoengage.com/engage/api/api/cac-open-clinic/v1/slots/availability?day={date}T00:00:00.000-04:00&location_id={self.location.value}&slot_type={self.priority_area.value}&key=455aadd5-1e1b-4078-88e2-e375f2531536"
        response = await self.__get(url)
        content = response[response.find("slots_left"):]
        slots_left = re.search(r'\d+', response[response.find("slots_left"):]).group()
        return int(slots_left)

    async def __aenter__(self):
        logger.info(f"Creating browser session for [{self.location}, {self.priority_area}]")
        await self.__sessions_create()
        return self

    async def __aexit__(self, *args):
        logger.info(f"Destroying browser session for [{self.location}, {self.priority_area}]")
        await self.__sessions_destroy()
