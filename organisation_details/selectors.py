from employees.models import Position, OrganisationDetail, Department


def get_all_departments():
    return Department.objects.all()


def get_all_positions():
    return Position.objects.all()


def get_position(position_id):
    return Position.objects.get(pk=position_id)


def get_organisationdetail(user):
    try:
        organisationdetail = user.solitonuser.employee.organisationdetail
        return organisationdetail
    except OrganisationDetail.DoesNotExist:
        return None


def get_department(department_id):
    return Department.objects.get(pk=department_id)
