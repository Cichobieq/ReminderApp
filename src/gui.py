#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# from subprocess import check_call
import threading
import time
import datetime
import json

from pynotifier import Notification
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkscrolledframe import ScrolledFrame

import notification
import fonts
import hello_window


class App:
    def __init__(self):
        root = tk.Tk()
        ICON = tk.PhotoImage(file=r"data/img/icon-clock.gif")

        root.title("Reminder")
        root.tk.call("wm", "iconphoto", root._w, ICON)
        root.resizable(False, False)
        root.eval(f"tk::PlaceWindow {root.winfo_pathname(root.winfo_id())} center")

        notify_thread = threading.Thread(target=notification.notify_fn)
        notify_thread.start()

        clock_label = tk.Label(
            master=root,
            text="",
            font=fonts.Calibri_30,
            padx=10, pady=10,
        )
        clock_label.grid(row=0, column=0)

        def clock_fn():
            while True:
                now = datetime.datetime.now()

                if now.second >= 10:
                    if now.minute >= 10:
                        clock_print = f"{now.hour}:{now.minute}:{now.second}"
                    else:
                        clock_print = f"{now.hour}:0{now.minute}:{now.second}"
                else:
                    if now.minute >= 10:
                        clock_print = f"{now.hour}:{now.minute}:0{now.second}"
                    else:
                        clock_print = f"{now.hour}:0{now.minute}:0{now.second}"

                clock_label["text"] = clock_print

                time.sleep(1)

        clock_thread = threading.Thread(target=clock_fn)
        clock_thread.start()

        date_label = tk.Label(
            master=root,
            text="",
            font=fonts.Calibri_30,
            padx=10, pady=10,
        )
        date_label.grid(row=0, column=1)

        def date_fn():
            while True:
                now = datetime.datetime.now()
                date_print = f"{now.day}.{now.month}.{now.year}"

                date_label["text"] = date_print

                time.sleep(1)

                date_fn()

        date_thread = threading.Thread(target=date_fn)
        date_thread.start()

        def show_reminds_fn():
            show_reminds_window = tk.Tk()
            show_reminds_window.title("Show reminds")
            show_reminds_window.resizable(False, False)
            show_reminds_window.eval(
                f"tk::PlaceWindow {show_reminds_window.winfo_pathname(show_reminds_window.winfo_id())} center"
            )

            show_label = tk.Label(
                master=show_reminds_window,
                text="Type your remind's title.",
                font=fonts.Calibri_30,
                padx=20,
                pady=5,
            )
            show_label.grid(row=0, column=0, columnspan=2)

            show_entry = tk.Entry(master=show_reminds_window, font=fonts.Calibri_15)
            show_entry.grid(row=1, column=0, ipadx=170, ipady=15, padx=10, pady=5)

            def show_button_fn():
                value_to_search = show_entry.get()
                show_entry.delete(0, tk.END)

                with open(r"data/all_reminds.json", "r") as ar:
                    all_reminds_loaded = json.load(ar)
                    all_reminds = all_reminds_loaded["data"].copy()

                    is_correct = False

                    for i in range(len(all_reminds)):
                        if value_to_search == all_reminds[i]["title"]:
                            searched_reminds_parameters = all_reminds[i]
                            is_correct = True
                            break

                    if is_correct:
                        final_show_window = tk.Tk()
                        final_show_window.title("Check titles")
                        final_show_window.resizable(False, False)
                        final_show_window.eval(
                            f"tk::PlaceWindow {final_show_window.winfo_pathname(final_show_window.winfo_id())} center"
                        )

                        title_label = tk.Label(
                            master=final_show_window,
                            text="Title: ",
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        title_label.grid(row=0, column=0)

                        remind_title_label = tk.Label(
                            master=final_show_window,
                            text=searched_reminds_parameters["title"],
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        remind_title_label.grid(row=0, column=1)

                        description_label = tk.Label(
                            master=final_show_window,
                            text="Description: ",
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        description_label.grid(row=1, column=0)

                        if searched_reminds_parameters["description"] != "":
                            remind_description_label = tk.Label(
                                master=final_show_window,
                                text=searched_reminds_parameters["description"],
                                font=fonts.Calibri_15,
                                padx=10,
                                pady=5,
                            )
                            remind_description_label.grid(row=1, column=1)
                        else:
                            remind_description_label2 = tk.Label(
                                master=final_show_window,
                                text="Empty",
                                font=fonts.Calibri_15,
                                padx=10,
                                pady=5,
                            )
                            remind_description_label2.grid(row=1, column=1)

                        date_label = tk.Label(
                            master=final_show_window,
                            text="Date: ",
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        date_label.grid(row=2, column=0)

                        remind_date_label = tk.Label(
                            master=final_show_window,
                            text=searched_reminds_parameters["date"],
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        remind_date_label.grid(row=2, column=1)

                        time_label = tk.Label(
                            master=final_show_window,
                            text="Time: ",
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        time_label.grid(row=3, column=0)

                        remind_time_label = tk.Label(
                            master=final_show_window,
                            text=searched_reminds_parameters["time"],
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        remind_time_label.grid(row=3, column=1)

                        notification_label = tk.Label(
                            master=final_show_window,
                            text="Notification: ",
                            font=fonts.Calibri_15,
                            padx=10,
                            pady=5,
                        )
                        notification_label.grid(row=4, column=0)

                        if searched_reminds_parameters["notification"]:
                            remind_notification_label = tk.Label(
                                master=final_show_window,
                                text="Yes",
                                font=fonts.Calibri_15,
                                padx=10,
                                pady=5,
                            )
                            remind_notification_label.grid(row=4, column=1)
                        else:
                            remind_notification_label = tk.Label(
                                master=final_show_window,
                                text="No",
                                font=fonts.Calibri_15,
                                padx=10,
                                pady=5,
                            )
                            remind_notification_label.grid(row=4, column=1)

                        close_button = tk.Button(
                            master=final_show_window,
                            text="Close",
                            font=fonts.Calibri_20,
                            command=final_show_window.destroy,
                        )
                        close_button.grid(row=5, column=0, columnspan=2, ipadx=100, ipady=20, padx=10, pady=5)

                    else:
                        print("Title is incorrect.")

                        incorrect_label = tk.Label(
                            master=show_reminds_window,
                            text="Incorrect title",
                            font=fonts.Calibri_15,
                            fg="red",
                            pady=10,
                        )
                        incorrect_label.grid(row=4, column=0, columnspan=2)

            show_button = tk.Button(
                master=show_reminds_window,
                text="Show",
                font=fonts.Calibri_15,
                relief=tk.GROOVE,
                command=show_button_fn,
            )
            show_button.grid(row=1, column=1, padx=10)

            show_label2 = tk.Label(
                master=show_reminds_window,
                text="To check all reminds' titles click button below.",
                font=fonts.Calibri_15,
                padx=20,
                pady=10,
            )
            show_label2.grid(row=2, column=0, columnspan=2)

            def check_titles_fn():
                show_titles_window = tk.Tk()
                show_titles_window.title("Check titles")
                show_titles_window.resizable(False, False)
                show_titles_window.eval(
                    f"tk::PlaceWindow {show_titles_window.winfo_pathname(show_titles_window.winfo_id())} center"
                )

                with open(r"data/all_reminds.json", "r") as ar:
                    all_reminds = json.load(ar)
                    list_of_titles = []

                    for i in range(len(all_reminds["data"])):
                        list_of_titles.append(all_reminds["data"][i]["title"])

                    sf = ScrolledFrame(show_titles_window, width=170, height=150)
                    sf.pack(side="top", expand=1, fill="y")

                    sf.bind_arrow_keys(show_titles_window)
                    sf.bind_scroll_wheel(show_titles_window)

                    scroll_frame = sf.display_widget(tk.Frame)

                    for i in range(len(list_of_titles)):
                        current_title = list_of_titles[i]
                        title_label = tk.Label(
                            master=scroll_frame,
                            text=current_title,
                            font=fonts.Calibri_20,
                            padx=10,
                        )
                        title_label.grid(row=i, column=1, pady=5)

            check_titles_button = tk.Button(
                master=show_reminds_window,
                text="Check titles",
                font=fonts.Calibri_15,
                relief=tk.GROOVE,
                command=check_titles_fn,
            )
            check_titles_button.grid(row=3, column=0, ipadx=200, ipady=20, padx=10, pady=5, columnspan=2)

        show_reminds_button = tk.Button(
            master=root,
            text="Show reminds",
            font=fonts.Calibri_15,
            relief=tk.GROOVE,
            command=show_reminds_fn,
        )
        show_reminds_button.grid(row=1, column=0, padx=10, pady=5, ipadx=206, ipady=15, columnspan=2)

        def add_remind():
            add_remind_window = tk.Tk()
            add_remind_window.title("Add remind")
            add_remind_window.resizable(False, False)
            add_remind_window.eval(
                f"tk::PlaceWindow {add_remind_window.winfo_pathname(add_remind_window.winfo_id())} center"
            )

            start_label = tk.Label(
                master=add_remind_window,
                text="Type your remind parameters below:",
                font=fonts.Calibri_30,
                padx=10,
                pady=10,
            )
            start_label.grid(row=0, column=0, columnspan=2)

            title_label = tk.Label(
                master=add_remind_window,
                text="Title:",
                font=fonts.Calibri_15,
                justify=tk.RIGHT,
            )
            title_label.grid(row=1, column=0)

            title_entry = tk.Entry(master=add_remind_window, font=fonts.Calibri_15)
            title_entry.grid(row=1, column=1, ipadx=240, ipady=9)

            description_label = tk.Label(
                master=add_remind_window,
                text="Description:",
                font=fonts.Calibri_15,
                justify=tk.RIGHT,
                padx=5,
            )
            description_label.grid(row=2, column=0)

            description_entry = tk.Entry(master=add_remind_window, font=fonts.Calibri_15)
            description_entry.grid(row=2, column=1, ipadx=240, ipady=9)

            date_label = tk.Label(
                master=add_remind_window,
                text="Date (f.e. 14/7/2020):",
                font=fonts.Calibri_15,
                justify=tk.RIGHT,
                padx=5,
            )
            date_label.grid(row=3, column=0)

            date_entry = tk.Entry(master=add_remind_window, font=fonts.Calibri_15)
            date_entry.grid(row=3, column=1, ipadx=240, ipady=9)

            time_label = tk.Label(
                master=add_remind_window,
                text="Time (f.e. 15:00):",
                font=fonts.Calibri_15,
                justify=tk.RIGHT,
                padx=5,
            )
            time_label.grid(row=4, column=0)

            time_entry = tk.Entry(master=add_remind_window, font=fonts.Calibri_15)
            time_entry.grid(row=4, column=1, ipadx=240, ipady=9)

            notification_label = tk.Label(
                master=add_remind_window,
                text="Notification (type yes or no):",
                font=fonts.Calibri_15,
                justify=tk.RIGHT,
                padx=5,
            )
            notification_label.grid(row=5, column=0)

            notification_entry = tk.Entry(
                master=add_remind_window, font=fonts.Calibri_15
            )
            notification_entry.grid(row=5, column=1, ipadx=240, ipady=6)

            def else_fn():
                print("Type correct parameters.")

                error_label = tk.Label(
                    master=add_remind_window,
                    text="Type correct parameters.",
                    font=fonts.Calibri_15,
                    foreground="red",
                )
                error_label.grid(row=7, column=0, columnspan=2)

            def add_remind_fn():
                TITLE = title_entry.get()
                DESCRIPTION = description_entry.get()
                DATE = date_entry.get()
                TIME = time_entry.get()
                notification = notification_entry.get()

                with open(r"data/reminds_number.json", "r+") as rn:
                    reminds_number = json.load(rn)

                    with open(r"data/all_reminds.json", "r+") as rm:
                        all_reminds = json.load(rm)

                        if (
                            TITLE != ""
                            and DATE != ""
                            and TIME != ""
                            and notification != ""
                            and TITLE != " "
                            and DATE != " "
                            and TIME != " "
                        ):
                            if (
                                notification.lower() == "yes"
                                or notification.lower() == "no"
                            ):
                                try:
                                    if datetime.datetime.strptime(
                                        DATE, "%d/%m/%Y"
                                    ) and datetime.datetime.strptime(TIME, "%H:%M"):
                                        if (
                                            notification == "yes"
                                            or notification == "Yes"
                                        ):
                                            NOTIFICATION_MODIFIED = True
                                        elif (
                                            notification == "no" or notification == "No"
                                        ):
                                            NOTIFICATION_MODIFIED = False

                                        remind_content = {
                                            "title": TITLE,
                                            "description": DESCRIPTION,
                                            "date": DATE,
                                            "time": TIME,
                                            "notification": NOTIFICATION_MODIFIED,
                                        }

                                        rm.seek(0)
                                        rm.truncate(0)

                                        final_dict = all_reminds.copy()
                                        final_dict["data"].append(remind_content)

                                        json.dump(final_dict, rm, indent=4)

                                        new_number = str(
                                            int(reminds_number["number"]) + 1
                                        )

                                        rn.seek(0)
                                        rn.truncate(0)
                                        json.dump({"number": new_number}, rn, indent=4)

                                        add_remind_window.destroy()
                                    else:
                                        else_fn()
                                except ValueError:
                                    else_fn()
                            else:
                                else_fn()
                        else:
                            else_fn()

            final_add_remind_button = tk.Button(
                master=add_remind_window,
                text="Add remind",
                font=fonts.Calibri_15,
                relief=tk.GROOVE,
                command=add_remind_fn,
            )
            final_add_remind_button.grid(row=6, column=0, ipadx=240, ipady=6, pady=5, columnspan=2)

        add_remind_button = tk.Button(
            master=root,
            text="Add remind",
            font=fonts.Calibri_15,
            relief=tk.GROOVE,
            command=add_remind,
        )
        add_remind_button.grid(row=2, column=0, padx=10, pady=5, ipadx=219, ipady=15, columnspan=2)

        def remove_remind():
            remove_reminds_window = tk.Tk()
            remove_reminds_window.title("Show reminds")
            remove_reminds_window.resizable(False, False)
            remove_reminds_window.eval(
                f"tk::PlaceWindow {remove_reminds_window.winfo_pathname(remove_reminds_window.winfo_id())} center"
            )

            remove_label = tk.Label(
                master=remove_reminds_window,
                text="Type your remind's index.",
                font=fonts.Calibri_30,
                padx=20,
                pady=5,
            )
            remove_label.grid(row=0, column=0, columnspan=2)

            remove_entry = tk.Entry(master=remove_reminds_window, font=fonts.Calibri_15)
            remove_entry.grid(row=1, column=0, ipadx=170, ipady=15, padx=10, pady=5)

            def remove_button_fn():
                value_to_search = remove_entry.get()
                remove_entry.delete(0, tk.END)

                is_correct = False

                with open(r"data/all_reminds.json", "r+") as ar:
                    if value_to_search.isdecimal():
                        all_reminds_loaded = json.load(ar)
                        print(all_reminds_loaded)
                        data_reminds_loaded_len = len(all_reminds_loaded["data"])

                        for i in range(data_reminds_loaded_len):
                            if int(value_to_search) == i:
                                is_correct = True
                                break
                    else:
                        incorrect_label = tk.Label(
                            master=remove_reminds_window,
                            text="Index can't be a letter.",
                            font=fonts.Calibri_15,
                            fg="red",
                            pady=10,
                        )
                        incorrect_label.grid(row=4, column=0, columnspan=2)

                        print("Index can't be a letter.")

                    if is_correct:
                        if value_to_search.isdecimal():
                            updated_reminds = all_reminds_loaded.copy()
                            index_to_remove = int(value_to_search) - 1
                            updated_reminds["data"].pop(index_to_remove)

                            ar.seek(0)
                            ar.truncate(0)
                            json.dump(updated_reminds, ar, indent=4)

                            print("Your remind has been removed")
                            remove_reminds_window.destroy()
                        else:
                            incorrect_label = tk.Label(
                                master=remove_reminds_window,
                                text="Incorrect index.",
                                font=fonts.Calibri_15,
                                fg="red",
                                pady=10,
                            )
                            incorrect_label.grid(row=4, column=0, columnspan=2)
                    else:
                        incorrect_label = tk.Label(
                            master=remove_reminds_window,
                            text="Incorrect index.",
                            font=fonts.Calibri_15,
                            fg="red",
                            pady=10,
                        )
                        incorrect_label.grid(row=4, column=0, columnspan=2)

                        print("Incorrect index.")

            remove_button = tk.Button(
                master=remove_reminds_window,
                text="Remove",
                font=fonts.Calibri_15,
                relief=tk.GROOVE,
                command=remove_button_fn,
            )
            remove_button.grid(row=1, column=1, padx=10)

            remove_label2 = tk.Label(
                master=remove_reminds_window,
                text="To check all reminds' titles and indexes click button below.",
                font=fonts.Calibri_15,
                padx=20,
                pady=10,
            )
            remove_label2.grid(row=2, column=0, columnspan=2)

            def check_titles_fn():
                show_titles_window = tk.Tk()
                show_titles_window.title("Check titles")
                show_titles_window.resizable(False, False)
                show_titles_window.eval(
                    f"tk::PlaceWindow {show_titles_window.winfo_pathname(show_titles_window.winfo_id())} center"
                )

                with open(r"data/all_reminds.json", "r") as ar:
                    all_reminds = json.load(ar)
                    list_of_titles = []

                    for i in range(len(all_reminds["data"])):
                        list_of_titles.append(all_reminds["data"][i]["title"])

                    sf = ScrolledFrame(show_titles_window, width=170, height=150)
                    sf.pack(side="top", expand=1, fill="y")

                    sf.bind_arrow_keys(show_titles_window)
                    sf.bind_scroll_wheel(show_titles_window)

                    scroll_frame = sf.display_widget(tk.Frame)

                    for i in range(len(list_of_titles)):
                        current_title = list_of_titles[i]

                        title_label = tk.Label(
                            master=scroll_frame,
                            text=f"{i}. {current_title}",
                            font=fonts.Calibri_15,
                            padx=10,
                        )
                        title_label.grid(row=i, column=1, pady=5)

            check_titles_button = tk.Button(
                master=remove_reminds_window,
                text="Check titles and indexes",
                font=fonts.Calibri_15,
                relief=tk.GROOVE,
                command=check_titles_fn,
            )
            check_titles_button.grid(row=3, column=0, ipadx=200, ipady=20, padx=10, pady=5, columnspan=2)

        show_reminds_button = tk.Button(
            master=root,
            text="Show reminds",
            font=fonts.Calibri_15,
            relief=tk.GROOVE,
            command=show_reminds_fn,
        )
        show_reminds_button.grid(row=1, column=0, padx=10, pady=5, ipadx=206, ipady=15, columnspan=2)

        remove_remind_button = tk.Button(
            master=root,
            text="Remove remind",
            font=fonts.Calibri_15,
            relief=tk.GROOVE,
            command=remove_remind,
        )
        remove_remind_button.grid(row=3, column=0, padx=10, pady=5, ipadx=200, ipady=15, columnspan=2)

        def settings():
            pass

        settings_button = tk.Button(
            master=root,
            text="Settings",
            font=fonts.Calibri_15,
            relief=tk.GROOVE,
            command=settings,
        )
        settings_button.grid(row=4, column=0, padx=10, pady=5, ipadx=235, ipady=15, columnspan=2)

        def about():
            pass

        about_button = tk.Button(
            master=root,
            text="About",
            font=fonts.Calibri_15,
            relief=tk.GROOVE,
            command=remove_remind,
        )
        about_button.grid(row=5, column=0, padx=10, pady=5, ipadx=246, ipady=15, columnspan=2)

        hello_window.hello_window()

        root.mainloop()