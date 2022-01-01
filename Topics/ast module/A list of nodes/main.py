import ast

expression = "(34 + 6) * (23**2 - 7 + 45**2)"

# put your code here
tree = ast.parse(expression)
nodes = ast.walk(tree)
print(len([x for x in nodes]))