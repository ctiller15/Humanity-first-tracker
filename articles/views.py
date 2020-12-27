from django.shortcuts import render
from feed_reader.models import Entry, Category

def home(request):
    categories = Category.objects.all()
    print(categories)

    entries = Entry.objects.all()
    print(entries)

    context = {
        'articles': entries
    }
    return render(request, 'home.html', context)
