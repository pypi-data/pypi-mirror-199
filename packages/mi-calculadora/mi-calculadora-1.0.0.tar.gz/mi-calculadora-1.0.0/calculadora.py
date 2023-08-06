print("El programa ha comenzado a ejecutarse")
from py_expression_eval import Parser

parser = Parser()
expr = input("Introduce una expresión matemática: ")
result = parser.parse(expr).evaluate({})
print("El resultado de la expresión es:", result)

print("Este programa es la prueba del servidor")
input("Presiona Enter para salir...")
