from django.shortcuts import render
from feed_reader.models import Entry, Category

def home(request):
    ubiEntries = Entry.objects.filter(category__name='ubi')
    yangEntries = Entry.objects.filter(category__name='andrew_yang')
    automationEntries = Entry.objects.filter(category__name='automation')

    context = {
        'articles': {
            'ubi': ubiEntries,
            'yang': yangEntries,
            'automation': automationEntries,
        }
    }
    return render(request, 'home.html', context)
