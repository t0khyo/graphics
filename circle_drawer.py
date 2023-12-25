from tkinter import *

def draw_circle(canvas):
    x_point = int(x.get())
    y_point = int(y.get())
    radius = int(r.get())
    canvas.create_oval(x_point - radius, y_point - radius, x_point + radius, y_point + radius, outline="black", width=2)

# Create the main window
root = Tk()
root.title("Circle Drawer")

# Create a canvas widget
canvas = Canvas(root, width=400, height=400)
canvas.grid(row=0, column=0, columnspan=3)

# Labels and Entry widgets
Label(root, text="X:", fg="black", font="none 12").grid(row=1, column=0, sticky=W)
x = Entry(root, width=20, bg="white")
x.grid(row=1, column=1, columnspan=2)

Label(root, text="Y:", fg="black", font="none 12").grid(row=2, column=0, sticky=W)
y = Entry(root, width=20, bg="white")
y.grid(row=2, column=1, columnspan=2)

Label(root, text="Radius:", fg="black", font="none 12").grid(row=3, column=0, sticky=W)
r = Entry(root, width=20, bg="white")
r.grid(row=3, column=1, columnspan=2)

# Button
Button(root, text="Draw the circle", width=15, command=lambda: draw_circle(canvas)).grid(row=4, column=1, pady=10)

# Start the Tkinter event loop
root.mainloop()
