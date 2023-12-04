
# fastapi funciona mejor usando type hints
# Python no tiene tipado fuerte. Aunque hagamos type hint
# python permite seguir cambiando los tipos de las variables
# sin embargo para fastapi es interesante emplear los type hints

my_string_variable = "my string variable"
print(my_string_variable)
print(type(my_string_variable))

my_string_variable = 5
print(my_string_variable)
print(type(my_string_variable))

my_typed_variable: str = "my typed string variable"
print(my_typed_variable)
print(type(my_typed_variable))

my_typed_variable = 5
print(my_typed_variable)
print(type(my_typed_variable))