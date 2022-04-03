from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Student, Worker, Complaint


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(User.objects.all())]
    )
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = (
            "id",
            "email",
            "username",
            "password",
            "password2",
            "contact_number",
            "roll_number",
            "room_number",
            "usertype",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            error_message = {"registration failed": "passwords must match"}
            raise serializers.ValidationError(error_message)
        password_validation.validate_password(attrs["password"])
        return attrs


class StudentRegisterSerializer(UserRegisterSerializer):
    class Meta(UserRegisterSerializer.Meta):
        model = Student

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        student = Student.objects.create(username=username, email=email)
        student.set_password(validated_data["password"])
        student.contact_number = validated_data["contact_number"]
        student.roll_number = validated_data["roll_number"]
        student.room_number = validated_data["room_number"]
        student.save()
        return student


class WorkerRegisterSerializer(UserRegisterSerializer):
    class Meta(UserRegisterSerializer.Meta):
        model = Worker

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        worker = Worker.objects.create(username=username, email=email)
        worker.set_password(validated_data["password"])
        worker.usertype = validated_data["usertype"]
        worker.contact_number = validated_data["contact_number"]
        worker.save()
        return worker


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "contact_number",
            "roll_number",
            "room_number",
            "usertype",
        )


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    model = User

    def validate(self, attrs):
        new_pass = attrs["new_password"]
        new_pass_confirm = attrs["new_password_confirm"]
        if new_pass != new_pass_confirm:
            message = {"new_password_confirm": "new password fields must match"}
            raise serializers.ValidationError(message)
        password_validation.validate_password(new_pass)
        return attrs


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"
