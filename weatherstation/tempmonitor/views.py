from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import non_atomic_requests, atomic
from django.views.decorators.http import require_POST
from .models import temperatureReading
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        temperature = request.POST.get('data')
        time = request.POST.get('published_at')
        logger.debug(f'Temperature received: {temperature}, time: {time}')
        #save temperatureReading object
        temperature_entry = temperatureReading(temp=temperature)
        temperature_entry.save()
        logger.debug(f'Temperature entry saved: {temperature_entry}')

        #load all temperatureReading values as floats from database into a list
        temperatures = [float(reading.temp) for reading in temperatureReading.objects.all()]

        logger.debug(f'Temperatures: {temperatures}')
    return JsonResponse({'temperatures': temperatures})




def temperature_data(request):
    temperatures = [float(reading.temp) for reading in temperatureReading.objects.all()]
    dates = [reading.time.strftime("%d/%m/%Y") for reading in temperatureReading.objects.all()]

    avg = sum(temperatures)/len(temperatures)
    avg = round(avg, 2)

    monthly_avg = [] #list of average temperatures for each month

    #get average temperature for each month
    for month in range(1, 13):
        monthly_temperatures = [float(reading.temp) for reading in temperatureReading.objects.filter(time__month=month)]
        if len(monthly_temperatures) > 0:
            monthly_avg.append(round(sum(monthly_temperatures)/len(monthly_temperatures), 2))
        else:
            monthly_avg.append(0)

    return JsonResponse({'temperatures': temperatures, 'dates': dates, 'avg': avg, 'monthly_avg': monthly_avg})
    
@csrf_exempt
def home(request):
    temperatures = [float(reading.temp) for reading in temperatureReading.objects.all()]
    dates = [reading.time for reading in temperatureReading.objects.all()]
    logger.debug(f'Temperatures: {temperatures}')
    logger.debug(f'Dates: {dates}')
    #convert dates to strings
    #dates = [date.strftime("%m/%d/%Y") for date in dates]

    #code to render graph will go here eventually

    return render(request, 'tempmonitor/home.html', {'temperatures': temperatures, 'dates': dates})


def about(request):
    return HttpResponse('This will be the about page')


