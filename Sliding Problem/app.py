##
# app.py
# contains the GUI for board.py

# Will have different modes of input with a drop down
# Will have a rating mode with radio buttons

import tkinter as tk
from tkinter import ttk
from board import *

LARGE_FONT = ("Verdana", 12)

class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Sliding Problem')
        self.container = tk.Frame(self)
        self.geometry("400x300+400+200") # Set a geometry for every slide

        self.container.pack(side ="top", fill = "both", expand = True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        
        for F in (Home,Help):
            frame = F(self.container,self)

            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")

        self.show_frame(Home)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def add_and_show_main_frame(self, row_column_varible):
        
        frame = UserControlPage(self.container,self, rows = row_column_varible)

        self.frames[UserControlPage] = frame
        frame.grid(row = 0, column=0, sticky="nsew")

        frame.tkraise()

class Home(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)

        self.frame_1 = tk.Frame(self)                           # Frame 1
        page_name_label = tk.Label(self.frame_1, text = "Home Page", font = LARGE_FONT)
        page_name_label.grid(columnspan = 2, row = 0, column =0)
        
        self.modes = ['A user controled square', 'Simulated squares for all possiblities', 'Simulated shapes for all possiblities']
        self.mode_variable = tk.StringVar()
        self.mode_variable.set(self.modes[0])
        mode_menu = tk.OptionMenu(self.frame_1, self.mode_variable, *self.modes)
        self.mode_variable.trace('w', self.toggle_show_row_column_entry)
        mode_menu.grid(row = 0, column = 1, columnspan = 2)
        self.frame_1.grid(row=0, column=0)

        self.frame_2 = tk.Frame(self)                               # Frame 2 (A Frame that can be forgotten)
        
        row_column_label = tk.Label(self.frame_2, text = "What it the size of the grid that you want to simulate:")
        row_column_label.grid(row = 0,column = 0)
        row_column_variable = tk.IntVar()
        row_column_variable.set(3)
        row_column_entry = tk.Entry(self.frame_2, textvariable = row_column_variable)
        row_column_entry.grid(row=1, column=0)
        self.frame_2.grid(row=1, column=0)


        self.control_frame = tk.Frame(self)                         # Control Frame (Has all the buttons)
        start_app_button = tk.Button(self.control_frame, text = "Start", command = lambda: self.start_pressed(controller, row_column_variable))
        start_app_button.grid(row=0,column = 0)

        help_button = tk.Button(self.control_frame, text = 'Help', command = lambda: controller.show_frame(Help))
        help_button.grid(row=0,column = 1)
        self.control_frame.grid(row=2, column=0)

    def toggle_show_row_column_entry(self, *args):
        if self.mode_variable.get() != self.modes[0]:
            self.frame_2.grid_forget()
        else:
            self.frame_2.grid(row=1, column=0)

    def start_pressed(self, controller, row_column_variable):
        mode = self.mode_variable.get()
        if mode == self.modes[0]:
            controller.add_and_show_main_frame(row_column_variable)
        elif mode == self.modes[1]:
            self.possible_list = tk.StringVar()
            graph_label = tk.Label(self, textvariable = self.possible_list)
            graph_label.grid(row=3,column=0)
            self.run_squares()


        elif mode == self.modes[2]:
            print('Mode Under Construction: \nPredicted Finish: Never')
            pass
            graph_frame = tk.Frame(self)

    def run_squares(self):
        possible_list = []
        for i in range(1,5):
            self.get_possiblities(i**2)
            possible_counter = 0
            while len(self.possiblities) > 0:
                board = Board(i)
                board.add_block(None, None, self.possiblities[0])
                board.nodeify()
                p = board.check_linkage()
                board.switch_the_switches(p)
                if board.is_possible():
                    possible_counter += 1
                    
                del self.possiblities[0]
            possible_list.append(possible_counter)
            self.possible_list.set(str(possible_list))

    def get_possiblities(self,final_length):
        self.possiblities = []
        self.recersion([],0,final_length,0)
        self.recersion([],1,final_length,0)

    def recersion(self,temp_list,value,final_length,distance):
        if len(temp_list) < final_length:
            temp_list.append(value)
        if len(temp_list) == final_length:
            self.possiblities.append(temp_list)
        else:
            self.recersion(temp_list,0,final_length,distance+1)
            self.recersion(temp_list[:distance+1],1,final_length,distance+1)
        
        
                
            
            
            

class UserControlPage(tk.Frame):
    
    def __init__(self, parent, controller, rows):
        
        tk.Frame.__init__(self,parent)

        self.rows = rows.get()

        self.board = Board(self.rows)

        home_page_button = tk.Button(self, text = "Home", command = lambda: controller.show_frame(Home))
        home_page_button.grid(row=11, column = 0, columnspan = self.rows)

        self.board_of_buttons = []

        self.ice_img     = tk.PhotoImage(file="ice.gif")
        self.boulder_img = tk.PhotoImage(file="boulder.gif")

        
        for i in range(self.rows):
            n = []
            for j in range(self.rows):
                n.append(tk.Button(self, image = self.ice_img, command = lambda x=i, y=j: self.change_mode(x,y,self.ice_img)))  
            self.board_of_buttons.append(n)

        for i in range(self.rows):
            for j in range(self.rows):
                self.board_of_buttons[j][i].grid(row = i, column = j)

        self.is_possible = tk.StringVar()
        self.is_possible.set(self.get_is_possible())
        self.is_possible_label = tk.Label(self, textvariable = self.is_possible)
        self.is_possible_label.grid(row = self.rows + 1, column = 0, columnspan=self.rows)



    def change_mode(self,row,column,image):
        self.change_image(row,column,image)
        self.board.board[row][column].change_type()
        for i in range(len(self.board.board)):
            for j in range(len(self.board.board)):
                self.board.board[i][j].off=True
                self.board.board[i][j].on=False
        self.is_possible.set(self.get_is_possible())
            
        

    def change_image(self, row, column, image):
        if image == self.ice_img:
            self.board_of_buttons[row][column] = tk.Button(self, image = self.boulder_img, command = lambda: self.change_mode(row,column,self.boulder_img))
            self.board_of_buttons[row][column].grid(row = column, column = row)
        else:
            self.board_of_buttons[row][column] = tk.Button(self, image = self.ice_img, command = lambda: self.change_mode(row,column,self.ice_img))
            self.board_of_buttons[row][column].grid(row = column, column = row)

    def get_is_possible(self):
        self.board.nodeify()
        p = self.board.check_linkage()
        self.board.switch_the_switches(p)
        
        if self.board.is_possible():
            return 'It is possible'
        else:
            return "It is not possible"

class Help(tk.Frame):

    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)
        intro_label = tk.Label(self, text = """This program is a simulation of a Sliding Problem.
In this Simulation, the idea is simple:
Is it possible to reach any one point from any other point.
The rules are also simple:
Once you start moving, you can't stop, unless you hit a wall. This mimics the motion of sliding on ice.

On the home screen Enter a number of rows. This is a BETA so the rows and the columns will be the same
creating a square grid.
Click the tiles to change them from ice to walls to ice to walls
Down the bottom will be the result.

Images are definatly subject to Copyright""")
        intro_label.pack()
        
        self.boulder_img = tk.PhotoImage(file = 'boulder.gif')
        self.ice_img = tk.PhotoImage(file = 'ice.gif')
        
        ice_img_label = tk.Label(self, image = self.ice_img)
        ice_img_label.pack()

        ice_explanation = tk.Label(self, text = 'Ice')
        ice_explanation.pack()

        boulder_img_label = tk.Label(self, image = self.boulder_img)
        boulder_img_label.pack()

        boulder_explanation = tk.Label(self, text = 'Boulder')
        boulder_explanation.pack()


        home_page_button = tk.Button(self, text = "Home", command = lambda: controller.show_frame(Home))
        home_page_button.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
