from TopicFactory import TopicFactory


class ThreeDPlotter(TopicFactory):
    def __init__(self):

        self.input_dict = {
            "function": ["", "sin(x) + cos(x)", "length", "", ""],
            "x max": ["", "10", "length", ""],
            "x min": ["", "0", "length", "", ""],
        }

        self.info = {
            "input": self.input_dict,
            "formula": "",
            "Note": "This is a 2D Plotter",
            "solve_method": "",
            "plot_method": False,
            "Bonus": self.Bonus
        }

    def giveInfo(self):
        return self.info

    def Bonus(self, info):
        return self.selfPlot(info["input"]["function"][0], info["input"]["x max"][0], info["input"]["x min"][0])
    def selfPlot(self, function, xMax, xMin):
        import numpy as np
        import matplotlib.pyplot as plt
        from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                                implicit_multiplication_application)
        function_str = function

        # Define the range of values for x
        x_range = np.linspace(xMin, xMax, 100)

        # Parse the function string into a SymPy expression
        transformations = (standard_transformations + (implicit_multiplication_application,))
        function_expr = parse_expr(function_str, transformations=transformations)

        # Convert the SymPy expression to a NumPy function that can be evaluated on arrays
        f = np.vectorize(lambda x: function_expr.evalf(subs={'x': x}))

        # Evaluate the function for the x values
        y_values = f(x_range)

        # Find the max, min, and x-intercept of the function
        max_y = max(y_values)
        min_y = min(y_values)
        x_intercept = x_range[np.where(np.diff(np.sign(y_values)))[0][0]]

        # Create the plot and add the function curve
        fig, ax = plt.subplots()
        ax.plot(x_range, y_values)
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')
        # Annotate the max, min, and x-intercept of the function on the plot

        # Set labels for the axes and the title of the plot
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f"Plot of {function_str}")

        # Show the plot
        plt.show()