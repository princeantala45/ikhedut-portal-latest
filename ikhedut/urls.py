from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from ikhedut import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   
from .views import *

router = routers.DefaultRouter()
router.register(r"contact", ContactView, basename="contact")

urlpatterns = [
    path("api/register/", RegistrerUser.as_view()),
    path("generic-sellcrops/", SellCropsGeneric.as_view()),
    path("generic-sellcrops1/<int:id>/", SellCropsGeneric1.as_view()),
    path("postad/", PostAdGeneric.as_view()),
    path("Postad1/<int:id>/", PostAdGeneric1.as_view()),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.index, name="ikhedut"),

    path("api/", include(router.urls)),
    path("api/cart/", views.api_add_to_cart, name="api_add_to_cart"),
    path("api/buy-crops/", buy_crops_api, name="buy_crops_api"),
    path("api/checkout/", checkout_api, name="checkout_api"),

    path("agricultureguidance/", views.agricultureguidance,name="agricultureguidance"),
    path("sellcrops/", views.sellcrops_page,name="sellcrops_page"),
    path("buycrops/", views.buycrops,name="buycrops"),
    path("tractor/", views.tractor,name="tractor"),
    path("signup/", views.signup,name="signup"),
    path("tillage/", views.tillage,name="tillage"),
    path("ox/", views.ox,name="ox"),
    path("agrochemicals/", views.agrochemicals,name="agrochemicals"),
    path("fertilizer/", views.fertilizer,name="fertilizer"),
    path("spraypump/", views.spraypump,name="spraypump"),
    path("contact/", views.contact,name="contact"),
    
    path("login/", login_page, name="login"),        
    path("login_api/", views.login_api, name="login_api"),
    path("logout/", views.logout,name="logout"),
    path("userprofile/", views.userprofile, name="userprofile"),

    path("cart/", views.cart,name="cart"),
    path("cart/expire/<int:item_id>/", views.expire_cart_item),
    path("delete-crop/<id>/", views.delete_crop, name="delete_crop"),
    path("remove-cart/<int:item_id>/",views.remove_from_cart,name="remove_from_cart"),

    path("postadvertisement/", views.postadvertisement),
    path("postedadvertisement/", views.postedadvertisement),
    path("delete-advertisement/<int:id>/",views.delete_advertisement,name="delete_advertisement"),

    path("checkout/", views.checkout),
    path("order_success/", views.order_success),
    path("order/cancel/<int:order_id>/", views.cancel_order),
    path("order/request-cancel/<int:order_id>/", views.request_cancel_order),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
