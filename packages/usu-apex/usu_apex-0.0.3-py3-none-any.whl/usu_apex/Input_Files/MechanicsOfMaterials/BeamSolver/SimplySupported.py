import numpy as np
import sympy
x, y2, y1 = sympy.symbols('x y2 y1')

# Example input list with string numbers
output_dict = ["17 -38*np.cos(np.pi/4)", "-10 30 38*np.cos(np.pi/4)", "-10 90 (5*38*np.cos(np.pi/4))"]

variables_passed = [[0], [y1, y2, -10], [-20, 4]]
"""""
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
"""
part1 = []
part2 = []
for i in range(3):
    if i == 1:
        continue
    part1.append(variables_passed[i])



variables = [x, y2]


part1[0].extend([variables[0]])
part1[1][1]= part1[1][1] * y2




# Define the equations
eq1 = sympy.Eq(sum(part1[0]), 0)
eq2 = sympy.Eq(sum(part1[1]), 0)


# Solve the system of equations
sol = sympy.solve((eq1, eq2), (x, y2))

# Print the solution

y2_ans = sol[y2]

eq3 = sympy.Eq(sum(variables_passed[1]), 0)

sol2 = sympy.solve((eq3.subs(y2, y2_ans), y2), y1)


sol.update(sol2)
print(sol)