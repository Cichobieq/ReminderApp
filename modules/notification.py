import os
import time
import datetime
import json

import pynotifier as pn
from pydub import AudioSegment
from pydub.playback import play


def notify_fn():
    while True:
        with open(r"data/settings.json", "r") as s:
            settings_json = json.load(s)

        automatic_reminds_delete = settings_json["automatic_reminds_delete"]
        notification_sound = settings_json["notification_sound"]

        if notification_sound:
            sound_path = settings_json["sound_path"]

        with open(r"data/all_reminds.json", "r+") as ar:
            all_reminds = json.load(ar)["data"].copy()

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
                    remind_notification = pn.Notification(
                        title=element["title"],
                        description=element["description"],
                        icon_path=r"data/img/notification-clock-icon.png",
                        duration=5,
                        urgency=pn.Notification.URGENCY_NORMAL,
                    )
                    remind_notification.send()

                    with open(r"data/all_reminds.json") as s:
                        settings_json = json.load(s)

                        if automatic_reminds_delete:
                            del element

                    if notification_sound:
                        if os.path.exists(sound_path):
                            sound = AudioSegment.from_mp3(sound_path)
                            play(sound)
                        else:
                            print("Error while playing sound. Incorrect sound path.")

                    break
        time.sleep(1)