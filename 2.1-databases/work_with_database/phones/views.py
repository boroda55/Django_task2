from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    # Получаем ссылку на метод order_by менеджера объектов модели Phone
    # (позволяет сортировать результаты запроса)
    order_by = Phone.objects.order_by

    # Указываем имя шаблона для рендеринга
    template = 'catalog.html'

    # Получаем параметр сортировки из GET-запроса
    # Если параметр 'sort' не передан, вернется None
    url_parameter = request.GET.get('sort', None)

    # Создаем словарь для хранения информации о текущем способе сортировки
    # Изначально все значения None - сортировка не активна
    sort_variants = {
        'sort_by_date': None,
        'sort_by_min_price': None,
        'sort_by_max_price': None,
        'sort_by_name': None
    }

    # Проверяем, был ли передан параметр сортировки
    if url_parameter:
        # Сортировка по минимальной цене (возрастание)
        if url_parameter == 'min_price':
            phones_from_db = order_by('price').all()  # ASC сортировка по price
            sort_variants['by_min_price'] = True  # Активируем флаг этой сортировки

        # Сортировка по максимальной цене (убывание)
        elif url_parameter == 'max_price':
            phones_from_db = order_by('-price').all()  # DESC сортировка по price
            sort_variants['by_max_price'] = True

        # Сортировка по имени (алфавитный порядок)
        elif url_parameter == 'name':
            phones_from_db = order_by('name').all()  # ASC сортировка по name
            sort_variants['by_name'] = True

        # Если передан неизвестный параметр - сортируем по дате (по умолчанию)
        else:
            phones_from_db = order_by('-release_date').all()  # DESC по дате
            sort_variants['by_date'] = True
    else:
        # Если параметр сортировки не указан - сортируем по дате (по умолчанию)
        phones_from_db = order_by('-release_date').all()
        sort_variants['by_date'] = True

    # Создаем базовый контекст с списком телефонов
    context = {'phones': phones_from_db}

    # Добавляем в контекст информацию о текущей сортировке
    context.update(sort_variants)

    # Добавляем в контекст SQL-запрос (для отладки)
    context.update({'query_set': phones_from_db.query.__str__()})

    # Рендерим шаблон с полученным контекстом
    return render(request, template, context)


def show_product(request, slug):
    # Указываем имя шаблона, который будет использоваться для рендеринга страницы
    # Это файл product.html в директории templates вашего приложения
    template = 'product.html'

    try:
        # Пытаемся найти телефон в базе данных по полю slug
        # Phone.objects.get() возвращает ОДИН объект, соответствующий условию
        # Если объект не найден - выбрасывается исключение ObjectDoesNotExist
        # Если найдено несколько объектов - MultipleObjectsReturned
        phone = Phone.objects.get(slug=slug)

    except ObjectDoesNotExist:
        # Обработка случая, когда телефон с указанным slug не найден
        # Возвращаем HTTP-ответ с кодом 404 (Not Found)
        # и текстовым сообщением 'Phone not found'
        return HttpResponseNotFound('Phone not found')

    # Создаем словарь контекста, который будет передан в шаблон
    # В данном случае передаем только один объект - найденный телефон
    context = {'phone': phone}

    # Рендерим шаблон с переданным контекстом и возвращаем HTTP-ответ
    # Функция render объединяет шаблон с данными и создает HttpResponse
    return render(request, template, context)
