from django.urls import path, reverse
from . import views

urlpatterns = [
    # Pages
    path('', views.dashboard_page, name="dashboard_page"),
    path('employees/', views.employees_page, name="employees_page"),
    path('employee/<int:id>/', views.employee_page, name="employee_page"),
    path('edit_employee_page/<int:id>/', views.edit_employee_page, name="edit_employee_page"),
    path('edit_certification_page/<int:id>/', views.edit_certification_page, name="edit_certification_page"),
    path('edit_emergency_contact_page/<int:id>/', views.edit_emergency_contact_page,
         name="edit_emergency_contact_page"),
    path('edit_beneficiary_page/<int:id>/', views.edit_beneficiary_page, name="edit_beneficiary_page"),
    path('edit_spouse_page/<int:id>/', views.edit_spouse_page, name="edit_spouse_page"),
    path('edit_dependant_page/<int:id>/', views.edit_dependant_page, name="edit_dependant_page"),


    # Process
    path('add_new_employee/', views.add_new_employee, name="add_new_employee"),
    path('delete_employee/<int:id>', views.delete_employee, name="delete_employee"),
    path('edit_employee/<int:id>', views.edit_employee, name="edit_employee"),
    path('add_new_home_address/', views.add_new_home_address, name="add_new_home_address"),
    path('edit_home_address/', views.edit_home_address, name="edit_home_address"),
    path('add_certification/', views.add_certification, name="add_certification"),
    path('delete_certification/<int:id>', views.delete_certification, name="delete_certification"),
    path('edit_certification/', views.edit_certification, name="edit_certification"),
    path('add_emergency_contact', views.add_emergency_contact, name="add_emergency_contact"),
    path('delete_emergency_contact/<int:id>', views.delete_emergency_contact, name="delete_emergency_contact"),
    path('edit_emergency_contact', views.edit_emergency_contact, name="edit_emergency_contact"),
    path('add_beneficiary/', views.add_beneficiary, name="add_beneficiary"),
    path('edit_beneficiary/', views.edit_beneficiary, name="edit_beneficiary"),
    path('delete_beneficiary/<int:id>/', views.delete_beneficiary, name="delete_beneficiary"),
    path('add_spouse/', views.add_spouse, name="add_spouse"),
    path('edit_spouse/', views.edit_spouse, name="edit_spouse"),
    path('delete_spouse/<int:id>', views.delete_spouse, name="delete_spouse"),
    path('add_dependant/', views.add_dependant, name="add_dependant"),
    path('edit_dependant/', views.edit_dependant, name="edit_dependant"),
    path('delete_dependant/<int:id>', views.delete_dependant, name="delete_dependant"),
    path('add_employee_contacts/', views.add_employee_contacts, name="add_employee_contacts"),
    path('delete_employee_contact/', views.delete_employee_contact, name="delete_employee_contact"),



    path('add_deduction/', views.add_deduction, name="add_deduction"),
    path('edit_deduction/', views.edit_deduction, name="edit_deduction"),
    path('add_allowance/', views.add_allowance, name="add_allowance"),
    path('add_supervisee/', views.add_supervisee, name="add_supervisee"),
    path('delete_superviser/<int:id>/', views.delete_supervisee, name="delete_supervisee"),
    path('delete_deduction/<int:id>', views.delete_deduction, name="delete_deduction"),
    path('delete_allowance/<int:id>', views.delete_allowance, name="delete_allowance"),
    path('edit_bank_details/', views.edit_bank_details, name="edit_bank_details"),
    path('add_bank_details/', views.add_bank_details, name="add_bank_details"),
    path('add_organisation_details/', views.add_organisation_details, name="add_organisation_details"),
    path('edit_organisation_details/', views.edit_organisation_details, name="edit_organisation_details"),
    path('employees_download/', views.employees_download, name="employees_download"),

    path('edit_leave_details/', views.edit_leave_details, name="edit_leave_details"),
    path('suspend_employee/<int:employee_id>/', views.suspend_employee, name="suspend_employee"),
    path('employee_profile_page/<int:employee_id>/', views.employee_profile_page, name="employee_profile_page"),
    path('add_more_details_page/<int:employee_id>/', views.add_more_details_page, name="add_more_details_page"),
    path('activate_employees_page', views.activate_employees_page, name="activate_employees_page"),
    path('activate_employee/<int:employee_id>/', views.activate_employee, name="activate_employee"),
]

# JS routes
def javascript_settings():
    js_conf = {
        'add_employee_contacts': reverse('add_employee_contacts'),
        'delete_employee_contact': reverse('delete_employee_contact'),
    }

    return js_conf