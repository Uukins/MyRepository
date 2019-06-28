from .forms import LoginForm,RegForm

def login_modal_form(request):
    return {'login_modal_form':LoginForm()}
def register_modal_form(request):
    return {'reigster_modal_form':RegForm()}