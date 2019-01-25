import json
import os

import requests
from pushbullet import Pushbullet

# contains a cache of the previous results
previous_result = {}

def septime(event, context):
    global previous_result
    result = do()
    # only notify when the results have changed
    if result != previous_result:
        previous_result = result
        if result["resas"]:
            print("Sending notification to pushbullet")
            send_to_pushbullet(json.dumps(result), os.environ.get("PUSHBULLET_API_KEY"))
        else:
            print("no available resa")


def do():
    main_url = "https://module.lafourchette.com/en_GB/resa/pick-pax/10889-d34ca/54499"
    print(main_url)
    nb_people_list = requests.get(url=main_url).json()["availableNbPeopleList"]
    options_pax = [2]
    available_nb_people = list(filter(lambda x: x.get("has_wait_list", 0) != 1 and x.get("nb_people", 0) in options_pax, nb_people_list))
    print(f"List of groups that have availabilities {available_nb_people}")

    results = []
    for pax in options_pax:
        resas = find_resa(pax)
        if resas:
            results.append({
                "pax": pax,
                "results": resas
            })

    return {
        # "list_available_people": available_nb_people,
        "resas": results
    }


def find_resa(pax):
    results = {}
    pick_date_url = f"https://module.lafourchette.com/en_GB/resa/pick-date/{pax}/10889-d34ca/54499"
    print(pick_date_url)
    pick_dates = requests.get(url=pick_date_url).json().get("availableDateList", [])
    print(f"Search for a party of {pax} people")
    dates = list(filter(lambda x: x != "", map(lambda x: x.get("date", ""), pick_dates)))
    print(f"Found dates: {dates}")
    for date in dates:
        print(f"Requesting for {date}...")
        query_date_url = f"https://module.lafourchette.com/en_GB/resa/pick-time/{pax}/{date}/10889-d34ca/54499"
        print(query_date_url)
        query_date = requests.get(url=query_date_url).json().get("availableTimeslotList", [])
        for slot in query_date:
            if slot.get("name", "") != "BREAKFAST":
                for timeslot in slot.get("timeslots", []):
                    time = timeslot.get("time", "N/A")
                    print(time)
                    if timeslot.get("sale_type_list", {}).get("hasWaitList", 0) != 1:
                        if (results.get(date, [])):
                            results[date].append(f"{time}")
                        else:
                            results[date] = [time]

    return results


def send_to_pushbullet(text, pushbullet_api_key):
    print(text)
    pb = Pushbullet(pushbullet_api_key)
    push = pb.push_note("Septime Booking!", text)


# to run locally
if __name__ == "__main__":
    septime(None, None)
