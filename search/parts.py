from .models import mark, model, part
import random


def generate_parts(*, count: int) -> tuple[bool, str]:
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
