import csv
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clientes.forms import TrackForm
from clientes.models import Reporte, FullSolution
from clientes.helpers import get_audited_list

def index(request):
    return JsonResponse({"message": "Hello World!"})

def audits_to_csv(request):

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    q = request.GET.get("q")

    query = FullSolution.audits.all()
    if q:
        if q == "filter":
            query = query.exclude(contrato__in=get_audited_list())

    writer = csv.writer(response)
    writer.writerow(["Contrato", "olt_name"])
    for item in query:
        writer.writerow([item.contrato, item.olt_name])

    return response

@login_required
def create_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.author = request.user
            track.save()
            return redirect('home')
    else:
        form = TrackForm()
    return render(request, 'create_track.html', {'form': form})

def reporte_list(request):
    reportes = Reporte.objects.all()
    return render(request, 'reporte_list.html', {'reportes': reportes})
