from pyexpat import model
from ikhedut.models import Ad, CropSale,Contact,Order
from rest_framework import serializers

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
            "total_amount", # Ensure this has a comma before it
        ]

    def validate(self, data):
        payment_method = data.get("payment_method")

        if payment_method == "CARD":
            required = ["cardholdername","card_number", "card_expiry", "card_cvv"]
            for field in required:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field} is required for card payment")

        if payment_method == "UPI" and not data.get("upi_id"):
            raise serializers.ValidationError("UPI ID is required for UPI payment")

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
        
