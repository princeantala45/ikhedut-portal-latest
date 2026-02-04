from ikhedut.models import Ad, CropSale,Contact,Order, Signup
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class Cropsaleserializers(serializers.ModelSerializer):
    class Meta:
        model = CropSale
        exclude = ["seller", "is_approved"]


class Conactserializers(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields='__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "fullname",
            "mobile",
            "city",
            "pincode",
            "address",
            "payment_method",
            "cardholdername",
            "card_number",
            "card_expiry",
            "card_cvv",
            "upi_id",
        ]

    def validate(self, data):
        payment_method = data.get("payment_method")

        if payment_method == "CARD":
            required = ["cardholdername", "card_number", "card_expiry", "card_cvv"]
            for field in required:
                if not data.get(field):
                    raise serializers.ValidationError({
                        field: "This field is required for card payment"
                    })

        if payment_method == "UPI" and not data.get("upi_id"):
            raise serializers.ValidationError({
                "upi_id": "UPI ID is required for UPI payment"
            })

        return data
       
class PostAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            "id",
            "fullname",
            "mobile",
            "state",
            "city",
            "productname",
            "description",
            "price",
            "image",
            "is_approved",
        ]
        read_only_fields = ["is_approved"]
        
class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repassword = serializers.CharField(write_only=True, required=True)
    mobile = serializers.CharField(write_only=True, required=True)
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repassword", "mobile", "image"]

    def validate(self, data):
        if data["password"] != data["repassword"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })

        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({
                "username": "Username already exists"
            })

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "email": "Email already exists"
            })

        return data

    def create(self, validated_data):
        validated_data.pop("repassword")
        mobile = validated_data.pop("mobile")
        image = validated_data.pop("image")
        password = validated_data.pop("password")

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(password)
        user.save()

        Signup.objects.create(
            user=user,
            mobile=mobile,
            image=image
        )

        return user
