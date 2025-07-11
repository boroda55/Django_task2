from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def recipe (request, dish):
    if dish not in DATA:
        return render(request, 'calculator/index.html', {'recipe': {}})
    servings = 1
    if 'servings' in request.GET:
        try:
            servings = int(request.GET['servings'])
            if servings <= 0:
                raise ValueError
        except ValueError:
            return HttpResponse("Неверное количество порций. Укажите целое положительное число.", status=400)

    scaled_recipe = {
        ingredient: round(amount * servings, 2) for ingredient, amount in DATA[dish].items()
    }

    return render(request, 'calculator/index.html', {'recipe': scaled_recipe})



# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
