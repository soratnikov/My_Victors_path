class Book:
    title = "заголовок"
    pages = 143
    def __init__(self):
        self.name = "Книга джунглей"
    def set_attr(self, title):
        pass

book1 = Book()
book2 = Book()

# book1.name = "Над пропастью во ржи"
# book1.year = 2025


print(Book.__dict__)
print(book1.__dict__)
print(book1.name)
print(id(book1.name))
print(book2.name)
print(id(book2.name))

class Goods:
    title = "Мороженое"
    weight = 154
    tp = "Еда"
    price = 1024

delattr(Goods, "price")
setattr(Goods, "price", 2048)
setattr(Goods, "inflation", 100)

print(Goods.price)



class Notes:
    ...
attrs = {
    "uid": 1005435,
    "title": "Шутка",
    "author": "И.С. Бах",
    "pages": 2,
}

[setattr(Notes,k,v) for k,v in attrs.items()]
print(getattr(Notes, "author", False))


class TravelBlog:
    total_blogs = 0


tb1 = TravelBlog()

setattr(tb1, "name", "Франция")
setattr(tb1, "days", 6)
TravelBlog.total_blogs += 1
tb2 = TravelBlog()
print(TravelBlog.total_blogs)

setattr(tb2, "name", "Италия")
setattr(tb2, "days", 5)
TravelBlog.total_blogs += 1
print(TravelBlog.total_blogs)



class Figure:
    type_fig = "ellipse"
    color = "red"


dict = {
    "start_pt": (10, 5),
    "end_pt": (100, 20),
    "color": 'blue',
}

fig1 = Figure()
[setattr(fig1, k, v) for k, v in dict.items()]
delattr(fig1, "color")

for item in fig1.__dict__:
    print(item, sep=" ", end=" ")


class Person:
    name = "Сергей Балакирев"
    job = "Программист"
    city = "Москва"

p1 = Person()

print(hasattr(p1, "job"))

class Graph:
