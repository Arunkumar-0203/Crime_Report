from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from Crime.models import Criminals, PoliceReg, fir_reg, UserReg


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/police_index.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)

        criminal = Criminals.objects.filter(police__login=self.request.user.id).count()
        m = fir_reg.objects.filter(status='approved',police__login=self.request.user.id).count()
        context['m'] =  m
        context['criminal'] =  criminal

        return context

class AddCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/add_criminals.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        addre = request.POST['addre']
        con = request.POST['con']
        age = request.POST['age']
        image = request.FILES['image']

        ps = PoliceReg.objects.get(login_id=self.request.user.id)

        s = Criminals()
        s.address = addre
        s.name = name
        s.contact = con
        s.age = age
        s.image = image
        s.police = ps
        s.save()

        messages = "Added Successfully"
        return render(request,'police_staff/add_criminals.html',{'message':messages})

class ViewCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_criminals.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewCriminals,self).get_context_data(**kwargs)
        cri = Criminals.objects.all()

        context['cri'] = cri

        return context


class DeleteCriminals(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['c_id']
        user = Criminals.objects.get(pk=id).delete()
        return render(request,'police_staff/view_criminals.html',{'message':"Criminals Removed"})


# class ProfileView(LoginRequiredMixin,TemplateView):
#     template_name = 'police_staff/profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileView,self).get_context_data(**kwargs)
#         pl = PoliceReg.objects.get(login_id=self.request.user.id)
#
#         context['pl'] = pl
#
#         return context


class ApproveFIR(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/approve.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ApproveFIR, self).get_context_data(**kwargs)
        m = fir_reg.objects.filter(police__login=self.request.user.id,status='pending')

        context['m'] = m
        return context

class ApprFIR(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = fir_reg.objects.get(pk=id)
        user.status='approved'

        user.save()
        return render(request,'police_staff/police_index.html',{'message':"FIR Approved"})

class RejectFIR(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = fir_reg.objects.get(pk=id)
        user.status='declined'

        user.save()
        return render(request,'police_staff/police_index.html',{'message':"FIR Declined"})


class ViewFIR(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_fir.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewFIR, self).get_context_data(**kwargs)
        m = fir_reg.objects.filter(police__login=self.request.user.id,status='approved')

        context['m'] = m
        return context

    def post(self, request, *args, **kwargs):
        charge = request.FILES['charge']
        fir = request.POST['fir']



        s = fir_reg.objects.get(pk=fir)
        s.charge = charge
        s.save()

        messages = "Added Successfully"
        return render(request,'police_staff/police_index.html',{'message':messages})

class ViewUser(LoginRequiredMixin,TemplateView):
    template_name = 'police_staff/view_user.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewUser, self).get_context_data(**kwargs)
        id = self.request.GET['id']
        m = UserReg.objects.filter(pk=id)

        context['m'] = m
        return context