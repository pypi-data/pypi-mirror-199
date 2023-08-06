#################
####  Todos  ####
#################
############################################
####  Link button fire to color change  ####
####                                    #######################
####  Implement score -> decrease based on required tiles  ####
####                                 ##########################
####  Offer hints -> decrease score  ####
####                              #######
####  messagebox on victory/fail  ####
####                              ####################
####  Color change to sequence provided Text box  ####
######################################################

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

from sympy import Symbol, lambdify
import numpy as np

from random import randint

from fractions import Fraction


x, y = Symbol('x'), Symbol('y')
f = lambdify([x, y], str(((-1)**x) / y))

for i in range(1, 10):
    print(Fraction(f(i, i)).limit_denominator(10))
    
######################
####  Difficulty  ####
######################
###################################################################
####  Easy - all tiles contain a correct part of the sequence  ####
####                                                           ##############
####  Medium - 50% of the extras contain a correct part of the sequence  ####
####                                                                    #####
####  Hard - 30% of the extras contain a correct part of the sequence   #####
####                                                                    ############
####  Cryptologist - None of the extras contain a correct part of the sequence  ####
####################################################################################
class TayloredTiles:
    # Spin off from Wordle
    # For some reason the change of difficulty messes with the range
    def __init__(self, root, symbols: list[str] = ['x'], formula: str = "1/x", difficulty: str = "Easy", colored_starters: int = 4):
        self.taylored_frame = ttk.Frame(root, padding=10)
        self.symbols = [Symbol(symbol) for symbol in symbols]
        self.formula = formula
        self.correct_extras = 0 # On hard
        
        self.colored_starters = colored_starters
        
        self.coords_list = []
        self.selected_answers = []
        self.buttons = {}
        self.mapped_button_pool = {}
        self.guess_formula = tk.StringVar()
        
        if difficulty == "Easy":
            self.correct_extras = 10
        elif difficulty == "Medium":
            self.correct_extras = 5
        elif difficulty == "Hard":
            self.correct_extras = 3
            
        self.generate_numbers()
        
        print(self.answers)
        print(self.total_pool)
        
        heading = ttk.Label(self.taylored_frame, text="Taylored Tiles!")
        description = ttk.Label(self.taylored_frame, text="Complete the sequence or write the formula!\nMore to follow!")
        self.numbers_in_sequence = ttk.Label(self.taylored_frame, text="")
        
        heading.grid(row=0, column=0)
        description.grid(row=1, column=0)
        self.numbers_in_sequence.grid(row=3, column=0)
        
        self.build_interface()
        
    # Not efficient but it's 530 in the morning
    # Need to fix here!!!
    def populate_label(self):
        indices = []
        
        for num in self.selected_answers:
            idx = self.answers.index(num)
            
            if idx != -1:
                indices.append(idx)
            
        text_string = ""
        for idx in range(len(self.answers)):
            if idx in indices:
                text_string += str(self.answers[idx])
            else:
                text_string += "?"
            if idx != len(self.answers) - 1:
                text_string += ", "
        
        return text_string
        
    def formify(self):
        return lambdify(*self.symbols, self.formula, "numpy") 

    def get_fractions(self, array, max_denominator: int = 10):
        return [Fraction(num).limit_denominator(max_denominator) for num in array]
                
    def generate_numbers(self):
        f = self.formify()
        self.answers = self.get_fractions(f(np.array([i for i in range(1, 11)])))
        
        # print(self.answers)
        # print(type(self.answers))
        
        self.total_pool = [self.answers[randint(0, len(self.answers)-1)] for _ in range(self.correct_extras)]
        
        for num in self.answers:
            self.total_pool.append(num)
        
    def check_list(self, row: int, column: int):
        # Figure this out later!!!
        num = self.buttons[self.coords_list[row * 5 + column]].cget('text')
        fractional_num = Fraction(num)
        
        try:
            if fractional_num in self.answers:
                if fractional_num not in self.selected_answers:
                    self.selected_answers.append(fractional_num)
                self.buttons[self.coords_list[row*5+column]].config(bg="green")
            
                """ Not working right now!
                
                print(self.mapped_button_pool)
                for val in self.mapped_button_pool[num].values():
                    print("HERE")
                    print(val)
                    if val != (row, column):
                        temp_row = val[0]
                        temp_column = val[1]
                        self.buttons[self.coords_list[temp_row*5 + temp_column]].config(bg="blue")
                """    
            else: 
                self.buttons[self.coords_list[row * 5 + column]].config(bg="red")
        except:
            print("Bad number!")
            
        # coord = f"{r}_{c}"
        for key, button in self.buttons.items():
            coord = f"{row}_{column}"
            
            if key != coord and button.cget('text') == num:
                button.config(bg="blue")
                
        self.numbers_in_sequence.config(text=self.populate_label())
            
    def color_button(self):
        pass
        
    def submit(self):
        guessed_formula = self.guessing_formula_entry.get()
        guessed_formula = guessed_formula.replace(' ', '')
        
        print(guessed_formula)
        print(self.formula)
        print(guessed_formula == self.formula)
        if guessed_formula == self.formula:
            messagebox.showinfo("Winner", "You Win!")
        
    def build_interface(self):
        board_frame = ttk.Frame(self.taylored_frame, padding=10)
        board_frame.grid(row=2, column=0, sticky="nesw")
        
        for r in range(4):
            for c in range(5):
                coord = f"{r}_{c}"
                
                # Refactor this into a method to use when clicked later!!!
                idx = randint(0, len(self.total_pool)-1)
                selected_number = self.total_pool[idx]
                del self.total_pool[idx]
                
                if self.colored_starters and selected_number in self.answers and selected_number not in self.selected_answers:
                    self.colored_starters -= 1
                    self.selected_answers.append(selected_number)
                    background = "green"
                    self.mapped_button_pool[str(selected_number)] = [(r, c)]
                else:
                    background = "gray"
                    if selected_number in self.answers:
                        try:
                            self.mapped_button_pool[str(selected_number)].append((r, c))
                        except:
                            self.mapped_button_pool[str(selected_number)] = [(r, c)]
                    
                self.coords_list.append(coord)
                self.buttons[self.coords_list[-1]] = tk.Button(board_frame, text=f"{selected_number}", bg=background)
                self.buttons[self.coords_list[-1]]['command'] = lambda row=r, column=c: self.check_list(row, column)
                self.buttons[self.coords_list[-1]].grid(row=r, column=c, padx=(10,10), pady=(10,10), sticky="nesw")
                
        self.numbers_in_sequence.config(text=self.populate_label())
        board_frame.columnconfigure(tuple(range(4)), weight=1)
        board_frame.rowconfigure(tuple(range(5)), weight=1)   
        
        guessing_formula_label = tk.Label(self.taylored_frame, text="Guess The Formula")
        self.guessing_formula_entry = tk.Entry(self.taylored_frame, textvariable=self.guess_formula)
        formula_response = ttk.Button(self.taylored_frame, text="Submit", command=self.submit)
        
        guessing_formula_label.grid(row=4, column=0)
        self.guessing_formula_entry.grid(row=5, column=0)
        formula_response.grid(row=6, column=0)
        
        
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.taylored_frame.grid(row=_row, column=_column) 
        
if __name__ == "__main__":
    root = tk.Tk()
    root.tk.call("source", "/usr/Sphinx/themes/Azure-ttk-theme-main/azure.tcl")
    root.tk.call("set_theme", "dark")
    
    tiles = TayloredTiles(root)
    tiles.set_grid()
    
    root.mainloop()
