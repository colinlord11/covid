import logging
import re
from datetime import date

import requests

from location import Location
from priority_area import PriorityArea

logger = logging.getLogger("vaccine_api")


class VaccineApi:
    def __request(self, command: str, url: str):
        """
        Utility method for requesting through FlareSolver's api.
        """
        return requests.post("http://localhost:8191/v1", json={
            "cmd": command,
            "url": url,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

    def __get(self, url: str):
        """
        Http GET method using FlareSolver's api.
        """
        return self.__request("request.get", url)

    def __sessions_create(self):
        self.__request("sessions.create", None)

    def __sessions_destroy(self):
        self.__request("sessions.destroy", None)

    def find_available_slots(self, location: Location, priority_area: PriorityArea, date: date):
        """
        Finds the available vaccination spots.

        Parameters
        ----------
        location : Location
            The user's location.
        priority_area: PriorityArea
            The user's priority group.
        date : Date
            The date to check for availability.
        Returns
        -------
        int
            The number of available slots.
        """
        logger.info(f"Searching for vaccination slots: {location}, {priority_area}, {date}")
        request = self.__get(f"https://nygh.vertoengage.com/engage/api/api/cac-open-clinic/v1/slots/availability?day={date}T00:00:00.000-04:00&location_id={location.value}&slot_type={priority_area.value}&key=455aadd5-1e1b-4078-88e2-e375f2531536")
        content = request.text[request.text.find("slots_left"):]
        slots_left = re.search(r'\d+', content).group()
        return int(slots_left)

    def __enter__(self):
        logger.info("Creating browser session")
        self.__sessions_create
        return self

    def __exit__(self, type, value, traceback):
        logger.info("Destroying browser session")
        self.__sessions_destroy
