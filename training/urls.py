from django.urls import path

from training import views

urlpatterns = [
    path('user_training_page', views.user_training_page, name="user_training_page"),
    path('schedule_training', views.schedule_training_page, name="schedule_training_page"),
    path('edit_training_schedule/<int:training_schedule_id>/', views.edit_training_schedule,
         name="edit_training_schedule"),
    path('delete_training_schedule/<int:training_schedule_id>/', views.delete_training_schedule,
         name="delete_training_schedule"),
    path('training_schedules_page', views.training_schedules_page, name="training_schedules_page"),
    path('approve_training_page', views.approve_training_page, name="approve_training_page"),
    path('pending_training_application_page/<int:training_application_id>', views.pending_training_application_page,
         name="pending_training_application_page"),
    # Process
    path('reject_training_application/<int:training_application_id>', views.reject_training_application,
         name="reject_training_application"),
    path('approve_training_application/<int:training_application_id>', views.approve_training_application,
         name="approve_training_application"),
]
