import tkinter as tk
import json

import fonts


def hello_window():
    with open(r"data/info.json", "r+") as ps:
        status = json.load(ps)

        if status["status"] == "unused":
            # hello_window
            hello_window = tk.Tk()
            hello_window.title("Welcome")
            # hello_window.tk.call('wm', 'iconphoto', hello_window._w, const.ICON)
            hello_window.resizable(False, False)
            hello_window.eval(
                "tk::PlaceWindow %s center"
                % hello_window.winfo_pathname(hello_window.winfo_id())
            )

            hw_hello_label = tk.Label(
                master=hello_window,
                text="Welcome to reminder. Enjoy yourself :)",
                font=fonts.Calibri_30,
                padx=20,
                pady=20,
            ).pack()

            ok_button = tk.Button(
                master=hello_window,
                text="Ok!",
                font=fonts.Calibri_20,
                padx=350,
                pady=25,
                command=hello_window.destroy,
            ).pack()

            status["status"] = "used"
            ps.seek(0)
            ps.truncate(0)
            json.dump(status, ps)
