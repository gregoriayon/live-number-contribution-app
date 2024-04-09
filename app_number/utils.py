from django.db.models import Sum


def get_chart_data(obj):
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [el['value__sum'] for el in qs]
    chart_labels = [el['owner'] for el in qs]

    return chart_data, chart_labels