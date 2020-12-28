from django.shortcuts import render
from resources.models import Resource

def resources(request):
    resources = Resource.objects.all().order_by('order').filter(hidden=False)

    context = {
        'resources': resources
    }

    return render(request, 'resources.html', context)


