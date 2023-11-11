from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import WeatherData
from .forms import CityForm
import requests
from django.shortcuts import render
from rest_framework import generics
from .serializers import WeatherDataSerializer

@login_required(login_url='login')
def HomePage(request):
    city_name = request.GET.get('city_name', '')  # Set a default value if not provided in the request
    return render(request, 'home.html', {'city_name': city_name})
# User authentication views
def SignupPage(request):
    if request.method == 'POST':
        # Handle user registration
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return HttpResponse("Passwords do not match.")
        else:
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')
    
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        # Handle user login
        username = request.POST.get('username')
        password1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=password1)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username/Password is not correct.")
    
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

# Weather data views
@login_required(login_url='login')
def HomePage(request):
    city_name = request.GET.get('city_name', '')  # Set a default value if not provided in the request
    return render(request, 'home.html', {'city_name': city_name})

def add_weather_data(request):
    if request.method == 'POST':
        # Get data from the request
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        location = request.POST.get('location')
        
        # Save data to the database
        weather_data = WeatherData(temperature=temperature, humidity=humidity, location=location)
        weather_data.save()
        
        return JsonResponse({'message': 'Weather data added successfully'})
    
    return JsonResponse({'message': 'Invalid request method'})

def city_weather(request, city_name):
    unit = request.GET.get('unit', 'metric')  # Default to metric if not provided
    api_key = 'f8b3464e1efdf3b190a4c7451941c72b'  
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={unit}'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    background_color = get_background_color(weather_description)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)

        data = response.json()

        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        visibility = data.get('visibility', 'N/A')
        weather_description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']

        context = {
            'city_name': city_name,
            'temperature': temperature,
            'feels_like': feels_like,
            'humidity': humidity,
            'visibility': visibility,
            'weather_description': weather_description,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'background_color': background_color,
        }
        return render(request, 'city_weather.html', context)
    
    
    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions (e.g., connection error, timeout)
        error_message = f"Error making the request: {e}"
        return render(request, 'error.html', {'error_message': error_message})

    except Exception as e:
        # Handle other exceptions
        error_message

def get_background_color(weather_description):
    if "scattered clouds" in weather_description.lower():
        return "#d9d9d9"  # Light gray for cloudy weather
    elif "rain" in weather_description.lower():
        return "#85a3e0"  # Light blue for rainy weather
    elif "clear" in weather_description.lower():
        return "#87ceeb"  # Sky blue for clear weather
    else:
        return "#ffffff"  # Default to white background
    
class WeatherDataList(generics.ListCreateAPIView):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
