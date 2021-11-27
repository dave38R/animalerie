from django.shortcuts import render
from .models import Animal, Equipement


# Create your views here.
def post_list(request):
    animals = Animal.objects.all()
    equipement = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'animals': animals, 'equipement': equipement})
