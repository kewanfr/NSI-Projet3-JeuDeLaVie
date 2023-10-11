import tkinter as tk

# Define a function to change the color of a cell by its coordinates
def change_cell_color(row, column, color):
    # Get the list of widgets in the grid
    cells = root.grid_slaves()
    # Find the widget with the given row and column
    for cell in cells:
        if int(cell.grid_info()['row']) == row and int(cell.grid_info()['column']) == column:
            # Change the background color of the cell
            cell.configure(bg=color)
            break
# Define the function to execute on cell click
def cell_clicked(event):
    # Get the coordinates of the clicked cell
    cell = event.widget
    x, y = event.widget.grid_info()['row'], event.widget.grid_info()['column']
    change_cell_color(x, y, 'red')
    # if cell['bg'] == 'white':
    #     cell.configure(bg='black')
    # else:
    #     cell.configure(bg='white')
    print(f"Cell clicked: ({x}, {y})")

# Create the tkinter window
root = tk.Tk()

# Create the grid of cells
for i in range(10):
    for j in range(10):
        # Create a frame for each cell
        cell = tk.Frame(root, width=30, height=30, borderwidth=1, relief="solid")
        # Set the background color of the cell
        if (i + j) % 2 == 0:
            cell.configure(bg="white")
        else:
            cell.configure(bg="black")
        # Bind the click event to the cell
        cell.bind("<Button-1>", cell_clicked)
        # Add the cell to the grid
        cell.grid(row=i, column=j)

# Start the tkinter event loop
root.mainloop()