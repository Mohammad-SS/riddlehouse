
from django.shortcuts import render
from django.views import View

# Create your views here.


class LandingView(View):
    def get(self, request):
        return render(request, 'main/landing.html', {})
    
    

class RoomView(View):
    def get(self, request, pk):
        return render(request, 'main/reserveroom.html', {})