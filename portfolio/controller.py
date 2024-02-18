from .models import NewProject


def create_save_session(request, step_one_data, step_two_data):
    new_project = NewProject(
        name=step_one_data['name'],
        partner=step_one_data['partner'],
        summary=step_one_data['summary'],
        data_initial=step_one_data['data_initial'],
        data_final=step_one_data['data_final'],
        area=step_two_data['area'],
        rooms=step_two_data['rooms'],
        style=step_two_data['style'],
        categories=step_two_data['categories'],
        add_stores=step_two_data['add_stores'],
        user=request.user  # Se o usuário estiver disponível na sessão
    )
    new_project.save()
    return new_project