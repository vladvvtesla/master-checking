from django.shortcuts import render
from .models import MasterSite, MainServer, Head, Mount, Ccd
# Register View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# Main_table view
def main_table(request):
    m_sites = MasterSite.objects.order_by('sitename')
    #mcodes = [amur, tunka, kislo, tavr, saao, iac, oafa]

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

    amur_mount = Mount.objects.filter(sitename = 'MASTER-Amur')
    tunka_mount = Mount.objects.filter(sitename = 'MASTER-Tunka')
    kislo_mount = Mount.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_mount = Mount.objects.filter(sitename = 'MASTER-Tavrida')
    saao_mount = Mount.objects.filter(sitename = 'MASTER-SAAO')
    iac_mount = Mount.objects.filter(sitename = 'MASTER-IAC')
    oafa_mount = Mount.objects.filter(sitename = 'MASTER-OAFA')

    amur_ccdw = Ccd.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'west')
    tunka_ccdw = Ccd.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'west')
    kislo_ccdw = Ccd.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'west')
    tavr_ccdw = Ccd.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'west')
    saao_ccdw = Ccd.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'west')
    iac_ccdw = Ccd.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'west')
    oafa_ccdw = Ccd.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'west')

    amur_ccde = Ccd.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'east')
    tunka_ccde = Ccd.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'east')
    kislo_ccde = Ccd.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'east')
    tavr_ccde = Ccd.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'east')
    saao_ccde = Ccd.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'east')
    iac_ccde = Ccd.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'east')
    oafa_ccde = Ccd.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'east')


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
                                                'amur_mount': amur_mount[0],
                                                'tunka_mount': tunka_mount[0],
                                                'kislo_mount': kislo_mount[0],
                                                'tavr_mount': tavr_mount[0],
                                                'saao_mount': saao_mount[0],
                                                'iac_mount': iac_mount[0],
                                                'oafa_mount': oafa_mount[0],
                                                        'amur_ccdw': amur_ccdw[0],
                                                        'tunka_ccdw': tunka_ccdw[0],
                                                        'kislo_ccdw': kislo_ccdw[0],
                                                        'tavr_ccdw': tavr_ccdw[0],
                                                        'saao_ccdw': saao_ccdw[0],
                                                        'iac_ccdw': iac_ccdw[0],
                                                        'oafa_ccdw': oafa_ccdw[0],
                                                'amur_ccde': amur_ccde[0],
                                                'tunka_ccde': tunka_ccde[0],
                                                'kislo_ccde': kislo_ccde[0],
                                                'tavr_ccde': tavr_ccde[0],
                                                'saao_ccde': saao_ccde[0],
                                                'iac_ccde': iac_ccde[0],
                                                'oafa_ccde': oafa_ccde[0],
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
