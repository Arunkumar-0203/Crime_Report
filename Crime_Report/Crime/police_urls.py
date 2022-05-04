from django.urls import path

from Crime.police_views import IndexView, AddCriminals, ViewCriminals, DeleteCriminals, ApproveFIR, ApprFIR, RejectFIR, \
    ViewFIR, ViewUser
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('',IndexView.as_view()),
    path('AddCriminals',AddCriminals.as_view()),
    path('ViewCriminals',ViewCriminals.as_view()),
    path('DeleteCriminals',DeleteCriminals.as_view()),
    path('ApproveFIR',ApproveFIR.as_view()),
    path('ApprFIR',ApprFIR.as_view()),
    path('RejectFIR',RejectFIR.as_view()),
    path('ViewFIR',ViewFIR.as_view()),
    path('ViewUser',ViewUser.as_view()),
    # path('ProfileView',ProfileView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
        ),
        name='logout'
    ),


]
def urls():
      return urlpatterns,'police','police'