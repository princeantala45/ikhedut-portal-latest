from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from ikhedut import views
from .views import (
    CropsaleView,
    ContactView,
    api_add_to_cart,
    buy_crops_api,
    checkout_api,
    sellcrops_api,
    AdvertisementViewSet,
)

router = routers.DefaultRouter()
router.register(r"sellcrops", CropsaleView, basename="sellcrops")
router.register(r"contact", ContactView, basename="contact")
router.register(r"advertisement", AdvertisementViewSet, basename="advertisement")

urlpatterns = [
    path("", views.index, name="ikhedut"),

    path("api/", include(router.urls)),
    path("api/sellcrops/", sellcrops_api, name="sellcrops_api"),
    path("api/cart/", api_add_to_cart, name="api_add_to_cart"),
    path("api/buy-crops/", buy_crops_api, name="buy_crops_api"),
    path("api/checkout/", checkout_api, name="checkout_api"),

    path("agricultureguidance/", views.agricultureguidance),
    path("sellcrops/", views.sellcrops_page),
    path("buycrops/", views.buycrops),
    path("tractor/", views.tractor),
    path("signup/", views.signup),
    path("tillage/", views.tillage),
    path("ox/", views.ox),
    path("agrochemicals/", views.agrochemicals),
    path("fertilizer/", views.fertilizer),
    path("spraypump/", views.spraypump),
    path("contact/", views.contact),
    

    path("login/", views.user_login),
    path("logout/", views.logout),
    path("userprofile/", views.userprofile, name="userprofile"),

    path("cart/", views.cart),
    path("cart/expire/<int:item_id>/", views.expire_cart_item),
    path("delete-crop/<int:id>/", views.delete_crop, name="delete_crop"),
    path("remove-cart/<int:item_id>/", views.remove_from_cart),

    path("postadvertisement/", views.postadvertisement),
    path("postedadvertisement/", views.postedadvertisement),
    path(
    "delete-advertisement/<int:id>/",
    views.delete_advertisement,
    name="delete_advertisement"
),


    path("checkout/", views.checkout),
    path("order_success/", views.order_success),
    path("order/cancel/<int:order_id>/", views.cancel_order),
    path("order/request-cancel/<int:order_id>/", views.request_cancel_order),
    path("delete-crop/<int:id>/", views.delete_crop, name="delete_crop"),


    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
