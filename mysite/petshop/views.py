from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Animal, Equipement


def index(request):
    animals_list = Animal.objects.order_by('name')
    equipment_list = Equipement.objects.order_by('name')
    context = {
        'animals_list': animals_list,
        'equipment_list':equipment_list,
    }
    return render(request, 'petshop/index.html', context)


def nourrir(animal):
    if animal.lit_etat() is not None:
        mangeoire = Equipement.objects.get(name="mangeoire")
        if animal.lit_etat() != 'affamé':
            return "Désolé, " + str(animal.name) + " n'a pas faim..."
        elif mangeoire.verifie_disponibilite() != 'libre':
            occupant = mangeoire.cherche_occupant()
            return 'Désolé, la mangeoire est occupée par ' + str(occupant)
        else:
            animal.change_etat('repus')
            animal.change_lieu('mangeoire')
    else:
        return "Désolé, " + str(animal.name) + " n'est pas un animal connu"


def divertir(animal):
    if animal.lit_etat() is not None:
        roue = Equipement.objects.get(name="roue")
        if animal.lit_etat() != 'repus':
            return 'Désolé,'+str(animal.name) + " n'est pas en état de faire du sport."
        elif roue.verifie_disponibilite() != 'libre':
            occupant = roue.cherche_occupant()
            return 'Désolé, la roue est occupée par ' + str(occupant)
        else:
            animal.change_etat('fatigué')
            animal.change_lieu('roue')
    else:
        return "Désolé, " + str(animal.name) + " n'est pas un animal connu"


def coucher(animal):
    if animal.lit_etat() is not None:
        nid = Equipement.objects.get(name="nid")
        if animal.lit_etat() != 'fatigué':
            return "Désolé, " + str(animal.name) + " n'est pas fatigué."
        elif nid.verifie_disponibilite() != 'libre':
            occupant = nid.cherche_occupant()
            return 'Désolé, le nid est occupé par ' + str(occupant)
        else:
            animal.change_etat('endormi')
            animal.change_lieu('nid')
    else:
        return "Désolé, " + str(animal.name) + " n'est pas un animal connu"


def reveiller(animal):
    if animal.lit_etat() is not None:
        if animal.lit_etat() != 'endormi':
            return "Désolé, " + str(animal.name) + " ne dort pas."
        else:
            animal.change_etat('affamé')
            animal.change_lieu('litière')
    else:
        return "Désolé, " + str(animal.name) + " n'est pas un animal connu"



def modify(request):

    try:
        selected_animal = request.POST['animal']
        selected_action = request.POST['action']
    except (KeyError, Animal.DoesNotExist):
        messages.info(request, "Vous devez selectionner un animal et une action")
    else:
        animal = Animal.objects.get(pk=selected_animal)
        if selected_action == "nourrir":
            messages.info(request, nourrir(animal))
        if selected_action == "divertir":
            messages.info(request, divertir(animal))
        if selected_action == "coucher":
            messages.info(request, coucher(animal))
        if selected_action == "reveiller":
            messages.info(request, reveiller(animal))

    return HttpResponseRedirect(reverse('petshop:index'))
