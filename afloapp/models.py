from django.db import models


class Formateur(models.Model):
    nom = models.CharField(max_length=30)
    specicialite = models.CharField(max_length=20, default="Informatique")

    def __str__(self) -> str:
        return f"{self.nom}"
    

class Formation(models.Model):
    nom = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    diplomante = models.BooleanField(default=True)

    responsable = models.OneToOneField(
        Formateur, 
        related_name="formation", 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.nom}"
    

class Matiere(models.Model):
    nom = models.CharField(max_length=30)
    difficulte = models.IntegerField()

    formations = models.ManyToManyField(Formation, related_name="matieres")

    def __str__(self) -> str:
        return f"{self.nom}"
    

class Eleve(models.Model):
    nom = models.CharField(max_length=30)

    formation = models.ForeignKey(
        Formation, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )
    
    def __str__(self) -> str:
        return f"{self.nom}"