from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import CSV_load, dossier_form
from .models import import_dossiers, dossier, Note, Todo, Notification
from django.contrib.auth.models import User
from .utils import *
from django.db.models import Sum, Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import AccountAuthenticationForm, Create_Note
from django.shortcuts import render, redirect
from datetime import date
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        feder_form = CSV_load(request.POST, request.FILES)
        if feder_form.is_valid:
            import_dossiers.objects.all().delete()
            dossier.objects.all().delete()
            feder_form.save()
            Create_Dossiers()
            return redirect('report:index')
        else:
            feder_form = CSV_load()
            context = {'form': feder_form}
            print('fail')
            return render(request, 'report/index.html', context)
    else:
        feder_form = CSV_load()
        utilisateurs = User.objects.all()
        print(feder_form)
        print('test')
        projet = dossier.objects.all()
        todo = Todo.objects.all()
        notif = Notification.objects.filter(nature="note")
        nb_projets = dossier.objects.count()
        nb_waiting = dossier.objects.filter(result_next_step="WAITING FOR CUSTOMER").count()
        nb_closed_lost = dossier.objects.filter(result_next_step="CLOSED  LOST").count()
        nb_closed_win = dossier.objects.filter(result_next_step="CLOSED WIN").count()
        nb_waiting_for_sample = dossier.objects.filter(result_next_step="WAITING FOR SAMPLE & PRICING").count()
        Vol_vente = dossier.objects.aggregate(Sum('y_mb'))
        Vol_vente_kg = dossier.objects.aggregate(Sum('y_vol'))
        produits_boisson = list(dossier.objects.filter(channel="BOISSON").values_list('product').distinct())
        produits_confiserie = list(dossier.objects.filter(channel="CONFISERIE").values_list('product').distinct())

        context = {
            'form': feder_form,
            'utilisateurs': utilisateurs,
            'dossier':projet,
            'nb_projets':nb_projets,
            'todo':todo,
            'nb_waiting': nb_waiting,
            'nb_closed_lost':nb_closed_lost,
            'nb_closed_win':nb_closed_win,
            'nb_waiting_for_sample':nb_waiting_for_sample,
            'Vol_vente':Vol_vente,
            'Vol_vente_kg':Vol_vente_kg,
            'notif': notif,
        }

        return render(request, 'report/index.html', context)

@login_required
def add_dossier(request):
    if request.method == "POST":
        form = dossier_form(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Dossier ajouté !')
            form = dossier_form()
            files = dossier.objects.all()
            todo = Todo.objects.all()
            notif = Notification.objects.filter(nature="note")
            context = {'form': form, 'files':files, 'todo':todo, 'notif':notif}
            return render(request, 'report/add_dossier.html', context)
        else:
            context = {'form' : form}
            messages.add_message(request, messages.INFO, "Oups, il y' a une erreur dans le formulaire...")
            return render(request, 'report/add_dossier.html', context)
    else:
        form = dossier_form()
        files = dossier.objects.all()
        todo = Todo.objects.all()
        notif = Notification.objects.filter(nature="note")
        context = {'form':form, 'files':files, 'todo':todo, 'notif':notif}
        return render(request, 'report/add_dossier.html', context)


def delete(request, pk):
    dossier.objects.get(pk=pk).delete()
    messages.add_message(request, messages.INFO, 'Dossier supprimé !')
    return redirect('report:index')


def delete_note(request, pk, id):
    Note.objects.get(pk=pk).delete()
    messages.add_message(request, messages.INFO, 'Note supprimé !')
    next = request.POST.get('next', '/')
    return redirect('report:fiche_dossier', id)

@login_required
def fiche_dossier(request, pk):
    projet = dossier.objects.get(pk=pk)
    note = Note.objects.filter(identifier=pk)
    files = dossier.objects.all()
    todo = Todo.objects.all()
    notif = Notification.objects.filter(nature="note")
    context = {'dossier': projet, 'note':note, 'files':files, 'todo':todo, 'notif':notif}
    return render(request, 'report/dossier.html', context)


def Nouvelle_Note(request, pk):
    if request.method == "POST":
        User.objects.get(id=request.user.id)
        user = request.user
        note_op = request.POST.get('note')
        identifier = str(pk)
        file = dossier.objects.get(pk=pk).customer

        if len(note_op) != 0:
            Note.objects.create(identifier=identifier, note=note_op, user=user, date=date.today())
            Notification.objects.create(content=note_op, date=date.today(), nature="note", user=user, identifier=identifier, file=file)
            return redirect('report:fiche_dossier', identifier)
        else:
            return redirect('report:fiche_dossier', identifier)
    else:
        identifier = str(pk)
        return redirect('report:fiche_dossier', identifier)

def signIn(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("report:index")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect("report:index")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'report/authentification.html', context)

def signOut(request):
    logout(request)
    return redirect('report:signIn')

def add_Todo(request):
    if request.method == "POST":
        contenu = request.POST.get("content")
        Todo.objects.create(content=contenu, date=date.today(), done=False)
        Notification.objects.create(content=contenu, date=date.today(), nature="todo")
        return redirect('report:index')
    else:
        return redirect('report:index')

def done(request, pk):
    pk = pk
    todo = Todo.objects.get(pk=pk)
    Todo.objects.filter(pk=pk).update(done=True)
    Notification.objects.create(content="todo.content", date=date.today(), nature="done")
    return redirect('report:index')

class Report(View):
    def get(self, request, *args, **kwargs):
        template = get_template('report/report.html')
        dossiers = dossier.objects.all()
        nb_projets = dossier.objects.count()
        nb_waiting = dossier.objects.filter(result_next_step="WAITING FOR CUSTOMER").count()
        nb_closed_lost = dossier.objects.filter(result_next_step="CLOSED  LOST").count()
        nb_closed_win = dossier.objects.filter(result_next_step="CLOSED WIN").count()
        nb_waiting_for_sample = dossier.objects.filter(result_next_step="WAITING FOR SAMPLE & PRICING").count()
        Vol_vente = dossier.objects.aggregate(Sum('y_mb'))
        Vol_vente_kg = dossier.objects.aggregate(Sum('y_vol'))
        nb_projets = dossier.objects.count()

        context = {
            'dossiers': dossiers,
            'nb_waiting': nb_waiting,
            'nb_closed_lost': nb_closed_lost,
            'nb_closed_win': nb_closed_win,
            'nb_waiting_for_sample': nb_waiting_for_sample,
            'Vol_vente': Vol_vente,
            'Vol_vente_kg': Vol_vente_kg,
            'nb_projets' : nb_projets,
        }
        html = template.render(context)
        pdf = render_to_pdf('report/report.html', context)
        return pdf

def export_data(request):
    my_model_resource = MyModelResource()
    dataset = my_model_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Export.xls"'
    return response

def waiting(request, pk):
    pk = pk
    dossier.objects.filter(pk=pk).update(result_next_step="WAITING FOR CUSTOMER")
    return redirect('report:fiche_dossier', pk)

def CLOSED_LOST(request, pk):
    pk = pk
    dossier.objects.filter(pk=pk).update(result_next_step="CLOSED  LOST")
    return redirect('report:fiche_dossier', pk)

def CLOSED_WIN(request, pk):
    pk = pk
    dossier.objects.filter(pk=pk).update(result_next_step="CLOSED WIN")
    return redirect('report:fiche_dossier', pk)

def WAITING_FOR_SAMPLE(request, pk):
    pk = pk
    dossier.objects.filter(pk=pk).update(result_next_step="WAITING FOR SAMPLE & PRICING")
    return redirect('report:fiche_dossier', pk)
