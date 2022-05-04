
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from Crime.models import Criminals, Feedback, UserReg, PoliceReg, fir_reg


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_index.html'
    login_url = '/'

class ViewCriminals(LoginRequiredMixin,TemplateView):
    template_name = 'user/view_criminals.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewCriminals,self).get_context_data(**kwargs)
        cri = Criminals.objects.all()
        context['cri'] = cri
        return context

class AddFeedback(LoginRequiredMixin,TemplateView):
    template_name = 'user/feedback.html'
    login_url = '/'

    def post(self, request, *args, **kwargs):
        f = request.POST['feed']

        ps = UserReg.objects.get(login_id=self.request.user.id)

        s = Feedback()
        s.feedback = f
        s.user = ps
        s.save()

        messages = "Added Successfully"
        return render(request,'user/feedback.html',{'message':messages})

class SelectStation(LoginRequiredMixin,TemplateView):
    template_name = 'user/select_sation.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(SelectStation, self).get_context_data(**kwargs)
        staff = PoliceReg.objects.filter(login__last_name='1', login__is_staff='0')
        context['staff'] = staff
        return context

class FIR_reg(LoginRequiredMixin,TemplateView):
    template_name = 'user/fir_reg.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(FIR_reg, self).get_context_data(**kwargs)
        st = self.request.GET['st']
        ps = UserReg.objects.get(login_id=self.request.user.id)

        context['st'] = st
        context['ps'] = ps
        return context

    def post(self, request, *args, **kwargs):
        st = request.POST['st']
        timee = request.POST['timee']
        date = request.POST['date']
        complaint = request.POST['complaint']

        ps = UserReg.objects.get(login_id=self.request.user.id)
        pl = PoliceReg.objects.get(pk=st)

        s = fir_reg()
        s.police = pl
        s.user = ps
        s.complaint = complaint
        s.timee = timee
        s.c_date = date
        s.status = 'pending'
        s.save()

        messages = "Registered Successfully"
        return render(request,'user/user_index.html',{'message':messages})


class ViewFIR(LoginRequiredMixin,TemplateView):
    template_name = 'user/view_fir.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewFIR, self).get_context_data(**kwargs)
        m = fir_reg.objects.filter(user__login=self.request.user.id)

        context['m'] = m
        return context