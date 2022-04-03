from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    # ComplaintListView,
    StudentRegisterView,
    WorkerRegisterView,
    UserLogoutView,
    UserDetailView,
    PasswordChangeView,
    ComplaintCreateView,
    ComplaintDetailView,
    ComplaintListPendingView,
    ComplaintListDoneView,
)

urlpatterns = [
    path("student/signup", StudentRegisterView.as_view()),
    path("worker/signup", WorkerRegisterView.as_view()),
    path("login", obtain_auth_token),
    path("logout", UserLogoutView.as_view()),
    path("authdetail/<str:username>", UserDetailView.as_view()),
    path("changepassword", PasswordChangeView.as_view()),
    path("complaint/new", ComplaintCreateView.as_view()),
    path("complaint/<int:pk>", ComplaintDetailView.as_view()),
    # path("complaint/<str:username>/all", ComplaintListView.as_view()),
    path("complaint/pending", ComplaintListPendingView.as_view()),
    path("complaint/done", ComplaintListDoneView.as_view()),
]
