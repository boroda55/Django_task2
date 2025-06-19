from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import Book

def books_view(request):
    template = 'books/books_list.html'
    context = {}
    return render(request, template, context)


def books_list_view(request):
    template = 'books/books.html'
    book_object = Book.objects.all()
    context = {'books' : book_object,}
    return render(request, template, context)


def book_pub_date(request, date):
    template = 'books/books_pub_date.html'
    book = Book.objects.get(pub_date=date)
    all_books = Book.objects.all().order_by('pub_date')
    all_dates = Book.objects.dates('pub_date', 'day').order_by('pub_date')
    current_index = list(all_dates).index(book.pub_date)
    prev_date = all_dates[current_index - 1] if current_index > 0 else None
    next_date = all_dates[current_index + 1] if current_index < len(all_dates)-1 else None
    context = {
        'book': book,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, template, context)
