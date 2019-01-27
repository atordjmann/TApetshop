from django.db import models

STATE_CHOICES = (('affamé', 'affamé'), ('fatigué', 'fatigué'), ('repus', 'repus'), ('endormi', 'endormi'))

AVAILABILITY_CHOICES = (("libre", "libre"), ('occupé', 'occupé'))


class Equipement(models.Model):
    name = models.CharField(max_length=200)
    availability = models.CharField(max_length=200, choices=AVAILABILITY_CHOICES)

    def __str__(self):
        return self.name

    def verifie_disponibilite(self):
        return self.availability

    def cherche_occupant(self):
        return self.animal_set.all()[0].name


class Animal(models.Model):
    place = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    race = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    state = models.CharField(max_length=200, choices=STATE_CHOICES)

    def __str__(self):
        return self.name

    def lit_etat(self):
        return self.state

    def lit_lieu(self):
        return self.place

    def change_etat(self, etat):
        liste_etat = ['affamé', 'fatigué', 'repus', 'endormi']
        if etat in liste_etat:
            self.state = etat
            self.save()

    def change_lieu(self, lieu):
        old_equipment = Equipement.objects.get(name=self.place)
        equipement = Equipement.objects.get(name=lieu)
        if equipement.availability != 'occupé':
            self.place = equipement
            if lieu != 'litière':
                equipement.availability = 'occupé'
            old_equipment.availability = 'libre'
            equipement.save()
            old_equipment.save()
            self.save()
