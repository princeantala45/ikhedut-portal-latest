from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from ikhedut import views
from django.conf.urls.static import static
from django.contrib.auth import login
from rest_framework import routers
from .views import CropsaleView,ContactView,api_add_to_cart,buy_crops_api,checkout_api,sellcrops_api,AdvertisementViewSet

router=routers.DefaultRouter()
router.register(r'sellcrops', CropsaleView, basename='sellcrops')
router.register(r'contact', ContactView , basename='Contact')
router.register(r'advertisement', AdvertisementViewSet , basename='Ad')

urlpatterns = [
    path("api/",include(router.urls)),
    # path("api/checkout/", views.checkout_api, name="checkout_api"),
    path("api/sellcrops/", sellcrops_api, name="sellcrops_api"),
    path("",views.index,name="ikhedut"),
    path("api/cart/", api_add_to_cart, name="api_add_to_cart"),
    path("api/buy-crops/", buy_crops_api, name="buy_crops_api"),
    path("agricultureguidance/",views.agricultureguidance,name="agricultureguidance"),
    path("sellcrops/",views.sellcrops_page,name="sellcrops"),
    path("buycrops/", views.buycrops, name="buycrops"),
    path("tractor/",views.tractor,name="tractor"),
    path("tillage/",views.tillage,name="tillage"),
    path("ox/",views.ox,name="ox"),
    path("agrochemicals/",views.agrochemicals,name="agrochemicals"),
    path("fertilizer/",views.fertilizer,name="fertilizer"),
    path("contact/",views.contact,name="contact"),
    # path("signup/",views.signup,name="signup"),
    path("logout/",views.logout,name="logout"),
    path("login/",views.user_login,name="login"),
    path("userprofile/",views.userprofile,name="userprofile"),    
    path("cart/",views.cart,name="cart"),
    path("postadvertisement/",views.postadvertisement,name="postadvertisement"),
    path("postedadvertisement/",views.postedadvertisement,name="postedadvertisement"),
    path("remove-cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('delete-crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),
    path("api/checkout/", checkout_api, name="checkout_api"),
    path("checkout/", views.checkout, name="checkout"),
    path("order_success/", views.order_success, name="order_success"),
    path("spraypump/", views.spraypump, name="spraypump"),
    path("order/cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("advertisement/delete/<int:pk>/",views.delete_advertisement,name="delete_advertisement",),
    path("order/request-cancel/<int:order_id>/",views.request_cancel_order,name="request_cancel_order"),
    path("cart/expire/<int:item_id>/", views.expire_cart_item, name="expire_cart_item"),
    path("accounts/", include("django.contrib.auth.urls")),
    ]

