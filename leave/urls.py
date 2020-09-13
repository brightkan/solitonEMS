from django.urls import path, reverse
from . import views

urlpatterns = [
    # Pages 
    path('', views.leave_dashboard_page, name="leave_dashboard_page"),
    path('leave_records/', views.leave_records, name="leave_records"),
    path('add_leave_records/', views.add_leave_records, name="add_leave_records"),
    path('no_leave_record/', views.no_leave_record_page, name="no_leave_record_page"),
    path('types/', views.leave_types_page, name="leave_types_page"),
    path('apply/', views.apply_leave_page, name="apply_leave_page"),
    path("create_leave_plan_page", views.create_leave_plan_page, name="create_leave_plan_page"),
    path("approve_leave_plan_page", views.approve_leave_plan_page, name="approve_leave_plan_page"),
    path("leave_plans_page", views.leave_plans_page, name="leave_plans_page"),
    path("month_leave_plans_page/<int:month_id>/", views.month_leave_plans_page, name="month_leave_plans_page"),

    # Process
    path("approve_leave_plan/<int:id>/", views.approve_leave_plan, name="approve_leave_plan"),
    path("reject_leave_plan/<int:id>/", views.reject_leave_plan, name="reject_leave_plan"),
    path('add_new_type/', views.add_new_type, name="add_new_type"),
    path('edit_type/<int:id>/', views.edit_leave_type_page, name="edit_leave_type_page"),
    path('edit_leave_type/<int:id>/', views.edit_leave_type, name="edit_leave_type"),
    path('delete_type/<int:id>/', views.delete_leave_type, name="delete_leave_type"),
    path('apply_leave/', views.apply_leave, name="apply_leave"),
    path('edit_leave_application/', views.edit_leave_application, name="edit_leave_application"),
    path('delete_leave_application/', views.delete_leave_application, name="delete_leave_application"),
    path('approve_leave/', views.approve_leave, name="approve_leave"),
    path('reject_leave/<int:id', views.reject_leave, name="reject_leave"),
    path('get_end_date/', views.get_end_date, name="get_end_date"),
    path('get_no_of_days/', views.get_no_of_days, name="get_no_of_days"),
    path('leave_application_details/<int:id>/<str:role>/', views.leave_application_details, name="leave_application_details"),

    path('annual_calendar/', views.Leave_planner_summary, name="annual_calendar"),
    path('leave_planner/', views.leave_planer, name="leave_planner"),
    path('add_new_absence/', views.add_new_absence, name="add_new_absence"),
    path('Leave_planner_summary/', views.Leave_planner_summary, name="Leave_planner_summary"),
    path('leave_calendar/', views.leave_calendar, name="Leave_calendar"),

]

# JS routes
def javascript_settings():
    js_conf = {
        'get_end_date': reverse('get_end_date'),
        'get_no_of_days': reverse('get_no_of_days'),
        'approve_leave': reverse('approve_leave'),
        'reject_leave': reverse('reject_leave'),
        'edit_leave_application': reverse('edit_leave_application'),
        'delete_leave_application': reverse('delete_leave_application'),
        'apply_leave_page': reverse('apply_leave_page'),
        'leave_dashboard_page': reverse('leave_dashboard_page'),
    }

    return js_conf