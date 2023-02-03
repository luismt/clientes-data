from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clientes.forms import TrackForm
from clientes.models import Reporte

def index(request):
    return JsonResponse({"message": "Hello World!"})

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
