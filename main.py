import asyncio
import logging
from datetime import date, timedelta

import aiohttp
from win10toast import ToastNotifier

from location import Location
from priority_area import PriorityArea
from vaccine_api import VaccineApi

############################# Specify your search details here #############################
locations = [Location.CAREFIRST_SENIORS, Location.CENTENNIAL_COLLEGE]
priority_areas = [PriorityArea.ELIGIBLE_AGE_GROUPS, PriorityArea.TRANSPLANT_AND_CHEMOTHERAPY_RECIPIENTS]
############################################################################################

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
toast = ToastNotifier()

async def run_script(location, priority_area):
    async with aiohttp.ClientSession() as session:
        async with VaccineApi(location, priority_area, session) as api:
            is_slots_found = False
            while not is_slots_found:
                today = date.today()
                for i in range(1, 15):
                    check_date = today + timedelta(days=i)
                    available_slots = await api.find_available_slots(check_date)
                    if (available_slots != 0):
                        is_slots_found = True
                        found_message = f"{available_slots} slot(s) are available on {check_date} at {location} for {priority_area}"
                        logger.info(found_message)
                        toast.show_toast("Vaccination Appointment Found!", found_message, duration=30, threaded=True)
                        break

async def main():
    tasks = [asyncio.create_task(run_script(location, priority_area)) for location in locations for priority_area in priority_areas]
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

asyncio.run(main())
