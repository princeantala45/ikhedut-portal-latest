from .models import *
from django.db import transaction
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import viewsets,serializers
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .serializer import *
from django.db.models import Sum, Min
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response  import Response
from rest_framework import status
from .models import CropSale
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login


from .models import *
from .serializer import *


@login_required
def postadvertisement(request):
   return render(request,'postadvertisement.html')
class SellCropsGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset=CropSale.objects.all()
    serializer_class=Cropsaleserializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
class SellCropsGeneric1(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset=CropSale.objects.all()
    serializer_class=Cropsaleserializers
    lookup_field='id'

class PostAdGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset=Ad.objects.all()
    serializer_class=PostAdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostAdGeneric1(generics.ListAPIView,generics.CreateAPIView):
    queryset=Ad.objects.all()
    serializer_class=PostAdvertisementSerializer
    lookup_field='id'

    
class RegistrerUser(APIView):
    authentication_classes = []   
    permission_classes = [AllowAny]
    parser_classes = [JSONParser,MultiPartParser, FormParser]

    def post(self, request):

        serializer = UserSerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=201
        )


def login_page(request):
    return render(request, "login.html")


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password")
    )

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    login(request, user)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username
    })
    
@login_required
def sellcrops_page(request):
    return render(request, "sellcrops.html")
@permission_classes([IsAuthenticated])
class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = Conactserializers
    permission_classes = [IsAuthenticated]

@login_required
def contact(request):
    return render(request,"contact.html")
    
def index(request):
    crops = CropSale.objects.filter(is_approved=True)
    return render(request, "index.html", {"crops": crops})

def crops(request):
    return render(request,"crops.html")

def agricultureguidance(request):
    return render(request,"agricultureguidance.html")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def buy_crops_api(request):
    sales = CropSale.objects.filter(is_approved=True)

    crops = {}

    for sale in sales:
        key = sale.crop.capitalize().strip()

        if key not in crops:
            crops[key] = {
                "crop": sale.crop,
                "total_quantity": sale.quantity,
                "price": sale.price,
                "image": sale.image.url if sale.image else "",
            }
        else:
            crops[key]["total_quantity"] += sale.quantity
            crops[key]["price"] = min(crops[key]["price"], sale.price)

    return Response(list(crops.values()))

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    items = []
    total = 0

    if cart:
        items = cart.items.select_related("product")
        total = sum(item.subtotal for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total,
        "cart_created_at": cart.created_at if cart else None
    })

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    items = cart.items.select_related("product")
    total = sum(item.subtotal for item in items)

    return render(request, "checkout.html", {
        "items": items,
        "total": total,
    })

@login_required
def buycrops(request):
    return render(request, "buycrops.html")

def tractor(request):
    return render(request,"tractor.html")

def tillage(request):
    return render(request,"tillage.html")

def ox(request):
    return render(request,"ox.html")

def agrochemicals(request):
    return render(request,"agrochemicals.html")

def fertilizer(request):
    return render(request,"fertilizer.html")

def signup(request):
    return render(request,"signup.html")

def logout(request):
    auth_logout(request)
    return render(request, "logout.html")


def remove_from_cart(request, item_id):
    item = get_object_or_404(Cartitems, id=item_id)

    product = item.product
    qty = item.quantity

    with transaction.atomic():
        
        if product:
            product.quantity += qty
            product.save()

        item.delete()

    messages.success(request, "Item removed from cart")
    return redirect("cart")

@require_POST
def expire_cart_item(request, item_id):
    cart_item = get_object_or_404(
        Cartitems,
        id=item_id,
        cart__user=request.user
    )

    product = cart_item.product
    qty = cart_item.quantity

    with transaction.atomic():
        # restore stock
        if product:
            product.quantity += qty
            product.save()

        # delete cart item
        cart_item.delete()

    return JsonResponse({"status": "expired"})

