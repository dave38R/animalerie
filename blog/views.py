from django.shortcuts import render, get_object_or_404, redirect
from forms import MoveForm
from .models import Animal, Equipement


# Create your views here.
def animal_list(request):
    animals = Animal.objects.all()
    equipement = Equipement.objects.all()
    return render(request, 'blog/base.html', {'animals': animals, 'equipement': equipement})


def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)

    form = MoveForm(request.POST, instance=animal)

    if form.is_valid():
        form.save(commit=False)
        if animal.lieu.disponibilite == 'libre':
            animal.save()
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            if animal.lieu.id_equip != 'litière':
                animal.disponibilite = "occupé"
            if animal.lieu.id_equip == 'nid':
                animal.etat = 'endormi'
            if animal.lieu.id_equip == 'litière':
                animal.etat = 'affamé'
            if animal.lieu.id_equip == 'mangeoire':
                animal.etat = 'repus'
            if animal.lieu.id_equip == 'roue':
                animal.etat = 'fatigué'
            animal.save()



            return redirect('animal_detail', id_animal=id_animal)

        else:
            animal.lieu = ancien_lieu
            return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form,
                   'message': "Le lieu indiqué est déjà occupé"})




    else:
        form = MoveForm()
        return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form})



