import ast


code = """
import abcd
import xxxx
def greet(user_name):
    print("Hello, world!")
    print("Hello, ", user_name, "!", sep="")

user = "Mary"

greet(user)
"""

# put your code here
tree = ast.parse(code)
nodes = ast.walk(tree)
list_of_functions = []
for n in nodes:
    if isinstance(n, ast.Call):
        list_of_functions.append(n.func.id)
print(list_of_functions)
