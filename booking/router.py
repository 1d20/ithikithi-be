from rest_framework import routers
from booking import views


router = routers.DefaultRouter()
router.register(r'booking', views.BookingViewSet)
router.register(r'booking-person', views.BookingPersonViewSet)
router.register(r'uz', views.UZViewSet, base_name='uz')
