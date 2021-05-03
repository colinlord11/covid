import logging
from datetime import date, timedelta

from win10toast import ToastNotifier

from location import Location
from priority_area import PriorityArea
from vaccine_api import VaccineApi

########### Specify your search details here ###########
location = Location.CAREFIRST_SENIORS
priority_area = PriorityArea.ELIGIBLE_AGE_GROUPS
########################################################

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
toast = ToastNotifier()

# Run the script until an available slot is found
with VaccineApi() as vaccine_api:
    is_slots_found = False
    while not is_slots_found:
        today = date.today()
        # The website checks over the current date + the next 2 weeks, so this is what we'll do as well
        for i in range(1, 15):
            check_date = today + timedelta(days=i)
            available_slots = vaccine_api.find_available_slots(location, priority_area, check_date)
            if (available_slots != 0):
                is_slots_found = True
                found_message = f"{available_slots} slot(s) are available on {check_date}"
                logger.info(found_message)
                toast.show_toast("Vaccination Appointment Found!", found_message)
