from decouple import config
import feedparser
from feed_reader.models import Category, Entry
from datetime import datetime
from re import sub

feed_map = {
    'andrew_yang': {
        'feed_url': 'RSS_FEED_ANDREW_YANG',
        'results_category': 'andrew_yang'
    }
}

def parse_updated_date(date):
    return datetime(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec)

def clean_link(dirty_link):
    reg = r'https:\/\/w{3}\.google\.com\/url\?rct=j&sa=t&url='
    return sub(reg, '', dirty_link)

def save_category_model(feed_data, category_name):
    date_parsed = feed_data.feed.updated_parsed
    
    category, created = Category.objects.get_or_create(name=category_name)

    updated_date = parse_updated_date(date_parsed)

    if created:
        category.last_updated = updated_date
        category.save()
    else:
        if category.previous_date == updated_date:
            return False
        else:
            category.last_updated = updated_date
            category.save()

    return True

def save_entry_models(feed, category):
    for entry in feed.entries:
        article, created = Entry.objects.get_or_create(link_dirty=entry.link)

        if created:
            article.title = entry['title']
            article.link = clean_link(entry['link'])
            article.link_dirty = entry['link']
            article.summary = entry['summary']
            article.published = parse_updated_date(entry['published_parsed'])
            article.updated = parse_updated_date(entry['published_parsed'])

def job():
    
    parsed_data_url = feed_map['andrew_yang']['feed_url']
    parsed_data_category = feed_map['andrew_yang']['results_category']

    feed = feedparser.parse(parsed_data_url)
    
    able_to_update = save_category_model(feed, parsed_data_category)

    if able_to_update:
        save_entry_models(feed, parsed_data_category)

    print(config('RSS_FEED_ANDREW_YANG'))
