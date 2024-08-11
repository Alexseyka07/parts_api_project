from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .create import generate_parts
from .filter import (
    filter_mark_part_params,
    filter_marks_params,
    filter_other,
    filter_price,
)
from .models import mark, model, part

import json


def parts_create(request, count):
    result, error = generate_parts(count=count)
    if result:
        return HttpResponse("Parts created")
    return HttpResponse(f"ERROR: {error}")


def models(request):
    list_models = model.objects.all()
    if list_models.count() == 0:
        generate_parts(count=10000)
    data = [{"name": m.name, "mark": m.mark.name} for m in list_models if m.is_visible]
    return JsonResponse(data, safe=False)


def marks(request):
    list_marks = list(mark.objects.all())
    if list_marks.count() == 0:
        generate_parts(count=10000)
    data = [
        {"name": m.name, "producer_country_name": m.producer_country_name}
        for m in list_marks
        if m.is_visible
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def parts(request):
    query = json.loads(request.body)
    parts = part.objects.all()
    if parts.count() == 0:
        generate_parts(count=10000)
    if "mark_name" in query and "part_name" in query and "params" in query:
        parts = filter_mark_part_params(query=query, parts=parts)
    elif "mark_list" in query and "part_name" in query and "params" in query:
        parts = filter_marks_params(query=query, parts=parts)
    else:
        parts = filter_other(query=query, parts=parts)
    parts = filter_price(query=query, parts=parts)

    response = []
    summ = 0
    for p in parts:
        res_part = {
            "mark": {
                "id": p.mark.id,
                "name": p.mark.name,
                "producer_country_name": p.mark.producer_country_name,
            },
            "model": {"id": p.model.id, "name": p.model.name},
            "name": p.name,
            "json_data": p.json_data,
            "price": p.price,
        }
        summ += p.price
        response.append(res_part)

    page = int(query["page"])
    index = (page - 1) * 10
    response = response[index : (index + 10)]

    result = {"response": response, "count": len(parts), "summ": summ}

    return JsonResponse(result, safe=False)
