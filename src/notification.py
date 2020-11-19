import datetime
import json

import pynotifier as pn

def notify_fn():
    with open(r"data/all_reminds.json", "r+") as ar:
        all_reminds = json.load(ar)["data"]

    current_date_and_time = datetime.datetime.now()
    current_time = f"{current_date_and_time.hour}:{current_date_and_time.minute}"
    current_date = f"{current_date_and_time.day}/{current_date_and_time.month}/{current_date_and_time.year}"

    for element in all_reminds:
        if (
                element["date"] == current_date
                and element["time"] == current_time
                and f"{current_time}:0" == f"{current_time}:{current_date_and_time.second}"
        ):
            if element["notification"]:
                remind_notification = Notification(
                    title=element["title"],
                    description=element["description"],
                    icon_path=r"data/img/notification-clock-icon.png",
                    duration=5,
                    urgency=pn.Notification.URGENCY_NORMAL,
                )
                remind_notification.send()

                break
    time.sleep(1)