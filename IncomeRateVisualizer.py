import threading
import tkinter as tk
import time
from datetime import datetime

# There are multiple things that need work in this program. At the end of this file you'll find a list of items I'm aware need changes

# Dictionary containing names and salaries
rich_people = {'Elon Musk': 1930000, 'Bill Gates': 198333, 'Jeff Bezos': 1430000, 'Warren Buffet': 570776,
               'Mark Zuckerberg': 375000, 'Mackenzie Scott': 1232876, 'Donald Trump': 144, 'The Walton Family': 4166666,
               'Joe Rogan': 3425, 'United States': -171232876}

# Model class to hold data (currently not utilized)
class IncomeModel:
    def __init__(self):
        self.data = None

# View class responsible for creating the GUI and handling user interactions
class IncomeView:
    # Initializations and UI setup
    def __init__(self, root, controller):
        self.elapsed_time_str = "0 Seconds"
        self.entered = "False"
        self.us_value = 0
        self.rate = 0
        self.rich_rate = 0
        self.lock = threading.Lock()
        self.root = root
        self.controller = controller
        self.options = list(rich_people.keys())
        self.selected_option = tk.StringVar()
        self.default = "Select"
        self.warning = tk.Label(root, text="", fg="red")
        self.dropdown = tk.OptionMenu(root, self.selected_option, *self.options)
        self.top_label = tk.Label(root, text="Enter Hourly Income:")
        self.rich_label = tk.Label(root, text="Select Rich Person:")
        self.income_entry = tk.Entry(width=7)
        self.start_button = tk.Button(root, text="Start", command=self.start_click)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_click, state="disabled")
        self.add_button = tk.Button(root, text="Add", command=self.add_new)
        self.income_counter_label = tk.Label(root)
        self.time_counter_label = tk.Label(root)
        self.rich_income_counter_label = tk.Label(root)
        self.rich_income_counter_label.config(text="")
        self.income_counter_label.config(text="")
        self.time_counter_label.config(text="")
        self.selected_option.set(self.default)
        self.edit_button = tk.Button(root, text="Edit", command=self.edit_pressed)
        self.about_button = tk.Button(root, text="About", command=self.about)
        self.fact_label = tk.Label(root, text="")

        self.warning.place(x=8, y=85)
        self.fact_label.place(x=10, y=300)
        self.income_counter_label.place(x=8, y=190)
        self.rich_income_counter_label.place(x=8, y=220)
        self.time_counter_label.place(x=8, y=250)
        self.top_label.place(x=8, y=20)
        self.income_entry.place(x=130, y=20)
        self.dropdown.place(x=115, y=50)
        self.start_button.place(x=8, y=125)
        self.stop_button.place(x=50, y=125)
        self.edit_button.place(x=92, y=125)
        self.about_button.place(x=225, y=125)
        self.add_button.place(x=130, y=125)
        self.rich_label.place(x=8, y=55)

    # Continuously update income counters while the application is running
    def update_counters(self, start_time):
        global running
        income = 0.00
        rich_income = 0.00
        last_printed_value = None
        rich_last_printed_value = None

        while running:
            with self.lock:
                try:
                    self.rate = float(self.income_entry.get())
                except ValueError:
                    self.warning.config(text="Your income entry must be a number")
                    break
                root.geometry("400x335")
                self.rich_rate = float(rich_people.get(self.selected_option.get()))
                '''"ms" means millisecond. There are probably better ways to accomplish this, but I essentially 
                forced these two variables below to assign the right value. otherwise, the printed values wouldn't 
                update properly. I think it's because I force the program to sleep through each iteration'''
                income_per_ms = (self.rate * 1.20 / 360000)
                rich_income_per_ms = (self.rich_rate * 1.20 / 360000)
                income += income_per_ms
                current_value = round(income, 2)
                rich_income += rich_income_per_ms
                self.rich_current_value = round(rich_income, 2)
                elapsed_time = datetime.now() - start_time
                self.disable_while_running()
                if current_value != last_printed_value:
                    self.income_counter_label.config(text=f"You: ${current_value:.2f}")
                    last_printed_value = current_value

                if self.selected_option.get() != self.default:
                    if self.rich_current_value != rich_last_printed_value:
                        self.rich_income_counter_label.config(
                            text=f"{self.selected_option.get()}: ${self.rich_current_value:.2f}")

                hours, remainder = divmod(elapsed_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.elapsed_time_str = ", ".join(
                    f"{value} {unit}{'s' if value > 1 else ''}"
                    for value, unit in zip((hours, minutes, seconds), ("hour", "minute", "second"))
                    if value > 0)
                self.time_counter_label.config(text=f"Time Elapsed: {self.elapsed_time_str}")
                self.root.update()
                self.fact_label_update()
                time.sleep(0.01)

    def run_function(self):
        # Start a separate thread to run the update_counters function
        global running
        start_time = datetime.now()
        threading.Thread(target=self.update_counters, args=(start_time,), daemon=True).start()

    def start_click(self):
        # Handle the start button click event and initiate the income calculation
        self.fact_label.config(text="")
        if self.selected_option.get() == "Select" and self.income_entry.get() == "":
            self.warning.config(text="Please select a name and enter your income")
            return
        elif self.selected_option.get() == "Select" and self.income_entry.get() != "":
            self.warning.config(text="Please select a name from the dropdown")
            return
        elif self.selected_option.get() != "Select" and self.income_entry.get() == "":
            self.warning.config(text="Please enter your income")
            return
        else:
            global running
            running = True
            self.warning.config(text="")
            self.run_function()

    def stop_click(self):
        # Handle the stop button click event and stop the income calculation
        global running
        running = False
        self.entered = "False"
        self.fact_label.config(text="")
        root.geometry("300x175")
        self.enable_after_stop()

    def fact_label_update(self):
        # Update the fact label based on the income comparison with a rich person
        # This entire function needs to be overhauled and simplified
        if self.selected_option.get() != "United States":
            user_income = float(self.income_entry.get())
            if self.rich_current_value > ((user_income * 40) * 52) and self.entered == "Monthly":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(text="In " + time_string + " " + self.selected_option.get() + " has earned your yearly income.")
                self.entered = "Yearly"
            elif self.rich_current_value > (((user_income * 40) * 52) / 12) and self.entered == "Weekly":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(text="In " + time_string + " " + self.selected_option.get() + " has earned your monthly income.")
                self.entered = "Monthly"
            elif self.rich_current_value > user_income * 40 and self.entered == "Hourly":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(text="In " + time_string + " " + self.selected_option.get() + " has earned your weekly income.")
                self.entered = "Weekly"
            elif self.rich_current_value > user_income and self.entered == "False":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(text="In " + time_string + " " + self.selected_option.get() + " has earned your hourly income.")
                self.entered = "Hourly"
        elif self.selected_option.get() == "United States":
            user_income = float(self.income_entry.get())
            self.us_value = abs(self.rich_current_value)
            if self.us_value > ((user_income * 40) * 52) and self.entered == "Monthly":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(
                    text="In " + time_string + " " + self.selected_option.get() + " has spent your yearly income.")
                self.entered = "Yearly"
            elif self.us_value > (((user_income * 40) * 52) / 12) and self.entered == "Weekly":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(
                    text="In " + time_string + " " + self.selected_option.get() + " has spent your monthly income.")
                self.entered = "Monthly"
            elif self.us_value > user_income * 40 and self.entered == "Hourly":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(
                    text="In " + time_string + " " + self.selected_option.get() + " has spent your weekly income.")
                self.entered = "Weekly"
            elif self.us_value > user_income and self.entered == "False":
                time_string = ""
                if time_string == self.elapsed_time_str:
                    time_string = "less than 1 Second"
                else:
                    time_string = self.elapsed_time_str
                self.fact_label.config(
                    text="In " + time_string + " " + self.selected_option.get() + " has spent your hourly income.")
                self.entered = "Hourly"



    def add_new(self):
        # Open a new window to add a new person with name and hourly income
        self.disable_main_screen()
        self.new_person_window = tk.Toplevel(self.root)
        self.new_person_window.title("Add New")
        self.new_person_window.geometry("225x175")
        new_frame = tk.Frame(self.new_person_window)
        new_frame.pack(pady=20, padx=20)
        self.add_warning = tk.Label(self.new_person_window, text="", fg="red")
        self.name_entry = tk.Entry(self.new_person_window, width=16)
        self.salary_entry = tk.Entry(self.new_person_window, width=9)
        self.new_person_name = tk.Label(self.new_person_window, text="Name:")
        self.new_person_income = tk.Label(self.new_person_window, text="Hourly Income:")
        self.save_button = tk.Button(self.new_person_window, text="Save", command=self.save_person)
        self.cancel_button = tk.Button(self.new_person_window, text="Cancel", command=self.cancel_new)
        self.add_warning.place(x=10, y=85)
        self.name_entry.place(x=60, y=20)
        self.salary_entry.place(x=100, y=50)
        self.new_person_name.place(x=10, y=20)
        self.new_person_income.place(x=10, y=50)
        self.save_button.place(x=50, y=125)
        self.cancel_button.place(x=100, y=125)
        self.new_person_window.protocol("WM_DELETE_WINDOW", self.cancel_new_window)

    def cancel_new_window(self):
        # Handle closing the new person window
        self.enable_main_screen()
        self.selected_option.set(self.default)
        self.enable_main_screen()
        self.new_person_window.destroy()

    def save_person(self):
        # Save the new person's information and update the UI accordingly
        new_name = self.name_entry.get()
        new_income = (self.salary_entry.get())
        check_income = 0
        if new_name and new_income:
            try:
                check_income = float(new_income)
            except ValueError:
                self.add_warning.config(text="Income must be a number")
                return
            if check_income:
                rich_people.update({new_name: new_income})
                self.options = list(rich_people.keys())
                self.selected_option.set(self.default)
                self.dropdown.destroy()
                self.dropdown = tk.OptionMenu(self.root, self.selected_option, *self.options)
                self.dropdown.place(x=115, y=50)
                self.enable_main_screen()
                self.new_person_window.destroy()
        elif not new_name and not new_income:
            self.add_warning.config(text="Please add a name and income")
        elif new_name and not new_income:
            self.add_warning.config(text="Please add a value for 'Income'")
        elif not new_name and new_income:
            try:
                check_income = float(new_income)
            except ValueError:
                self.add_warning.config(text="Add a name, Income must be a number")
                return
            if check_income:
                self.add_warning.config(text="Please add a name")
        else:
            self.enable_main_screen()
            self.new_person_window.destroy()
            return




    def cancel_new(self):
        # Handle canceling the addition of a new person
        self.enable_main_screen()
        self.new_person_window.destroy()
        self.selected_option.set(self.default)

    def edit_pressed(self):
        # Open a new window to edit the list of people
        self.disable_main_screen()
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit")
        self.edit_window.geometry("225x365")

        # Create a list to store the Checkbutton widgets
        self.checkboxes = []

        new_frame = tk.Frame(self.edit_window)
        new_frame.pack(pady=20, padx=20)

        # Iterate over the dictionary and create Checkbutton for each entry
        for name in rich_people:
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(new_frame, text=name, variable=checkbox_var)
            checkbox.pack(anchor='w')
            self.checkboxes.append((name, checkbox, checkbox_var))
        self.delete_selected = tk.Button(self.edit_window, text="Delete Selected", command=self.delete_entries)
        self.cancel_edit = tk.Button(self.edit_window, text="Cancel", command=self.cancel_edit_button)
        self.delete_selected.place(x=10, y=325)
        self.cancel_edit.place(x=110, y=325)
        self.edit_window.protocol("WM_DELETE_WINDOW", self.cancel_edit_button)

    def cancel_edit_button(self):
        # Handle canceling the edit operation and close the edit window
        self.enable_main_screen()
        self.edit_window.destroy()

    def delete_entries(self):
        # Iterate over the list of Checkbutton tuples and delete selected entries
        for name, _, var in self.checkboxes:
            if var.get():
                del rich_people[name]

        # Update options in the dropdown menu
        self.options = list(rich_people.keys())
        self.selected_option.set(self.default)
        self.dropdown.destroy()
        self.dropdown = tk.OptionMenu(self.root, self.selected_option, *self.options)
        self.dropdown.place(x=115, y=50)

        self.enable_main_screen()
        self.edit_window.destroy()

    def about(self):
        # Display information about the application in a separate window
        self.about_window = tk.Toplevel(self.root)
        self.about_window.title("About")
        self.about_window.geometry("500x335")
        new_frame = tk.Frame(self.about_window)
        self.close_button = tk.Button(self.about_window, text="Close", command=self.close_about)
        self.title_text = tk.Label(self.about_window, text="Income Rate Visualizer", font=("Helvetica", 12))
        about_text = ("I built this application because I was curious to see the rate at which someone \nearns money "
                      "when compared to the average hourly income of a billionaire. \nOriginally it was just a CLI "
                      "application until I decided to implement a GUI. \n\n The basic functionality requires the user"
                      " to input their hourly income as well \nas select a name from the dropdown. If you'd like to "
                      "modify the list you can \nadd entries using the 'Add' button. These fields take entered data "
                      "and adds \nit to the dictionary. If you'd like to edit the list you can do so through the"
                      " 'Edit' \nbutton. This allows the user to select names using checkboxes to remove from \n"
                      "the dictionary and save changes. While running the script the incomes \nare "
                      "calculated to display the average income over time at a constant rate. While it \nmay not be "
                      "entirely accurate, it is only intended to be an average rate of change.")
        self.about_label = tk.Label(self.about_window, text=about_text, anchor='w')
        self.about_label.place(x=10, y=65)
        self.title_text.place(x=10, y=15)
        new_frame.pack(pady=20, padx=20)
        self.close_button.place(x=15, y=300)
        self.disable_main_screen()
        self.about_window.protocol("WM_DELETE_WINDOW", self.close_about)

    def close_about(self):
        # Close the about window
        self.enable_main_screen()
        self.about_window.destroy()

    def disable_while_running(self):
        # Disable UI elements while the application is running
        self.income_entry.config(state="disabled")
        self.dropdown.config(state="disabled")
        self.start_button.config(state="disabled")
        self.about_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.add_button.config(state="disabled")
        return

    def enable_after_stop(self):
        # Enable UI elements after stopping the application
        self.income_entry.config(state="normal")
        self.dropdown.config(state="normal")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.edit_button.config(state="normal")
        self.about_button.config(state="normal")
        self.add_button.config(state="normal")
        return

    def disable_main_screen(self):
        # Disable UI elements on the main screen
        self.income_entry.config(state="disabled")
        self.dropdown.config(state="disabled")
        self.start_button.config(state="disabled")
        self.about_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        self.add_button.config(state="disabled")
        return

    def enable_main_screen(self):
        # Enable UI elements on the main screen
        self.income_entry.config(state="normal")
        self.dropdown.config(state="normal")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.edit_button.config(state="normal")
        self.about_button.config(state="normal")
        self.add_button.config(state="normal")
        return


class IncomeController:
    # Controller class to manage the interaction between the model and view
    def __init__(self, root):
        self.model = IncomeModel()
        self.view = IncomeView(root, self)


if __name__ == "__main__":
    # Main entry point of the application
    root = tk.Tk()
    app = IncomeController(root)
    root.title("Income Rate Visualizer")
    root.geometry("300x175")
    root.mainloop()


# Below are things I'd like to change as well as things I know still need work. The basic functionality is here with minor bugs I need to work out.

# 1) Deleting all data in the dictionary makes it crash so that needs to be fixed
# 2) Add dynamic window scaling for the edit window so the window scales properly to fit all entries
# 3) Add a label at the top of the "Edit" window just for aesthetic and clarity that says "Select names to delete" or something
# 4) Fix the fact_label_update method, so it's more compact and doesn't burn your eyes when looking at the code. Printed text should be generated using "F-strings"
# 5) I'd like the "About" window to be able to scroll and I should format the text properly. Also put more pertinent information about the app
# 6) Somehow fix the code for "About" window text. Basically, redo the whole "About" window
# 7) In the "Add" and "Main" windows, I'd like to allow the user to select hourly or yearly income using dropdowns or radio buttons and input that instead of only hourly
# 8) Migrate to using a JSON file instead of using just a dictionary. I'd like the information to persist over multiple runs
# 9) In the "Edit" window, make it so you can update and save current entries income as well as delete them
# 10) Sometimes when stopping the program, the buttons don't reset properly at first for some reason