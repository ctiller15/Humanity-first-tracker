from django.shortcuts import render
from feed_reader.models import Entry, Category

def home(request):
    ubiEntries = Entry.objects.filter(category__name='ubi', hidden=False).order_by('-updated')
    yangEntries = Entry.objects.filter(category__name='andrew_yang', hidden=False).order_by('-updated')
    automationEntries = Entry.objects.filter(category__name='automation', hidden=False).order_by('-updated')

    yang_category, yang_category_created = Category.objects.get_or_create(name='andrew_yang')
    ubi_category, ubi_category_created = Category.objects.get_or_create(name='ubi')
    automation_category, automation_category_created = Category.objects.get_or_create(name='automation')

    context = {
        'articles': {
            'ubi': {
                'articles': ubiEntries,
                'updated': ubi_category.last_updated
            },
            'yang': {
                'articles': yangEntries,
                'updated': yang_category.last_updated
            },
            'automation': {
                'articles': automationEntries,
                'updated': automation_category.last_updated
            }
        }
    }

    return render(request, 'home.html', context)
