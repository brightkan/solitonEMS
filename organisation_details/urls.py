from django.urls import path

from . import views


urlpatterns = [
    path('', views.about_us, name="about_us"),
    path('no_organisation_detail_page/', views.no_organisation_detail_page, name="no_organisation_detail_page"),

    # departments
    path('edit_department_page/<int:department_id>/', views.edit_department_page, name="edit_department_page"),
    path('manage_departments/', views.manage_departments_page, name="manage_departments_page"),
    path('add_new_department/', views.add_new_department, name="add_new_department"),
    path('edit_department', views.edit_department, name="edit_department"),
    path('delete_department/<int:department_id>', views.delete_department, name="delete_department"),

    # Teams
    path('add_new_team/', views.add_new_team, name="add_new_team"),
    path('edit_team_page/<int:id>/', views.edit_team_page, name="edit_team_page"),
    path('teams', views.manage_teams_page, name="manage_teams_page"),
    path('edit_team/<team_id>/', views.edit_team_page, name="edit_team_page"),
    path('delete_team/<team_id>/', views.delete_team, name="delete_team"),
    path('team_employees/<team_id>/', views.team_employees, name="team_employees"),
    path('department_employees/<department_id>/', views.department_employees, name="department_employees"),

    # Job Positions
    path('manage_job_positions/', views.manage_job_positions_page, name="manage_job_positions_page"),
    path('add_new_job_position/', views.add_new_job_position, name="add_new_job_position"),
    path('edit_job_position/<int:position_id>', views.edit_job_position_page, name="edit_job_position_page"),
    path('edit_job_position/', views.edit_job_position, name="edit_job_position"),
    path('delete_job_position/<int:position_id>', views.delete_job_position, name="delete_job_position"),

    # Salary Scales
    path('manage_salary_scale/', views.manage_salary_scale_page, name="manage_salary_scale_page"),
    path('add_new_salary_scale/', views.add_new_salary_scale, name="add_new_salary_scale"),
    path('edit_salary_scale/<int:scale_id>', views.edit_salary_scale_page, name="edit_salary_scale_page"),
    path('edit_salary_scale/', views.edit_salary_scale, name="edit_salary_scale"),
    path('delete_salary_scale/<int:scale_id>', views.delete_salary_scale, name="delete_salary_scale"),
]
