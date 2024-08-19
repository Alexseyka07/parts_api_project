from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .create import generate_parts, create_query
from .filter import (
    filter_mark_part_params,
    filter_marks_params,
    filter_mark_model,
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
    if len(list_models) == 0:
        generate_parts(count=10000)
    data = [{"name": m.name, "mark": m.mark.name} for m in list_models if m.is_visible]
    return JsonResponse(data, safe=False)


def marks(request):
    list_marks = list(mark.objects.all())
    if len(list_marks) == 0:
        generate_parts(count=10000)
    data = [
        {"name": m.name, "producer_country_name": m.producer_country_name}
        for m in list_marks
        if m.is_visible
    ]
    return JsonResponse(data, safe=False)


def parts(request):

    marks = mark.objects.all()
    return render(
        request=request, context={"marks": marks}, template_name="search/parts.html"
    )


@csrf_exempt
def parts_response(request):
    print(request.body)
    req = request.POST
    parts = part.objects.all()
    if len(parts) == 0:
        generate_parts(count=10000)
    query = create_query(req)
    if "mark_name" in query and "part_name" in query and "color" in query["params"]:
        parts = filter_mark_part_params(query=query, parts=parts)
    if "mark_list" in query and "part_name" in query and "color" in query["params"]:
        parts = filter_marks_params(query=query, parts=parts)
    if "mark_name" in query and "model_name" in query:
        parts = filter_mark_model(query=query, parts=parts)

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

    result = {"response": response, "count": len(parts), "summ": summ }

    return render(request=request, context=result, template_name="search/parts.html")
