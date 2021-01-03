from decouple import config
import feedparser
import opengraph_parse
from feed_reader.models import Category, Entry
from datetime import datetime
from re import search
import pytz

feed_map = {
    # thinking on it, these should all be refactored to be defined at the database level.
    'andrew_yang': {
        'feed_url': config('RSS_FEED_ANDREW_YANG'),
        'results_category': 'andrew_yang'
    },
    'stimulus_checks': {
        'feed_url': config('RSS_FEED_STIMULUS_CHECKS'),
        'results_category': 'ubi'
    },
    'universal_basic_income': {
        'feed_url': config('RSS_FEED_UNIVERSAL_BASIC_INCOME'),
        'results_category': 'ubi'
    },
    'automation': {
        'feed_url': config('RSS_FEED_AUTOMATION'),
        'results_category': 'automation'
    }
}

def parse_updated_date(date):
    return datetime(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec, tzinfo=pytz.UTC)

def get_site_url(clean_link):
    reg = r'(?<=https:\/\/)[^\/]*'
    results = search(reg, clean_link)
    return results[0] if results else ''

def clean_link(dirty_link):
    # Regex removes google alert url wrapper.
    reg = r'(?<=https:\/\/w{3}\.google\.com\/url\?rct=j&sa=t&url=)(.*?)(?=&ct=ga&cd=)'
    results = search(reg, dirty_link)
    return results[0] if results else dirty_link

def clean_bolds(dirty_text):
    return dirty_text.replace('<b>', '').replace('</b>', '')

def save_category_model(feed_data, category_name):
    date_parsed = feed_data['feed']['updated_parsed']
    
    category, created = Category.objects.get_or_create(name=category_name)

    updated_date = parse_updated_date(date_parsed)

    if created:
        category.last_updated = updated_date
        category.save()
    else:
        if category.last_updated and category.last_updated >= updated_date:
            return False
        else:
            category.last_updated = updated_date
            category.save()

    return True

def save_entry_models(feed, category_name):
    for entry in feed['entries']:
        published_parsed_date = parse_updated_date(entry['published_parsed'])
        updated_parsed_date = parse_updated_date(entry['updated_parsed'])
        cleaned_link = clean_link(entry['link'])

        og_metadata = opengraph_parse.parse_page(cleaned_link, ["og:image", "og:title", "og:site_name"])

        saved_category = Category.objects.get(name=category_name)

        article, created = Entry.objects.get_or_create(
            link=cleaned_link, 
            link_dirty=entry['link'], 
            published=published_parsed_date, 
            updated=updated_parsed_date, 
            category_id=saved_category.id)

        if created:
            article.title = clean_bolds(entry['title'])
            article.link = cleaned_link
            article.link_dirty = entry['link']
            article.site_url = get_site_url(cleaned_link)
            article.summary = clean_bolds(entry['summary'])
            article.published = parse_updated_date(entry['published_parsed'])
            article.updated = parse_updated_date(entry['updated_parsed'])

            if og_metadata is not False:
                article.og_image = og_metadata['og:image'] or None if 'og:image' in og_metadata.keys() else None
                article.og_title = og_metadata['og:title'] or None if 'og:title' in og_metadata.keys() else None
                article.og_site_name = og_metadata['og:site_name'] or None if 'og:site_name' in og_metadata.keys() else None

        article.save()

def job():
    for key in feed_map.keys():
        parsed_data_url = feed_map[key]['feed_url']
        parsed_data_category = feed_map[key]['results_category']

        feed_results = feedparser.parse(parsed_data_url)
        
        able_to_update = save_category_model(feed_results, parsed_data_category)

        if able_to_update:
            save_entry_models(feed_results, parsed_data_category)

