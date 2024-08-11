from .models import mark, model, part
import random


def generate_parts(*, count: int) -> tuple[bool, str]:
    create_marks()
    create_models()
    colors = [
        "красный",
        "синий",
        "белый",
        "черный",
        "зеленый",
        "серый",
    ]
    part_names = [
        "бампер",
        "фара",
        "капот",
        "крыло",
        "дверь",
        "подвеска",
        "руль",
        "салон",
        "багажник",
        "зеркало",
        "задняя дверь",
        "передняя дверь",
        "передняя фара",
        "задняя фара",
        "сиденье",
        "колесо",
        "привод",
        "компрессор",
        "электроника",
        "двигатель",
        "тормоза",
    ]

    try:
        marks = mark.objects.all()
        models = model.objects.all()

        for _ in range(count):
            part_name = random.choice(part_names)
            random_mark = random.choice(marks)
            random_model = random.choice(models.filter(mark=random_mark))
            price = random.randint(1000, 10000)
            json_data = {
                "color": random.choice(colors),
                "is_new_part": random.choice([True, False]),
                "count": random.randint(1, 10),
            }

            part.objects.create(
                name=part_name,
                mark=random_mark,
                model=random_model,
                price=price,
                json_data=json_data,
                is_visible=random.choice([True, False]),
            )

        return True, ""
    except Exception as e:
        return False, str(e)

def create_marks() -> tuple[bool, str]: 
    mark.objects.all().delete()
    data = [
        {"name": "Mercedes", "producer_country_name": "Германия"},
        {"name": "BMW", "producer_country_name": "Германия"},
        {"name": "Honda", "producer_country_name": "Япония"},
        {"name": "Tesla", "producer_country_name": "США"},
        {"name": "Haval", "producer_country_name": "Китай"},
    ]
    try:
        for d in data:
            mark.objects.create(**d, is_visible=True)
        return True, ""
    except Exception as e:
        return False, str(e)


def create_models() -> tuple[bool, str]:
    model.objects.all().delete()
    data = [
        {"name": "Maybach", "mark": "Mercedes"},
        {"name": "g-class", "mark": "Mercedes"},
        {"name": "X5", "mark": "BMW"},
        {"name": "M5 Sedan", "mark": "BMW"},
        {"name": "Civic", "mark": "Honda"},
        {"name": "Accord", "mark": "Honda"},
        {"name": "Model 3", "mark": "Tesla"},
        {"name": "Cybertrack", "mark": "Tesla"},
        {"name": "Jolion", "mark": "Haval"},
        {"name": "H3", "mark": "Haval"},
    ]
    
    try:
        for d in data:
            m = mark.objects.get(name=d["mark"])
            model.objects.create(name = d["name"], mark = m, is_visible = True)
        return True, ""
    except Exception as e:
        return False, str(e)
