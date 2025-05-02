
import turtle


turtle.color("#0000CD")                                    # Цвет пера синий
number = input('Введите количество окружностей')  # Сохраняем ввод в переменную
number = int(number)                              # Преобразуем в число
for i in range(number):
    turtle.circle(100)
    turtle.left(360 / number)                           # Рассчитываем угол

turtle.mainloop()