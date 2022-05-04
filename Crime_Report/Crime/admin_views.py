from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from Crime.models import PoliceStation, PoliceReg, UserReg, Criminals, Feedback, fir_reg


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'admin/admin_index.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        staff = PoliceReg.objects.filter(login__last_name='1',login__is_staff='0').count()
        user = UserReg.objects.filter(login__last_name='1',login__is_staff='0').count()
        criminal = Criminals.objects.all().count()
        m = fir_reg.objects.filter(status='approved').count()
        context['m'] =  m
        context['criminal'] =  criminal
        context['user'] =  user
        context['staff'] =  staff
        return context

class AddStation(LoginRequiredMixin,TemplateView):
    template_name = 'admin/add_station.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):
        station = request.POST['station']

        s = PoliceStation()
        s.station_name = station
        s.save()

        messages = "Added Successfully"
        return render(request,'admin/add_station.html',{'message':messages})

class ViewStation(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_station.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewStation,self).get_context_data(**kwargs)
        p = PoliceStation.objects.all()

        context['p'] = p

        return context

class DeletePolice(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['ps_id']
        user = PoliceStation.objects.get(pk=id).delete()
        return render(request,'admin/admin_index.html',{'message':"Station Removed"})

class NewStation(LoginRequiredMixin,TemplateView):
    template_name = 'admin/approve_staff.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(NewStation,self).get_context_data(**kwargs)
        staff = PoliceReg.objects.filter(login__last_name='0',login__is_staff='0')
        context['staff'] =  staff
        return context

class RejectView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='0'
        user.is_active='0'
        user.save()
        return render(request,'admin/admin_index.html',{'message':"Account Removed"})

class ApproveView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'

        user.save()
        return render(request,'admin/admin_index.html',{'message':"Account Activated"})

class ApprovedStation(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_staff.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super(ApprovedStation,self).get_context_data(**kwargs)
        staff = PoliceReg.objects.filter(login__last_name='1',login__is_staff='0')
        context['staff'] =  staff
        return context

class ViewCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_criminals.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewCriminals,self).get_context_data(**kwargs)
        cri = Criminals.objects.all()

        context['cri'] = cri

        return context

    def post(self, request, *args, **kwargs):
        # template = loader.get_template('user/store.html')
        search = self.request.POST['search']
        cri = Criminals.objects.filter(name__icontains=search) | Criminals.objects.filter(address__contains=search)
        # return HttpResponse(template.render({"train": train}))
        return render(request,'admin/view_criminals.html',{'cri':cri})

class ViewFeed(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_feedback.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewFeed,self).get_context_data(**kwargs)
        f = Feedback.objects.all()

        context['feed'] = f

        return context


class ViewUser(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_user.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewUser, self).get_context_data(**kwargs)
        id = self.request.GET['id']
        m = UserReg.objects.filter(pk=id)

        context['m'] = m
        return context

class ViewFIR(LoginRequiredMixin,TemplateView):
    template_name = 'admin/view_fir.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewFIR, self).get_context_data(**kwargs)
        m = fir_reg.objects.all()
        try:
            search = self.request.GET['search']
            m = fir_reg.objects.filter(user__location__contains=search) | fir_reg.objects.filter(complaint__contains=search)
            context['m'] = m
        except:

            context['m'] = m
        return context