@login_required
def postedadvertisement(request):
    order = request.GET.get("order", "new")

    if order == "old":
        ads = Ad.objects.filter(is_approved=True).order_by("id")
    else:
        ads = Ad.objects.filter(is_approved=True).order_by("-id")

    return render(request, "postedadvertisement.html", {
        "ads": ads,
        "order": order,
    })


@require_POST
def delete_advertisement(request, id):
    ad = get_object_or_404(
        Ad,
        id=id,
        user=request.user
    )
    ad.delete()
    messages.success(request, "Advertisement deleted successfully.")
    return redirect("userprofile")


def order_success(request):
    return render(request, "order_success.html")

def spraypump(request):
    return render(request,'spraypump.html')

@login_required
def userprofile(request):
    user = request.user

    profile = Signup.objects.filter(user=user).first()
    crop_sales = CropSale.objects.filter(seller=user).order_by("-id")
    orders = Order.objects.filter(user=user).order_by("-created_at")
    ads = Ad.objects.filter(user=user).order_by("-id")

    return render(request, "userprofile.html", {
        "profile": profile,
        "crop_sales": crop_sales,
        "orders": orders,
        "ads": ads,
    })
 
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel():
        messages.error(request, "Order can no longer be cancelled.")
        return redirect("userprofile")

    order.status = "cancelled"
    order.save()

    messages.success(request, "Order cancelled successfully.")
    return redirect("userprofile")

def request_cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel():
        messages.error(request, "Cancellation time expired.")
        return redirect("userprofile")

    order.status = "cancel_requested"
    order.cancel_requested_at = timezone.now()
    order.save()

    messages.success(request,"Cancellation request sent to admin.")
    return redirect("userprofile")

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def api_my_crops(request):
    if request.method == "GET":
        crops = CropSale.objects.filter(seller=request.user)
        return Response(Cropsaleserializers(crops, many=True).data)

    serializer = Cropsaleserializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(seller=request.user)
    return Response({"success": True}, status=201)


@login_required
@require_POST
def delete_crop(request, id):
    crop = get_object_or_404(CropSale, id=id, seller=request.user)

    if crop.image:
        crop.image.delete(save=False)

    crop.delete()
    messages.success(request, "Crop submission deleted successfully.")
    return redirect("userprofile")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_add_to_cart(request):
    crop_name = request.data.get("crop_name")
    quantity = int(request.data.get("quantity", 1))

    crop = CropSale.objects.select_for_update().filter(
        crop__iexact=crop_name,
        is_approved=True,
        quantity__gte=quantity
    ).order_by("price").first()


    if not crop:
        return Response({"error": "Not enough stock"}, status=400)

    with transaction.atomic():
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            is_paid=False
        )

        item, created = Cartitems.objects.get_or_create(
            cart=cart,
            product=crop,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        crop.quantity -= quantity
        crop.save()

    return Response({"success": True})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_my_cart(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if not cart:
        return Response([])

    items = cart.items.select_related("product")

    data = []
    for item in items:
        data.append({
            "id": item.id,
            "crop": item.product.crop,
            "quantity": item.quantity,
            "price": item.subtotal,
        })

    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_remove_cart_item(request, item_id):
    item = get_object_or_404(Cartitems, id=item_id, cart__user=request.user)

    item.product.quantity += item.quantity
    item.product.save()

    item.delete()
    return Response({"success": True})

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def checkout_api(request):
    print("AUTH HEADER:", request.headers.get("Authorization"))
    print("USER:", request.user)
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart or not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    total = sum(item.subtotal for item in cart.items.all())

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        **serializer.validated_data
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.subtotal
        )

    cart.is_paid = True
    cart.save()

    return Response({"success": True, "order_id": order.id})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    user = request.user
    profile = Signup.objects.filter(user=user).first()

    return Response({
        "username": user.username,
        "email": user.email,
        "mobile": profile.mobile if profile else ""
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    data = []
    for o in orders:
        data.append({
            "id": o.id,
            "total": o.total_amount,
            "status": o.get_status_display(),
            "created_at": o.created_at.strftime("%d %b %Y"),
        })

    return Response(data)
