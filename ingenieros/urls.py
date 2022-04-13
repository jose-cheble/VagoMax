from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.IndexView.as_view(), name="index_page"),
    path("new-user", views.CreateUserView.as_view(), name="new_user_page"),
    path("my-machines", views.MyMachinesView.as_view(), name="my_machines_page"),
    path("my-machines/<slug:slug>", views.MachineDetailView.as_view(), name="detail_page"),
    path("add-machine", views.AddMachineView.as_view(), name="add_machine_page"),
    path("add_inspection/<slug:slug>",views.AddinspectionView.as_view() ,name="add_inspection_page"),
    path("my-profile", views.MyProfileView.as_view(), name="my_profile_page"),
    path("login", LoginView.as_view(template_name="ingenieros/login.html"), name="login_page"),
    path("logout", LogoutView.as_view(template_name="ingenieros/logout.html"), name="logout_page")
]