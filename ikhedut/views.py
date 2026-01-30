from django.shortcuts import render,redirect
from .models import Cart,Cartitems,Contact,Signup,Ad,CropSale,Order,OrderItem
from django.db import transaction
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login

from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,serializers
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .serializer import Cropsaleserializers,Conactserializers,OrderSerializer,PostAdvertisementSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Sum, Min

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from django.db import transaction

from rest_framework import status
from rest_framework.response import Response

class CropsaleView(viewsets.ModelViewSet):
    queryset = CropSale.objects.all()
    serializer_class = Cropsaleserializers
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ SERIALIZER ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

@login_required(login_url="/login")
def sellcrops_page(request):
    return render(request, "sellcrops.html")

class ContactView(viewsets.ModelViewSet):
    queryset=Contact.objects.all()
    serializer_class=Conactserializers
    permission_classes=[IsAuthenticated]

@require_POST
@login_required(login_url="/login")
def sellcrops_api(request):
    # print(f"DEBUG: Submitting crop for user: {request.user}") # terminal for this!
    crop_name = request.POST.get("crop")
    quantity = request.POST.get("quantity")
    price = request.POST.get("price")
    image = request.FILES.get("image")

    # Explicitly link request.user to the seller field
    CropSale.objects.create(
        seller=request.user, 
        crop=crop_name,
        quantity=int(quantity),
        price=int(price),
        image=image,
        is_approved=False
    )

    return JsonResponse({"message": "success"}, status=201)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CropSale

@login_required(login_url="/login")
def delete_crop(request, id):
    # Only allow the owner of the crop to delete it
    crop = get_object_or_404(CropSale, id=id, seller=request.user)
    
    if request.method == "POST":
        # Cleanup the image from media folder if it exists
        if crop.image:
            crop.image.delete(save=False)
            
        crop.delete()
        messages.success(request, "Crop submission deleted successfully.")
        
    return redirect("userprofile")


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
@permission_classes([AllowAny])
def buy_crops_api(request):
    sales = CropSale.objects.filter(is_approved=True)

    crops = {}

    for sale in sales:
        key = sale.crop.lower().strip()

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

# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get("username", "").strip()
#         email = request.POST.get("email", "").strip()
#         mobile = request.POST.get("mobile", "").strip()
#         password = request.POST.get("password")
#         repassword = request.POST.get("repassword")
#         image=request.FILES.get("image")

#         if not all([username, email, mobile, password, repassword]):
#             messages.error(request, "All fields are required")
#             return render(request, "signup.html")

#         if password != repassword:
#             messages.error(request, "Passwords do not match")
#             return render(request, "signup.html")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return render(request, "signup.html")
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return render(request, "signup.html")

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         Signup.objects.create(
#             user=user,
#             mobile=mobile,
#             image=image
#         )

#         messages.success(request, "Registration successful")
#         return redirect("login")

#     return render(request, "signup.html")


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_api(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    mobile = request.data.get("mobile")
    image = request.FILES.get("image")

    if not all([username, email, password, mobile]):
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    Signup.objects.create(
        user=user,
        mobile=mobile,
        image=image
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }, status=201)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return render(request, "logout.html")

@login_required(login_url="login")
def cart(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if not cart:
        return render(request, "cart.html", {"items": [], "total": 0})

    items = cart.items.select_related("product")
    total = sum(item.subtotal for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": round(total, 2),
        "now": timezone.now(),
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_add_to_cart(request):
    crop_name = request.data.get("crop_name")
    quantity = int(request.data.get("quantity", 1))

    # pick cheapest available stock
    crop = (
        CropSale.objects
        .filter(crop__iexact=crop_name, is_approved=True, quantity__gte=quantity)
        .order_by("price")
        .first()
    )

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

        # 🔽 DECREASE STOCK
        crop.quantity -= quantity
        crop.save()

    return Response({"success": True})

@login_required(login_url="login")
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cartitems, id=item_id)

    product = item.product
    qty = item.quantity

    with transaction.atomic():
        # 🔼 RESTORE STOCK
        if product:
            product.quantity += qty
            product.save()

        item.delete()

    messages.success(request, "Item removed from cart")
    return redirect("cart")

@require_POST
@login_required
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





@login_required(login_url="/login")
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

@login_required(login_url="login")
def postadvertisement(request):
   return render(request,'postadvertisement.html')

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = PostAdvertisementSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required
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






@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout_api(request):
    user = request.user

    cart = Cart.objects.filter(user=user, is_paid=False).first()
    if not cart or not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    items = cart.items.select_related("product")
    total = sum(item.subtotal for item in items)

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    # 1. Get the validated data
    data = serializer.validated_data
    
    # 2. Remove total_amount from data if it exists to avoid the "multiple values" error
    data.pop('total_amount', None)

    with transaction.atomic():
        # 3. Create the order using manual total and the rest of the data
        order = Order.objects.create(
            user=user,
            total_amount=total,  # We use the calculated total here
            **data               # This now contains fullname, mobile, address, etc.
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.subtotal
            )

        cart.is_paid = True
        cart.save()

    return Response(
        {
            "success": True,
            "order_id": order.id,
            "total": total
        },
        status=201
    )

@login_required(login_url="login")
def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if not cart:
        return render(request, "checkout.html", {
            "items": [],
            "total": 0
        })

    items = cart.items.select_related("product")
    total = sum(item.subtotal for item in items)

    return render(request, "checkout.html", {
        "items": items,
        "total": round(total, 2)
    })

def order_success(request):
    return render(request, "order_success.html")

def spraypump(request):
    return render(request,'spraypump.html')

@login_required(login_url="/login")
def userprofile(request):
    user = request.user
    profile = Signup.objects.filter(user=user).first()
    orders = Order.objects.filter(user=user).order_by("-created_at")
    ads = Ad.objects.filter(user=user).order_by("-id")
    
    crop_sales = CropSale.objects.filter(seller=user).order_by("-id")

    return render(request, "userprofile.html", {
        "user": user,
        "profile": profile,
        "orders": orders,
        "ads": ads,
        "crop_sales": crop_sales, 
    })
    
@login_required(login_url="/login")
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel():
        messages.error(request, "Order can no longer be cancelled.")
        return redirect("userprofile")

    order.status = "cancelled"
    order.save()

    messages.success(request, "Order cancelled successfully.")
    return redirect("userprofile")

@login_required(login_url="/login")
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
