from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import User, Student, Worker, Complaint
from .serializers import (
    StudentRegisterSerializer,
    WorkerRegisterSerializer,
    UserSerializer,
    PasswordChangeSerializer,
    ComplaintSerializer,
)


class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data=serializer.data)
        data = dict(serializer.data)
        data["token"] = Token.objects.get(user=data["id"]).key
        return Response(data=data, status=HTTP_201_CREATED, headers=headers)


class StudentRegisterView(UserRegisterView):
    serializer_class = StudentRegisterSerializer
    queryset = Student.objects.all()


class WorkerRegisterView(UserRegisterView):
    serializer_class = WorkerRegisterSerializer
    queryset = Worker.objects.all()


class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=HTTP_200_OK)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all().filter(is_staff=False)
    lookup_field = "username"

    def update(self, request, *args, **kwargs):
        if kwargs["username"] != request.user.username:
            message = {"update failed": "permission denied"}
            return Response(data=message, status=HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if kwargs["username"] != request.user.username:
            message = {"update failed": "permission denied"}
            return Response(data=message, status=HTTP_401_UNAUTHORIZED)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if kwargs["username"] != request.user.username:
            message = {"deletion failed": "permission denied"}
            return Response(data=message, status=HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)


class PasswordChangeView(UpdateAPIView):
    model = User
    serializer_class = PasswordChangeSerializer

    def update(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_pass = serializer.data.get("old_password")
        if not self.object.check_password(old_pass):
            message = {"old_password": "Incorrect password"}
            return Response(data=message, status=HTTP_400_BAD_REQUEST)
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        message = {"success": "password updated"}
        return Response(data=message, status=HTTP_200_OK)


class ComplaintCreateView(APIView):
    def post(self, request):
        if request.user.usertype != User.Types.STUDENT:
            message = {"operation failed": "worker cannot lodge complaint"}
            return Response(message, HTTP_401_UNAUTHORIZED)
        complaint = Complaint(student=request.user)
        serializer = ComplaintSerializer(complaint, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class ComplaintDetailView(RetrieveUpdateDestroyAPIView):
    model = Complaint
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()

    def update(self, request, *args, **kwargs):
        complaint = Complaint.objects.get(id=kwargs["pk"])
        if request.user != complaint.student:
            message = {"update failed": "unauthorized access"}
            return Response(message, HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        complaint = Complaint.objects.get(id=kwargs["pk"])
        if request.user != complaint.student:
            message = {"update failed": "unauthorized access"}
            return Response(message, HTTP_401_UNAUTHORIZED)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        complaint = Complaint.objects.get(id=kwargs["pk"])
        if request.user != complaint.student:
            message = {"deletion failed": "unauthorized access"}
            return Response(message, HTTP_401_UNAUTHORIZED)
        if complaint.mark_done:
            message = {"deletion failed": "complaint marked as done"}
            return Response(message, HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)


# class ComplaintListView(ListAPIView):
#     serializer_class = ComplaintSerializer
#     queryset = Complaint.objects.all()

#     def get_queryset(self):
#         if self.request.user.usertype == User.Types.STUDENT:
#             return self.queryset.filter(student__username=self.request.user.username)
#         return self.queryset.filter(worker__username=self.request.user.username)


class ComplaintListPendingView(ListAPIView):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()

    def get_queryset(self):
        if self.request.user.usertype == User.Types.STUDENT:
            return self.queryset.filter(student=self.request.user, mark_done=False)
        return self.queryset.filter(type=self.request.user.usertype, mark_done=False)


class ComplaintListDoneView(ListAPIView):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()

    def get_queryset(self):
        if self.request.user.usertype == User.Types.STUDENT:
            return self.queryset.filter(student=self.request.user, mark_done=True)
        return self.queryset.filter(type=self.request.user.usertype, mark_done=True)
