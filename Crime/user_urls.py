from django.urls import path

from Crime.user_views import IndexView, ViewCriminals, AddFeedback, SelectStation, FIR_reg, ViewFIR
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',IndexView.as_view()),
    path('ViewCriminals',ViewCriminals.as_view()),
    path('AddFeedback',AddFeedback.as_view()),
    path('SelectStation',SelectStation.as_view()),
    path('FIR_reg',FIR_reg.as_view()),
    path('ViewFIR',ViewFIR.as_view()),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),


]
def urls():
      return urlpatterns,'user','user'