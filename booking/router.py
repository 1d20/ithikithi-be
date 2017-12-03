from rest_framework import routers
from booking import views


router = routers.DefaultRouter()
router.register(r'booking', views.BookingViewSet, base_name='booking')
router.register(r'booking-person', views.BookingPersonViewSet, base_name='booking_person')
router.register(r'uz', views.UZViewSet, base_name='uz')
