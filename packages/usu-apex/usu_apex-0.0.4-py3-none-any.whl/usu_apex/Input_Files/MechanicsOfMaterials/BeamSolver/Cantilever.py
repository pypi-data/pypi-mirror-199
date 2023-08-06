import numpy as np
import sympy
from TopicFactory import TopicFactory
class Cantilever(TopicFactory):
    def __init__(self):
        self.input_dict = {
            "Forcex": ["", "", "force", "", ""],
            "Forcey": ["", "", "force", "", ""],
            "Moment": ["", "", "torque", "", ""],
        }

        self.info = {
            "input": self.input_dict,
            "formula": "",
            "Note": """
                    This is a cantilerver beam solver. Input all of the x force components into the text box separated by a 
                    space. All moments are taken around the reaction force location at the wall. Input the moment components
                    into the text box in the same way as the forces. Force magnitudes multiplied by their respective trig function
                    are acceptable inputs.
                    """,
            "solve_method": "",
            "plot_method": False,
            "Bonus": self.Bonus
        }

    def giveInfo(self):
            return self.info

    def Bonus(self, info):
        print(info)
        return self.selfSolve(info["input"]["Forcex"][0], info["input"]["Forcey"][0], info["input"]["Moment"][0])

    def selfSolve(self, Forcex, Forcey, Moment):
        # Example input list with string numbers
        output_dict = [Forcex, Forcey, Moment]

        variables_passed = []

        for string in output_dict:
            split_string = string.split()
            new_sublist = []
            for substring in split_string:
                if '*' in substring:  # check if the substring contains multiplication
                    new_sublist.append(eval(substring))  # evaluate the expression and append to the new sublist
                else:
                    new_sublist.append(float(substring))  # convert the string to float and append to the new sublist
            variables_passed.append(new_sublist)

        print(variables_passed)



        x, y, m = sympy.symbols('x y m')

        variables=[x,y,m]

        for i in range(len(variables_passed)):
            variables_passed[i].extend([variables[i]])

        print(variables_passed)

        # Define the equations
        eq1 = sympy.Eq(sum(variables_passed[0]), 0)
        eq2 = sympy.Eq(sum(variables_passed[1]), 0)
        eq3 = sympy.Eq(sum(variables_passed[2]), 0)

        # Solve the system of equations
        sol = sympy.solve((eq1, eq2, eq3), (x, y, m))

        # Print the solution
        print(sol)

        return sol