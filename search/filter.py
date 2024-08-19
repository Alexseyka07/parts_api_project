from .models import mark, model, part

def filter_mark_part_params(*, query, parts):
    if query["params"]["color"] == "all":
        parts = parts.filter(
            mark=mark.objects.filter(name__iexact=query["mark_name"]).first(),
            name__icontains=query["part_name"],
            json_data__is_new_part=bool(query["params"]["is_new_part"]),
            is_visible=True,
        )
        return parts

    parts = parts.filter(
        name__icontains=query["part_name"],
        mark=mark.objects.filter(name__iexact=query["mark_name"]).first(),
        json_data__color=query["params"]["color"],
        json_data__is_new_part=bool(query["params"]["is_new_part"]),
        is_visible=True,
    )

    return parts


def filter_marks_params(*, query, parts):
    if query["params"]["color"] == "all":
        parts = parts.filter(
            mark__id__in=[m for m in query["mark_list"]],
            name__icontains=query["part_name"],
            json_data__is_new_part=bool(query["params"]["is_new_part"]),
            is_visible=True,
        )
        return parts
    
    parts = parts.filter(
        mark__id__in=[m for m in query["mark_list"]],
        name__icontains=query["part_name"],
        json_data__is_new_part=bool(query["params"]["is_new_part"]),
        json_data__color=query["params"]["color"],
        is_visible=True,
    )

    return parts

def filter_mark_model(*, query, parts):
    parts = parts.filter(
        mark=mark.objects.filter(name__iexact=query["mark_name"]).first(),
        model=model.objects.filter(name__iexact=query["model_name"]).first(),
        json_data__is_new_part=bool(query["params"]["is_new_part"]),
        is_visible=True,
    )

    return parts

def filter_price(*, query, parts):
    if "price_gte" in query and query["price_gte"] != "":
        parts = parts.filter(price__gte=query["price_gte"])
    if "price_lte" in query and query["price_lte"] != "":
        parts = parts.filter(price__lte=query["price_lte"])
        
    return parts
