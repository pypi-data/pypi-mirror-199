import os
import tkinter as tk
from tkinter import ttk
import Solver

# All the callback functions here

# The current object to be passed around
current_object = None


# Function for when a course is selected from the course drop down box
def courseSelect(event):
    sub_box.set("Subject")
    topic_box.set("Topic")
    course_txt = course_box.get()
    file_list = os.listdir(f"usu_apex/Input_Files/{course_txt}")
    sub_box['values'] = file_list


# Function for when a subject is selected
def subSelect(event):
    topic_box.set("Topic")
    course_txt = course_box.get()
    sub_txt = sub_box.get()
    file_list = os.listdir(f"usu_apex/Input_Files/{course_txt}/{sub_txt}")
    good_files = []
    for i in file_list:
        if i[-3:] == ".py":
            good_files.append(i[:-3])
    topic_box['values'] = good_files


# Function for when a topic is selected
def topicSelect(event):
    # Erase the current inputs
    note_text.delete("1.0", tk.END)
    note_text.insert("1.0", "Note:\n")
    for child in input_frame.winfo_children():
        child.destroy()

    # Build the file path
    course_txt = course_box.get()
    sub_txt = sub_box.get()
    topic_txt = topic_box.get()
    mod_name = f"Input_Files.{course_txt}.{sub_txt}.{topic_txt}"

    # Import the specified module and get make an object from the class inside
    module = __import__(mod_name, fromlist=['*'])

    class_count = 0
    for name, obj in module.__dict__.items():
        if isinstance(obj, type):
            class_count += 1
            if class_count == 2:
                global current_object
                current_object = obj()
                break

    info = current_object.giveInfo()

    # Create the info boxes in the GUI
    note = info['Note']
    note_text.delete("1.0", tk.END)
    note_text.insert("1.0", "Note:\n"+note)

    # Get the units
    itr=0
    for i, element in enumerate(info['input']):
        # print(f"Units.{inputs[element][2]}")
        module = __import__(f"Units.{info['input'][element][2]}", fromlist=['*'])

        class_obj = None
        class_count = 0
        for name, obj in module.__dict__.items():
            if isinstance(obj, type):
                class_count += 1
                if class_count == 2:
                    class_obj = obj
                    break

        my_obj = class_obj()
        unit_dict = my_obj.giveDict()

        label = tk.Label(input_frame, text=element)
        entry = tk.Entry(input_frame)
        entry.insert(0, info['input'][element][1])
        unit = ttk.Combobox(input_frame, values=list(unit_dict.keys()))
        unit.set(list(unit_dict.keys())[0])
        label.grid(row=itr, column=0)
        entry.grid(row=itr, column=1)
        unit.grid(row=itr, column=2)
        itr += 1

    execute.config(state="normal")


# Function for when the execute button is pressed
def execute():
    # Update info with parameters given by the user
    global current_object
    input_children = input_frame.winfo_children()
    info = current_object.giveInfo()
    itr = 0

    for child in input_children:
        if isinstance(child, tk.Label):
            label_txt = child.cget("text")
            info['input'][label_txt][0] = input_children[itr + 1].get()
            info['input'][label_txt][3] = input_children[itr + 2].get()
        itr += 1

    # Call the solver to solve the equation
    output_info = Solver.solve(info)
    #print(output_info)

    # Populate the output
    outputwin = tk.Tk()
    outputwin.geometry("500x500")
    formula = tk.Label(outputwin, text=output_info['formula'])
    formula.grid(row=0)
    inputs = tk.Label(outputwin, text="Input from user:")
    inputs.grid(row=1)

    itr = 2
    for i in info['input']:
        label = tk.Label(outputwin, text=i)
        entry = tk.Label(outputwin, text=str(output_info['input'][i][0]))
        unit = tk.Label(outputwin, text=output_info['input'][i][3])
        label.grid(row=itr, column=0)
        entry.grid(row=itr, column=1)
        unit.grid(row=itr, column=2)
        itr += 1

    outputs = tk.Label(outputwin, text="Output:")
    outputs.grid(row=itr)
    itr += 1
    for i in output_info['output']:
        label = tk.Label(outputwin, text=i)
        entry = tk.Label(outputwin, text=str(output_info['output'][i][0]))
        unit = ttk.Label(outputwin, text=output_info['output'][i][3])
        label.grid(row=itr, column=0)
        entry.grid(row=itr, column=1)
        unit.grid(row=itr, column=2)
        itr += 1


# End of callback functions

# Create root
root = tk.Tk()
root.geometry('500x500')
root.title("Engineering Calculator")

# Initialize frames for organization
top_frame = tk.Frame(root)
top_frame.pack(side='top', fill="both", expand=True)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', fill="both", expand=True)

file_frame = tk.Frame(top_frame, relief='groove')
file_frame.pack(side='left', fill="both", expand=True)

note_frame = tk.Frame(top_frame, relief='groove')
note_frame.pack(side="right", fill="both", expand=True)

input_frame = tk.Frame(bottom_frame, relief='groove')
input_frame.pack(fill="both", expand=True)

# create subject drop down boxes
course_box = ttk.Combobox(file_frame)
course_box.set("Course")
sub_box = ttk.Combobox(file_frame)
sub_box.set("Subject")
topic_box = ttk.Combobox(file_frame)
topic_box.set("Topic")

# Populate the course drop down
course_files = os.listdir("Input_Files")
course_box['values'] = course_files

# Bind callback functions for the drop-downs
course_box.bind("<<ComboboxSelected>>", courseSelect)
sub_box.bind("<<ComboboxSelected>>", subSelect)
topic_box.bind("<<ComboboxSelected>>", topicSelect)

# Pack all the drop-downs in tight
course_box.grid(row=0, column=0)
sub_box.grid(row=1, column=0)
topic_box.grid(row=2, column=0)

# Create the note and input label and go button
note_text = tk.Text(note_frame)
note_text.insert(tk.END, "Note:\n")
note_text.grid(row=0)

input_label = tk.Label(input_frame, text="Inputs")
input_label.grid(row=0)

execute = tk.Button(bottom_frame, text="Execute", command=execute, state="disabled")
execute.pack(side="bottom")

# run the mainloop to initialize the GUI
tk.mainloop()
