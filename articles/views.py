from django.shortcuts import render
from feed_reader.models import Entry, Category
from datetime import datetime, timedelta
import pytz

def get_entries(category_name, start_date, end_date):
    entries = Entry.objects.filter(category__name=category_name, hidden=False, updated__gt=start_date, updated__lte=end_date).order_by('-updated')
    return entries

def get_articles(start_date, end_date):
    ubiEntries = get_entries('ubi', start_date, end_date)
    yangEntries = get_entries('andrew_yang', start_date, end_date)
    automationEntries = get_entries('automation', start_date, end_date)

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

    return context

def home(request):
    date_cutoff = 30
    today_date = datetime.now(pytz.utc)
    cutoff_date = datetime.now(pytz.utc) - timedelta(days=date_cutoff)
    generated_context = get_articles(cutoff_date, today_date)

    generated_context['display_message'] = f"the last {date_cutoff} days"

    return render(request, 'home.html', generated_context)

def search_results(request):
    date_from_str = request.GET.get('datefrom')
    date_to_str = request.GET.get('dateto')

    date_from = ''
    date_to = ''

    try:
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d").replace(tzinfo=pytz.utc) if date_from_str else datetime.min.replace(tzinfo=pytz.utc)
    except ValueError:
        date_from = datetime.min.replace(tzinfo=pytz.utc)
        date_from_str = 'the dawn of time'
    
    try:
        date_to = datetime.strptime(date_to_str, "%Y-%m-%d").replace(tzinfo=pytz.utc) if date_to_str else datetime.now(pytz.utc)
    except ValueError:
        date_to = datetime.now(pytz.utc)
        date_to_str = 'now'

    generated_context = get_articles(date_from, date_to)
    generated_context['display_message'] = f"<b>{date_from_str if date_from_str else 'the dawn of time'}</b> to <b>{date_to_str if date_to_str else 'now'}</b>"

    return render(request, 'home.html', generated_context)
