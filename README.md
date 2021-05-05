# Scarborough Vaccine Checker

[Vaccinations](https://www.scarboroughcovidvaccineclinic.ca/) are finally available in Scarborough!  
Unfortunately, spots are currently limited and you'll find yourself refreshing the page quite often to snag a spot.

## Why use this script?

If you're lazy and would rather run a program to check for spots in the background, you're in luck!  
This simple script will continuously check for available slots through the website's internal api.  
As soon as a slot is found, the program will stop and notify you the # of available slots.

[![Script result example](https://i.gyazo.com/05471b176790e243649389f22457d191.gif)](https://gyazo.com/05471b176790e243649389f22457d191)

## Requirements

To run the script, you'll need to install the following:
- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)

## Python Dependencies

This script depends on [asyncio](https://pypi.org/project/asyncio/) and [win10toast](https://pypi.org/project/win10toast/). To install them, enter the following:

```
pip install asyncio
pip install win10toast
```

## FlareSolverr

In order to bypass the internal api's bot protection, this script runs requests through [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr).  
To install this, enter the following command:

```
docker run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
```

## Configuration

Before running the script, specify the location and priority areas you'd like to search for in [main.py](https://github.com/qwbarch/scarborough-vaccine-checker/blob/688c4c49320d38cf07bec9c10ae6546f2b110d7c/main.py#L12)

| Location                      |
|-------------------------------|
| SHN_CENTENARY_HOSPITAL        |
| CENTENNIAL_COLLEGE            |
| CAREFIRST_SENIORS             |
| SCARBOROUGH_CENTRE            |
| TAIBU_COMMUNITY_HEALTH_CENTRE |

| PriorityArea                               |
|--------------------------------------------|
| CENTENNIAL_COLLEGE                         |
| ELIGIBLE_AGE_GROUPS                        |
| ADULT_RECIPIENTS_OF_CHRONIC_HOME_CAREFIRST |
| INDIGENOUS_ADULT                           |
| PRIORITY_HEALTHCARE_WORKERS                |
| FAITH_LEADERS                              |
| PEOPLE_WITH_HEALTH_CONDITIONS              |
| EDUCATION_WORKERS                          |
| TRANSPLANT_AND_CHEMOTHERAPY_RECIPIENTS     |

## Running the script

In order to start the script, enter the following command:
```
py main.py
```
This will keep running until a slot is found, which will then halt the script and display a notification.

## It's requesting too fast! How do I slow it down?

You may notice that it doesn't truly wait for the amount of seconds you specified in between each request.  
Each **location** and **priority area** spawns up a new browser session on **FlareSolver**.  
The script only waits in between each request for that browser session.  
To slow it down, simply increase the value in [search_delay_seconds](https://github.com/qwbarch/scarborough-vaccine-checker/blob/9fd9a4ad8ad9df53c24a42bb9b70a30a13efdc42/main.py#L15) until you feel satisfied.  

Note: I do not recommend leaving the delay at 0, you're asking to be rate limited or potentially banned by their api for abusing it.

## Limitations

Notification toasts requires **Windows 10** to function properly, usiong the **win10toast** library.
Everything else should work fine on any other OS.

## What are these errors I'm seeing?

Make sure docker is running and **FlareSolver** is active.  
If you're still receiving errors, their website's internal api has likely changed and this script will need to be updated.
