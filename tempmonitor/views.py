from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import non_atomic_requests, atomic
from django.views.decorators.http import require_POST
from .models import temperatureReading
from django.db.models import Avg
from django.db.models.functions import TruncDate


@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        temperature = request.POST.get('data')
        time = request.POST.get('published_at')
        #save temperatureReading object
        temperature_entry = temperatureReading(temp=temperature)
        temperature_entry.save()
        #load all temperatureReading values as floats from database into a list
        temperatures = [float(reading.temp) for reading in temperatureReading.objects.all()]

    return JsonResponse({'temperatures': temperatures})


def temperature_data(request):
    # Group readings by date and calculate the daily average temperature
    daily_avg_queryset = temperatureReading.objects.annotate(date=TruncDate('time')).values('date').annotate(avg_temp=Avg('temp')).order_by('date')
    
    # Extract the dates and daily average temperatures from the queryset
    dates = [entry['date'].strftime("%d/%m/%Y") for entry in daily_avg_queryset]
    daily_avg_temperatures = [entry['avg_temp'] for entry in daily_avg_queryset]

    # Calculate the overall average temperature
    overall_avg = round(sum(daily_avg_temperatures) / len(daily_avg_temperatures), 2)

    # Calculate the monthly average temperatures
    monthly_avg = []
    for month in range(1, 13):
        monthly_temperatures = [entry['avg_temp'] for entry in daily_avg_queryset if entry['date'].month == month]
        if monthly_temperatures:
            monthly_avg.append(round(sum(monthly_temperatures) / len(monthly_temperatures), 2))
        else:
            monthly_avg.append(0)

    return JsonResponse({'dates': dates, 'daily_avg_temperatures': daily_avg_temperatures, 'overall_avg': overall_avg, 'monthly_avg': monthly_avg})


@csrf_exempt
def home(request):
    temperatures = [float(reading.temp) for reading in temperatureReading.objects.all()]
    dates = [reading.time for reading in temperatureReading.objects.all()]
    #convert dates to strings
    #dates = [date.strftime("%m/%d/%Y") for date in dates]

    #code to render graph will go here eventually

    return render(request, 'tempmonitor/home.html', {'temperatures': temperatures, 'dates': dates})


def about(request):
    return render(request, 'tempmonitor/about.html')


