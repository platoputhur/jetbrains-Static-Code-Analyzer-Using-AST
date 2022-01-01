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

tree = ast.parse(code)

# put your code here
nodes = ast.walk(tree)
for n in nodes:
    if isinstance(n, ast.Import) or isinstance(n, ast.ImportFrom):
        print(n.names[0].name)
