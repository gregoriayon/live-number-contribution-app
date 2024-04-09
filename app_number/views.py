from django.shortcuts import render, redirect, get_object_or_404
from faker import Faker

from app_number.models import Statistic, DataItem
from app_number.utils import get_chart_data

# Create your views here.

fake = Faker()

def main(request):
    qs = Statistic.objects.all()
    if request.method == 'POST':
        new_statistic = request.POST.get('new-statistic')
        obj, _ = Statistic.objects.get_or_create(name=new_statistic)
        return redirect("app_number:dashboard", obj.slug)

    context = {
        'qs': qs
    }
    return render(request, 'app_number/main.html', context)


def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    chart_data, chart_labels = get_chart_data(obj)

    context = {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name(),

        'chart_data': chart_data,
        'chart_labels': chart_labels,
    }
    return render(request, 'app_number/dashboard.html', context)


