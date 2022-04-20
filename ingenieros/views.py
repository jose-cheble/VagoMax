from datetime import datetime
from multiprocessing import context
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from .models import EquiposModel, InspeccionesModel
from .forms import NuevaInspeccionForm, NuevoEquipoForm, UserRegisterForm
from datetime import date, datetime
from django.db import IntegrityError
from django.utils.text import slugify



# Create your views here.


class IndexView(View):

    def get(self, request):
        return render(request, "ingenieros/index.html")

    def post(self, request):
        return render(request, "ingenieros/index.html")

class CreateUserView(View):

    def get(self, request):
        form = UserRegisterForm()
        return render(request, "ingenieros/create-user.html",{ 
        "form" : form
        })
        
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data["username"]
            messages.success(request, f"usuario:{user_name} ha sido creado", {
                "form" : form
            })
            return HttpResponseRedirect(reverse("my_profile_page"))

        return render(request, "ingenieros/create-user.html",{ 
            "form" : form
            })

class MyMachinesView(View):

    def get(self, request):
        if request.user.is_authenticated:
            users_machines = EquiposModel.objects.all().filter(ingeniero=request.user)
            return render(request, "ingenieros/my-machines.html", {
                "all_machines": users_machines
            })
        else: 
            return HttpResponseRedirect(reverse("login_page"))


class MachineDetailView(View):
    def get(self, request, slug):
        machine = EquiposModel.objects.get(slug=slug)
        inspections = machine.inspections.all().order_by("-fecha")
        return render(request, "ingenieros/detail.html", {
            "machine": machine,
            "inspections": inspections
        })

    def post(self, request, slug):
        return HttpResponseRedirect(reverse("add_inspection_page", args=[slug]))

class AddMachineView(View):
    
    def get(self, request):
        new_machine_form = NuevoEquipoForm()
        return render(request, "ingenieros/add-machine.html", {
            "form" : new_machine_form
        })

    def post(self, request):
        if request.user.is_authenticated:
            new_machine_form = NuevoEquipoForm(request.POST)
            if new_machine_form.is_valid():
                new_machine = new_machine_form.save(commit=False)
                try:
                    new_machine.ingeniero = request.user
                    new_machine.save()
                    print(new_machine.ingeniero)
                except IntegrityError:
                    return render(request, "ingenieros/add-machine.html", {
                        "form" : new_machine_form,
                        "message": "El equipo ya existe, revisar los datos."
                    })
                else:
                    return HttpResponseRedirect(reverse("my_machines_page"))
        else: 
            return HttpResponseRedirect(reverse("login_page"))


class AddinspectionView(View):
    
    def get(self, request, slug):
        machine = EquiposModel.objects.get(slug=slug)
        inspection_form = NuevaInspeccionForm()
        inspection_form.set_initial(slug)
        return render(request, "ingenieros/add-inspection.html", {
            "machine": machine,
            "form": inspection_form,
        })

    def post(self, request, slug):
        machine = EquiposModel.objects.get(slug=slug)
        inspection_form = NuevaInspeccionForm(request.POST)
        last_inspection = machine.inspections.last()
        pagina = machine.pagina_numero
        print(last_inspection, pagina)
        if inspection_form.is_valid() and request.user.is_authenticated:
            machine.pagina_numero = request.POST["pagina"]
            machine.save()
            new_inspection = InspeccionesModel(
                equipo = machine,
                fecha = datetime.now(),
                observacion = request.POST["observacion"],
                pagina_numero = request.POST["pagina"]
            )
            new_inspection.save()

            return HttpResponseRedirect(reverse("detail_page", args=[slug]))
        
        context = {
            "machine": machine,
            "form": inspection_form
        }
        return render(request, "ingenieros/add-inspection.html", context)


class MyProfileView(View):

    
    def get(self, request):
        if request.user.is_authenticated:
            user_machines = EquiposModel.objects.all().filter(ingeniero=request.user)
            number_user_machines = user_machines.count()
            this_month_inspections = 0
            for machine in user_machines:
                if machine.inspections.last() != None:
                    if machine.inspections.last().fecha.month == datetime.now().month:
                        this_month_inspections += 1
            this_month_perc = this_month_inspections / number_user_machines * 100
                        
            return render(request, "ingenieros/my-profile.html", {
                "user_machines" : number_user_machines,
                "this_month_perc" : this_month_perc
            })
        else:
            return HttpResponseRedirect(reverse("login_page"))

    def post(self, request):
        if request.user.is_authenticated:
            return render(request, "ingenieros/my-profile.html")
        else:
            return HttpResponseRedirect(reverse("login_page"))


    