from django.shortcuts import render, redirect
from role.models import Notification
def redirect_user_role(request):
    user = request.user
    # If user is an employee
    if str(user.solitonuser.soliton_role) == 'Employee':
        return render(request,"role/employee.html")
    # If user is HOD
    if str(user.solitonuser.soliton_role) == 'HOD':
        return render(request,"role/hod.html")

# Send notification
def send_notification(solitonuser,message):
    notification = Notification(user=solitonuser,message=message)
    notification.save()

