from TopicFactory import TopicFactory


class ThreeDPlotter(TopicFactory):
    def __init__(self):

        self.input_dict = {
            "function": ["", "sin(sqrt(x**2 + y**2))", "length", "", ""],
        }

        self.info = {
            "input": self.input_dict,
            "formula": "",
            "Note": "This is a 3D Plotter\n"
                    "Write the function so that the\n"
                    "dependant variable is omitted.\n"
                    "i.e. write z = x+y as x+y.",
            "solve_method": "",
            "plot_method": False,
            "Bonus": self.Bonus
        }

    def giveInfo(self):
        return self.info

    def Bonus(self, info):
        return self.selfPlot(info["input"]["function"][0])

    def selfPlot(self, function):
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                                implicit_multiplication_application)
        # Define the function to plot as a string
        function_str = function

        # Define the range of values for x and y
        x_range = np.linspace(-10, 10, 100)
        y_range = np.linspace(-10, 10, 100)

        # Create a meshgrid of the x and y values
        x_mesh, y_mesh = np.meshgrid(x_range, y_range)

        # Parse the function string into a SymPy expression
        transformations = (standard_transformations + (implicit_multiplication_application,))
        function_expr = parse_expr(function_str, transformations=transformations)

        # Convert the SymPy expression to a NumPy function that can be evaluated on arrays
        f = np.vectorize(lambda x, y: function_expr.evalf(subs={'x': x, 'y': y}))

        # Evaluate the function for the x and y values
        z_mesh = f(x_mesh, y_mesh)

        # Create the figure and the 3D axes
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the surface of the function
        ax.plot_surface(x_mesh, y_mesh, z_mesh)

        # Set labels for the axes
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # Show the plot
        plt.show(block="false")