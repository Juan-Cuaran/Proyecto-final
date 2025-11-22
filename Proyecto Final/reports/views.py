from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from accesscontrol.models import AccessEventModels
from .models import Report


def list_reports(request):
    reports = Report.objects.all().order_by('-generated_at')
    return render(request, 'reports/list_reports.html', {'reports': reports})


def report_detail(request, pk):
    report = get_object_or_404(
        Report.objects.prefetch_related(
            Prefetch(
                'events',
                queryset=AccessEventModels.objects.select_related('credential', 'access_point').order_by('-timestamp')
            )
        ),
        pk=pk
    )
    events = report.events.all()
    return render(request, 'reports/report_detail.html', {'report': report, 'events': events})
