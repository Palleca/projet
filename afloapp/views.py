from django.contrib.auth import authenticate
from django.contrib.auth import login as djangoLogin
from django.contrib.auth import logout as djangoLogout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import FormateurForm, FormationForm
from .models import Eleve, Formateur, Formation, Matiere


@login_required(login_url="login")
def home(request: HttpRequest) -> HttpResponse:
    context = { 
        "name": "Quentin", 
        "age": 30,
        "activities": [
            {
                "name": "Sport",
                "display": True
            },
            {
                "name": "Musique",
                "display": True
            }
        ]
    }
    return render(request, 'afloapp/pages/home.html', context)


### Formations

@login_required(login_url="login")
@permission_required(perm="afloapp.view_formation", login_url="home")  # type: ignore
def formations(request: HttpRequest) -> HttpResponse:
    formations = Formation.objects.all().order_by("-updatedAt")
    context = { "formations": formations }
    return render(request, 'afloapp/pages/formations.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.view_formation", login_url="home")  # type: ignore
def formation(request: HttpRequest, pk: int) -> HttpResponse:
    formation = Formation.objects.get(id=pk)
    eleves = Eleve.objects.filter(formation__id=pk)
    matieres = Matiere.objects.filter(formations__id=pk)
    context = { "formation": formation, "eleves": eleves, 'matieres': matieres }
    return render(request, 'afloapp/pages/formation.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.add_formation", login_url="formations")  # type: ignore
def create_formation(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FormationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('formations')
    form = FormationForm()
    context = { "form": form }
    return render(request, 'afloapp/pages/create-formation.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.change_formation", login_url="formations")  # type: ignore
def update_formation(request: HttpRequest, pk: int) -> HttpResponse:
    formation = Formation.objects.get(id=pk)
    if request.method == "POST":
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid:
            form.save()
            return redirect('formations')
    form = FormationForm(instance=formation)
    context = { "form": form }
    return render(request, 'afloapp/pages/update-formation.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.delete_formation", login_url="formations")  # type: ignore
def delete_formation(request: HttpRequest, pk: int) -> HttpResponse:
    formation = Formation.objects.get(id=pk)
    formation.delete()
    return redirect('formations')


### Formateurs


@login_required(login_url="login")
@permission_required(perm="afloapp.view_formateur", login_url="home")  # type: ignore
def formateurs(request: HttpRequest) -> HttpResponse:
    formateurs = Formateur.objects.all()
    context = { "formateurs": formateurs }
    return render(request, 'afloapp/pages/formateurs.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.view_formateur", login_url="home")  # type: ignore
def formateur(request: HttpRequest, pk: int) -> HttpResponse:
    formateur = Formateur.objects.get(id=pk)
    context = { "formateur": formateur }
    return render(request, 'afloapp/pages/formateur.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.add_formateur", login_url="formateurs")  # type: ignore
def create_formateur(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FormateurForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('formateurs')
    form = FormateurForm()
    context = { "form": form }
    return render(request, 'afloapp/pages/create-formateur.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.change_formateur", login_url="formateurs")  # type: ignore
def update_formateur(request: HttpRequest, pk: int) -> HttpResponse:
    formateur = Formateur.objects.get(id=pk)
    if request.method == "POST":
        form = FormateurForm(request.POST, instance=formateur)
        if form.is_valid:
            form.save()
            return redirect('formateurs')
    form = FormateurForm(instance=formateur)
    context = { "form": form }
    return render(request, 'afloapp/pages/update-formateur.html', context)


@login_required(login_url="login")
@permission_required(perm="afloapp.delete_formateur", login_url="formateurs")  # type: ignore
def delete_formateur(request: HttpRequest, pk: int) -> HttpResponse:
    formateur = Formateur.objects.get(id=pk)
    formateur.delete()
    return redirect('formations')


@login_required(login_url="login")
@permission_required(perm="afloapp.change_formation", login_url="formateurs")  # type: ignore
def remove_responsability(request: HttpRequest, pk: int) -> HttpResponse:
    formation = Formation.objects.get(responsable_id=pk)
    formation.responsable = None
    formation.save()
    return redirect('formateurs')


### Others


def about(request: HttpRequest) -> HttpResponse:
    context = { "name": "Quentin" }
    return render(request, 'afloapp/pages/about.html', context)


def contact(request: HttpRequest) -> HttpResponse:
    context = { "name": "Quentin" }
    return render(request, 'afloapp/pages/contact.html', context)


### Authentication


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is None:
            return redirect('login')
        else:
            djangoLogin(request, user)
            return redirect('home')
        
    return render(request, 'afloapp/pages/login.html')


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid:
            user = form.save()
            group = Group.objects.get(name="BasicUser")
            user.groups.add(group)
            return redirect('login')
    form = UserCreationForm()
    context = { "form": form }
    return render(request, 'afloapp/pages/register.html', context)


@login_required(login_url="login")
def logout(request: HttpRequest) -> HttpResponse:
    djangoLogout(request)
    return redirect('login')
