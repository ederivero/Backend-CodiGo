nombres = ['Eduardo', 'Julia', 'Raul', 'Pedro']

print(nombres[0])
for nombre in nombres:
    print(nombre)


texto = 'hola, el dia de hoy llegare tarde'

for letra in texto:
    print(letra)

# si en el range no le indicamos el inicio, empezara desde el 0
for numero in range(10):
    print(numero)

print('--------')
for numero in range(5, 10):
    print(numero)

print('---------')
for numero in range(2, 20, 2):
    print(numero)

mes='julio'
while(mes != 'agosto'):
    print('no es agosto')
    break

edad = 9
if edad >= 18:
    print('puede consumir alcohol')
elif edad > 10:
    print('no puede consumir alcohol pero si caramelos')
else:
    print('no puede consumir absolutamente nada')