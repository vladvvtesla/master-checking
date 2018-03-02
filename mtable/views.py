from django.shortcuts import render
from .models import MasterSite, MainServer, Head
# Register View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# Main_table view
def main_table(request):
    m_sites = MasterSite.objects.order_by('sitename')
    amur_site = MasterSite.objects.filter(sitename = 'MASTER-Amur')
    tunka_site = MasterSite.objects.filter(sitename = 'MASTER-Tunka')
    kislo_site = MasterSite.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_site = MasterSite.objects.filter(sitename = 'MASTER-Tavrida')
    saao_site = MasterSite.objects.filter(sitename = 'MASTER-SAAO')
    iac_site = MasterSite.objects.filter(sitename = 'MASTER-IAC')
    oafa_site = MasterSite.objects.filter(sitename = 'MASTER-OAFA')

    amur_msrv = MainServer.objects.filter(sitename = 'MASTER-Amur')
    tunka_msrv = MainServer.objects.filter(sitename = 'MASTER-Tunka')
    kislo_msrv = MainServer.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_msrv = MainServer.objects.filter(sitename = 'MASTER-Tavrida')
    saao_msrv = MainServer.objects.filter(sitename = 'MASTER-SAAO')
    iac_msrv = MainServer.objects.filter(sitename = 'MASTER-IAC')
    oafa_msrv = MainServer.objects.filter(sitename = 'MASTER-OAFA')

    amur_head = Head.objects.filter(sitename = 'MASTER-Amur')
    tunka_head = Head.objects.filter(sitename = 'MASTER-Tunka')
    kislo_head = Head.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_head = Head.objects.filter(sitename = 'MASTER-Tavrida')
    saao_head = Head.objects.filter(sitename = 'MASTER-SAAO')
    iac_head = Head.objects.filter(sitename = 'MASTER-IAC')
    oafa_head = Head.objects.filter(sitename = 'MASTER-OAFA')

    return render(request, 'mtable/main_table.html', {  'sites_site': m_sites,
                                                        'amur_site': amur_site[0],
                                                        'tunka_site': tunka_site[0],
                                                        'kislo_site': kislo_site[0],
                                                        'tavr_site': tavr_site[0],
                                                        'saao_site': saao_site[0],
                                                        'iac_site': iac_site[0],
                                                        'oafa_site': oafa_site[0],
                                                'amur_msrv': amur_msrv[0],
                                                'tunka_msrv': tunka_msrv[0],
                                                'kislo_msrv': kislo_msrv[0],
                                                'tavr_msrv': tavr_msrv[0],
                                                'saao_msrv': saao_msrv[0],
                                                'iac_msrv': iac_msrv[0],
                                                'oafa_msrv': oafa_msrv[0],
                                                        'amur_head': amur_head[0],
                                                        'tunka_head': tunka_head[0],
                                                        'kislo_head': kislo_head[0],
                                                        'tavr_head': tavr_head[0],
                                                        'saao_head': saao_head[0],
                                                        'iac_head': iac_head[0],
                                                        'oafa_head': oafa_head[0],
                                                        } )



class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "mtable/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

# Authentication
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login

class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "mtable/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/mtable/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)
