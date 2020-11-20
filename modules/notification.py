import time
import datetime
import json

import pynotifier as pn


def notify_fn():
    while True:
        with open(r"data/all_reminds.json", "r") as ar:
            all_reminds = json.load(ar)["data"]

        current_date_and_time = datetime.datetime.now()
        current_time = f"{current_date_and_time.hour}:{current_date_and_time.minute}:{current_date_and_time.second}"
        current_date = f"{current_date_and_time.day}/{current_date_and_time.month}/{current_date_and_time.year}"

        for element in all_reminds:
            if (
                    element["date"] == current_date
                    and current_time == f"{element['time']}:0"
            ):
                if element["notification"]:
                    with open(r"data/all_reminds.json", "r+") as ar:
                        all_reminds2 = json.load(ar)
                        all_reminds2["data"].remove(element)

                        ar.seek(0)
                        ar.truncate(0)
                        json.dump(all_reminds2, ar, indent=4)

                    remind_notification = pn.Notification(
                        title=element["title"],
                        description=element["description"],
                        icon_path=r"data/img/notification-clock-icon.png",
                        duration=5,
                        urgency=pn.Notification.URGENCY_NORMAL,
                    )
                    remind_notification.send()

                    del all_reminds2

                    break
        time.sleep(1)

        del all_reminds