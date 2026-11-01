from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('api/me/', views.me_api, name='api_me'),
    path('api/profile/', views.save_profile, name='api_profile'),
    path('api/delete-profile/', views.delete_profile, name='api_delete_profile'),
    path('api/listings/', views.listings_api, name='api_listings'),
    path('api/my-submissions/', views.my_submissions_api, name='api_my_subs'),
    path('api/pending/', views.pending_api, name='api_pending'),
    path('api/submit/', views.submit_listing, name='api_submit'),
    path('api/approve/<int:pk>/', views.approve_listing, name='api_approve'),
    path('api/reject/<int:pk>/', views.reject_listing, name='api_reject'),
    path('api/delete/<int:pk>/', views.delete_listing, name='api_delete'),
]