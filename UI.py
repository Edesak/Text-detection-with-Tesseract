import threading
from tkinter import filedialog

import customtkinter as tk
from screeninfo import get_monitors

import core
from DragAndMark import NewWindow
import json


class UI:
    def __init__(self):
        self.threshold_slider_min = None
        self.threshold_slider_max = None
        self.detection_text_panel = None
        self.detect_text_info = None
        self.running_thread_test_detect = None
        self.height_slider = None
        self.width_slider = None
        self.y_slider = None
        self.x_slider = None
        self.file_path = None
        self.running_thread = None
        self.running_thread_detect = None
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.root = tk.CTk()
        self.values = {'x': 0,
                       'y': 0,
                       'width': 0,
                       'height': 0}
        self.total_height = 0
        self.total_width = 0
        self.get_total_resolution()
        self.IsDragandMarkable = True
        self.threshold_value_min = 170
        self.threshold_value_max = 255
        self.blur_value = 2
        self.detection_text = "byl jsi zabit"

    def get_total_resolution(self):

        width = 0
        height = 0
        for monitor in get_monitors():
            width += monitor.width
            height += monitor.height
        self.total_height, self.total_width = height, width

    def validate_input(self, new_value):
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False

    def slider(self, x, value):
        # print(int(x))
        value.delete(0, tk.END)
        value.insert(0, str(int(x)))

    def update_values(self, *args):
        if len(args) == 0:
            self.values_core(self.x.get(), self.y.get(), self.width.get(), self.height.get())

        if len(args) == 4:
            self.IsDragandMarkable = True
            start_x, start_y, end_x, end_y = args
            w = start_x - end_x
            h = start_y - end_y
            w = abs(w)
            h = abs(h)

            self.values_core(start_x, start_y, w, h)
            self.update_UI_numbers()

        else:
            pass

    def values_core(self, x, y, w, h):
        self.values['x'] = x
        self.values['y'] = y
        self.values['width'] = w
        self.values['height'] = h

    def check_roi(self):
        thread = threading.Thread(target=self.thrd_check_roi, daemon=True)
        thread.start()

    def thrd_check_roi(self):
        self.update_values()
        core.check_ROI(self.values['x'], self.values['y'], self.values['width'], self.values['height'], self)

    def thrd_start_roi(self):
        self.update_values()
        core.start_detection(self.values['x'], self.values['y'], self.values['width'], self.values['height'], self,
                             self.file_path)

    def thrd_start_test_roi(self):
        self.update_values()
        core.start_test_detection(self.values['x'], self.values['y'], self.values['width'], self.values['height'], self)

    def edit_switch(self):
        if self.switch.get() == 0:
            self.stop_thread()
        else:
            self.start_thread()

    def start_switch(self):
        if self.switch_start.get() == 0:
            self.stop_thread_detec()
        else:
            self.start_thread_detec()

    def start_test_switch(self):
        if self.switch_test_detection.get() == 0:
            self.stop_thread_test_detec()
        else:
            self.start_thread_test_detec()

    def start_thread(self):
        self.running_thread
        self.running_thread = threading.Thread(target=self.thrd_check_roi, daemon=True)
        self.running_thread.start()

    def stop_thread(self):
        self.running_thread
        self.running_thread.do_run = False

    def start_thread_detec(self):
        self.running_thread_detect
        self.running_thread_detect = threading.Thread(target=self.thrd_start_roi, daemon=True)
        self.running_thread_detect.start()

    def stop_thread_detec(self):
        self.running_thread_detect
        self.running_thread_detect.do_run = False

    def start_thread_test_detec(self):
        self.running_thread_test_detect
        self.running_thread_test_detect = threading.Thread(target=self.thrd_start_test_roi, daemon=True)
        self.running_thread_test_detect.start()

    def stop_thread_test_detec(self):
        self.running_thread_test_detect
        self.running_thread_test_detect.do_run = False

    def upload_file(self):
        self.file_path = filedialog.askopenfilename()
        # Do something with the selected file path
        print("Selected file:", self.file_path)

    def creating_new_window(self):
        if self.IsDragandMarkable:
            second_window = NewWindow(self.update_values)
            self.IsDragandMarkable = False
        else:
            pass

        # second_window.title("Second Window")

    def update_min_thresh(self, x):
        self.threshold_value_min = int(x)
        self.threshold_slider_min.set(self.threshold_value_min)
        # print(self.threshold_value_min)

    def update_max_thresh(self, x):
        self.threshold_value_max = int(x)
        self.threshold_slider_max.set(self.threshold_value_max)
        # print(self.threshold_value_max)

    def on_entry_change(self,*args):
        # Get the current value from the StringVar
        entry_text = self.detection_text_panel.get()

        # Do something with the updated text
        self.detection_text = entry_text

    def update_blur(self):
        self.blur_value = self.blur.get()

    def update_UI_numbers(self):
        self.x.delete(0, tk.END)
        self.y.delete(0, tk.END)
        self.width.delete(0, tk.END)
        self.height.delete(0, tk.END)
        self.detection_text_panel.delete(0, tk.END)
        self.x_slider.set(self.values["x"])
        self.y_slider.set(self.values["y"])
        self.height_slider.set(self.values["width"])
        self.width_slider.set(self.values["height"])
        
        self.x.insert(0, str(self.values["x"]))
        self.y.insert(0, str(self.values["y"]))
        self.width.insert(0, str(self.values["width"]))
        self.height.insert(0, str(self.values["height"]))
        self.detection_text_panel.insert(0,str(self.detection_text))

    def save_settings(self):
        self.update_values()
        # Save variables to a file
        with open("saved_config.txt", "w") as file:
            file.write(f"values={self.values}\n")
            file.write(f"thr_v_min={self.threshold_value_min}\n")
            file.write(f"thr_v_max={self.threshold_value_max}\n")
            file.write(f"text_detection={self.detection_text}\n")

    def load_settings(self):
        loaded_data = {}
        with open("saved_config.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                loaded_data[key] = value

            value_string = loaded_data["values"]
            # Replace single quotes with double quotes
            value_string = value_string.replace("'", "\"")

            # Convert the string to a dictionary
            value_dict = json.loads(value_string)

            self.values_core(int(value_dict["x"]), int(value_dict["y"]), int(value_dict["width"]),
                             int(value_dict["height"]))

            self.threshold_value_min = loaded_data["thr_v_min"]
            self.threshold_value_max = loaded_data["thr_v_max"]
            self.detection_text = loaded_data["text_detection"]
        # self.update_values()
        self.update_min_thresh(self.threshold_value_min)
        self.update_max_thresh(self.threshold_value_max)
        self.update_UI_numbers()

    def create_UI(self):

        # self.root.geometry("350x200")
        self.root.title("The best UI you will ever see")

        validate_numeric = (self.root.register(self.validate_input), "%P")
        self.switch_start = tk.CTkSwitch(self.root, text="Start ROI", command=self.start_switch)
        self.switch_start.grid(row=0, column=3, pady=10)

        self.switch = tk.CTkSwitch(self.root, text="Edit ROI", command=self.edit_switch)
        self.switch.grid(row=1, column=3, pady=10)

        self.switch_test_detection = tk.CTkSwitch(self.root, text="Test ROI", command=self.start_test_switch)
        self.switch_test_detection.grid(row=2, column=3, pady=10)

        text_x = tk.CTkLabel(self.root, text="X", padx=5, pady=10)
        text_x.grid(row=0, column=0)
        text_y = tk.CTkLabel(self.root, text="Y", padx=5, pady=10)
        text_y.grid(row=1, column=0)
        text_width = tk.CTkLabel(self.root, text="Width", padx=5, pady=10)
        text_width.grid(row=2, column=0)
        text_height = tk.CTkLabel(self.root, text="Height", padx=5, pady=10)
        text_height.grid(row=3, column=0)

        snipp_button = tk.CTkButton(self.root, text="Drag and Mark", command=self.creating_new_window)
        snipp_button.grid(row=5, column=2, pady=10)

        upload_button = tk.CTkButton(self.root, text="Load sound file", command=self.upload_file)
        upload_button.grid(row=4, column=2)
        self.x = tk.CTkEntry(self.root, validate="key", validatecommand=validate_numeric)
        self.x.insert(0, "1052")
        self.x.grid(row=0, column=1, padx=5, pady=10)
        self.y = tk.CTkEntry(self.root, validate="key", validatecommand=validate_numeric)
        self.y.insert(0, "630")
        self.y.grid(row=1, column=1, padx=5, pady=10)
        self.width = tk.CTkEntry(self.root, validate="key", validatecommand=validate_numeric)
        self.width.insert(0, "358")
        self.width.grid(row=2, column=1, padx=5, pady=10)

        self.height = tk.CTkEntry(self.root, validate="key", validatecommand=validate_numeric)
        self.height.insert(0, "88")
        self.height.grid(row=3, column=1, padx=5, pady=10)

        self.x_slider = tk.CTkSlider(self.root, from_=0, to=self.total_width,
                                     command=lambda value: self.slider(value, self.x))
        self.x_slider.set(int(self.x.get()))
        self.x_slider.grid(row=0, column=2, padx=5, pady=10)

        self.y_slider = tk.CTkSlider(self.root, from_=0, to=self.total_height,
                                     command=lambda value: self.slider(value, self.y))
        self.y_slider.set(int(self.y.get()))
        self.y_slider.grid(row=1, column=2, padx=5, pady=10)

        self.width_slider = tk.CTkSlider(self.root, from_=0, to=self.total_width,
                                         command=lambda value: self.slider(value, self.width))
        self.width_slider.set(int(self.width.get()))
        self.width_slider.grid(row=2, column=2, padx=5, pady=10)

        self.height_slider = tk.CTkSlider(self.root, from_=0, to=self.total_height,
                                          command=lambda value: self.slider(value, self.height))
        self.height_slider.set(int(self.height.get()))
        self.height_slider.grid(row=3, column=2, padx=5, pady=10)

        thrs_min = tk.CTkLabel(self.root, text="Threashold MIN", padx=5, pady=10)
        thrs_min.grid(row=6, column=1)
        thrs_max = tk.CTkLabel(self.root, text="Threashold MAX", padx=5, pady=10)
        thrs_max.grid(row=7, column=1)

        self.threshold_slider_min = tk.CTkSlider(self.root, from_=0, to=255, command=self.update_min_thresh)
        self.threshold_slider_min.grid(row=6, column=2, padx=5, pady=10)
        self.threshold_slider_min.set(int(self.threshold_value_min))

        self.threshold_slider_max = tk.CTkSlider(self.root, from_=0, to=255, command=self.update_max_thresh)
        self.threshold_slider_max.grid(row=7, column=2, padx=5, pady=10)
        self.threshold_slider_max.set(int(self.threshold_value_max))

        # blur_text = tk.CTkLabel(self.root, text="Blur", padx=5, pady=10)
        # blur_text.grid(row=6, column=3)

        detect_text_template = tk.CTkLabel(self.root, text="Test detection:", padx=5, pady=10)
        detect_text_template.grid(row=0, column=4)

        detection_text_text = tk.CTkLabel(self.root, text="Text to detect", padx=5, pady=10)
        detection_text_text.grid(row=0, column=5)

        entry_var = tk.StringVar()
        entry_var.set(self.detection_text)
        self.detection_text_panel = tk.CTkEntry(self.root,textvariable=entry_var)
        self.detection_text_panel.grid(row=1, column=5, pady=10)

        entry_var.trace("w", self.on_entry_change)

        self.detect_text_info = tk.CTkLabel(self.root, text="Not detected", padx=5, pady=10, bg_color="red")
        self.detect_text_info.grid(row=1, column=4)

        save_button = tk.CTkButton(self.root, text="Save config", command=self.save_settings)
        save_button.grid(row=3, column=4)
        load_button = tk.CTkButton(self.root, text="Load config", command=self.load_settings)
        load_button.grid(row=4, column=4)

        # self.blur = tk.CTkEntry(self.root, validate="key", validatecommand=validate_numeric)
        # self.blur.insert(0, "2")
        # self.blur.grid(row=7, column=3, padx=5, pady=10)

        # apply_blur = tk.CTkButton(self.root, text="Apply Blur", command=self.update_blur)
        # apply_blur.grid(row=8, column=3)

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        self.root.maxsize(w * 4, h * 4)
        self.root.minsize(w, h)

        self.root.grid_propagate(True)

    def start_UI(self):

        self.root.mainloop()
