from django.urls import path

from contracts import views

urlpatterns = [

    path("manage_job_contracts", views.manage_job_contracts, name="manage_job_contracts"),
    path("terminate_contract/<int:contract_id>/", views.terminate_contract, name="terminate_contract"),
    path("edit_contract_page/<int:contract_id>/", views.edit_contract_page, name="edit_contract_page"),
    path("terminated_contracts", views.terminated_contracts_page, name="terminated_contracts_page"),
    path("activate_contract/<int:contract_id>/", views.activate_contract, name="activate_contract"),
    path("user_contracts_page", views.user_contracts_page, name="user_contracts_page"),
    path("manage_offences_page", views.manage_offences_page, name="manage_offences_page"),
    path("edit_offence_page/<int:offence_id>/", views.edit_offence_page, name="edit_offence_page"),
    path("delete_offence/<int:offence_id>/", views.delete_offence, name="delete_offence"),
    path("manage_penalties_page", views.manage_penalties_page, name="manage_penalties_page"),
    path("edit_penalty_page/<int:penalty_id>/", views.edit_penalty_page, name="edit_penalty_page"),
    path("delete_penalty/<int:penalty_id>/", views.delete_penalty, name="delete_penalty"),
    path("manage_terminations_page", views.manage_terminations_page, name="manage_terminations_page"),
    path("edit_termination/<int:termination_id>/", views.edit_termination_page, name="edit_termination_page"),
    path("delete_termination/<int:termination_id>/", views.delete_termination, name="delete_termination"),
]
