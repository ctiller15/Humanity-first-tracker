from django.shortcuts import render
from feed_reader.models import Entry, Category
from datetime import datetime, timedelta
import pytz

def get_entries(category_name):
    today_date = datetime.now(pytz.utc)
    cutoff_date = datetime.now(pytz.utc) - timedelta(days=30)
    entries = Entry.objects.filter(category__name=category_name, hidden=False, updated__lte=today_date, updated__gt=cutoff_date).order_by('-updated')
    return entries

def home(request):
    today_date = datetime.today()
    cutoff_date = datetime.today() - timedelta(days=30)
    ubiEntries = get_entries('ubi')
    yangEntries = get_entries('andrew_yang')
    automationEntries = get_entries('automation')

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
