# from django.shortcuts import render
# from .models import MasterSite, MainServer, Head, Mount, Ccd, Focuser, SecondServer, Ebox
# # Register View
# from django.views.generic.edit import FormView
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .models import MasterSite, MainServer, Head, Mount, Dome, Ccd, WFC, \
                    Filter, Focuser, SecondServer, Ebox, Actuator
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
    mexico_site = MasterSite.objects.filter(sitename='MASTER-Mexico')

    amur_msrv = MainServer.objects.filter(sitename = 'MASTER-Amur')
    tunka_msrv = MainServer.objects.filter(sitename = 'MASTER-Tunka')
    kislo_msrv = MainServer.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_msrv = MainServer.objects.filter(sitename = 'MASTER-Tavrida')
    saao_msrv = MainServer.objects.filter(sitename = 'MASTER-SAAO')
    iac_msrv = MainServer.objects.filter(sitename = 'MASTER-IAC')
    oafa_msrv = MainServer.objects.filter(sitename = 'MASTER-OAFA')
    mexico_msrv = MainServer.objects.filter(sitename='MASTER-Mexico')

    amur_head = Head.objects.filter(sitename = 'MASTER-Amur')
    tunka_head = Head.objects.filter(sitename = 'MASTER-Tunka')
    kislo_head = Head.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_head = Head.objects.filter(sitename = 'MASTER-Tavrida')
    saao_head = Head.objects.filter(sitename = 'MASTER-SAAO')
    iac_head = Head.objects.filter(sitename = 'MASTER-IAC')
    oafa_head = Head.objects.filter(sitename = 'MASTER-OAFA')
    mexico_head = Head.objects.filter(sitename='MASTER-Mexico')

    amur_mount = Mount.objects.filter(sitename = 'MASTER-Amur')
    tunka_mount = Mount.objects.filter(sitename = 'MASTER-Tunka')
    kislo_mount = Mount.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_mount = Mount.objects.filter(sitename = 'MASTER-Tavrida')
    saao_mount = Mount.objects.filter(sitename = 'MASTER-SAAO')
    iac_mount = Mount.objects.filter(sitename = 'MASTER-IAC')
    oafa_mount = Mount.objects.filter(sitename = 'MASTER-OAFA')
    mexico_mount = Mount.objects.filter(sitename='MASTER-Mexico')

    amur_dome = Dome.objects.filter(sitename = 'MASTER-Amur')
    tunka_dome = Dome.objects.filter(sitename = 'MASTER-Tunka')
    kislo_dome = Dome.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_dome = Dome.objects.filter(sitename = 'MASTER-Tavrida')
    saao_dome = Dome.objects.filter(sitename = 'MASTER-SAAO')
    iac_dome = Dome.objects.filter(sitename = 'MASTER-IAC')
    oafa_dome = Dome.objects.filter(sitename = 'MASTER-OAFA')
    mexico_dome = Dome.objects.filter(sitename='MASTER-Mexico')

    amur_ccdw = Ccd.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'west')
    tunka_ccdw = Ccd.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'west')
    kislo_ccdw = Ccd.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'west')
    tavr_ccdw = Ccd.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'west')
    saao_ccdw = Ccd.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'west')
    iac_ccdw = Ccd.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'west')
    oafa_ccdw = Ccd.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'west')
    mexico_ccdw = Ccd.objects.filter(sitename='MASTER-Mexico').filter(tube='west')

    amur_ccde = Ccd.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'east')
    tunka_ccde = Ccd.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'east')
    kislo_ccde = Ccd.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'east')
    tavr_ccde = Ccd.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'east')
    saao_ccde = Ccd.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'east')
    iac_ccde = Ccd.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'east')
    oafa_ccde = Ccd.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'east')
    mexico_ccde = Ccd.objects.filter(sitename='MASTER-Mexico').filter(tube='east')

    amur_wfcw = WFC.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'west')
    tunka_wfcw = WFC.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'west')
    kislo_wfcw = WFC.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'west')
    tavr_wfcw = WFC.objects.filter(sitename = 'MASTER-Tavrida').filter(wfcid = '500')
    saao_wfcw = WFC.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'west')
    iac_wfcw = WFC.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'west')
    oafa_wfcw = WFC.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'west')
    mexico_wfcw = WFC.objects.filter(sitename='MASTER-Mexico').filter(tube='west')

    amur_wfce = WFC.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'east')
    tunka_wfce = WFC.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'east')
    kislo_wfce = WFC.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'east')
    tavr_wfce = WFC.objects.filter(sitename = 'MASTER-Tavrida').filter(wfcid = '501')
    saao_wfce = WFC.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'east')
    iac_wfce = WFC.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'east')
    oafa_wfce = WFC.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'east')
    mexico_wfce = WFC.objects.filter(sitename='MASTER-Mexico').filter(tube='east')

    tavr_qhyw = Ccd.objects.filter(sitename = 'MASTER-Tavrida').filter(ccdid = '501')
    tavr_qhye = Ccd.objects.filter(sitename = 'MASTER-Tavrida').filter(ccdid = '500')

    amur_filterw = Filter.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'west')
    tunka_filterw = Filter.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'west')
    kislo_filterw = Filter.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'west')
    tavr_filterw = Filter.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'west')
    saao_filterw = Filter.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'west')
    iac_filterw = Filter.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'west')
    oafa_filterw = Filter.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'west')
    mexico_filterw = Filter.objects.filter(sitename='MASTER-Mexico').filter(tube='west')

    amur_filtere = Filter.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'east')
    tunka_filtere = Filter.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'east')
    kislo_filtere = Filter.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'east')
    tavr_filtere = Filter.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'east')
    saao_filtere = Filter.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'east')
    iac_filtere = Filter.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'east')
    oafa_filtere = Filter.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'east')
    mexico_filtere = Filter.objects.filter(sitename='MASTER-Mexico').filter(tube='east')

    amur_focuserw = Focuser.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'west')
    tunka_focuserw = Focuser.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'west')
    kislo_focuserw = Focuser.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'west')
    tavr_focuserw = Focuser.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'west')
    saao_focuserw = Focuser.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'west')
    iac_focuserw = Focuser.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'west')
    oafa_focuserw = Focuser.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'west')
    mexico_focuserw = Focuser.objects.filter(sitename='MASTER-Mexico').filter(tube='west')

    amur_focusere = Focuser.objects.filter(sitename = 'MASTER-Amur').filter(tube = 'east')
    tunka_focusere = Focuser.objects.filter(sitename = 'MASTER-Tunka').filter(tube = 'east')
    kislo_focusere = Focuser.objects.filter(sitename = 'MASTER-Kislovodsk').filter(tube = 'east')
    tavr_focusere = Focuser.objects.filter(sitename = 'MASTER-Tavrida').filter(tube = 'east')
    saao_focusere = Focuser.objects.filter(sitename = 'MASTER-SAAO').filter(tube = 'east')
    iac_focusere = Focuser.objects.filter(sitename = 'MASTER-IAC').filter(tube = 'east')
    oafa_focusere = Focuser.objects.filter(sitename = 'MASTER-OAFA').filter(tube = 'east')
    mexico_focusere = Focuser.objects.filter(sitename='MASTER-Mexico').filter(tube='east')

    amur_ssrv = SecondServer.objects.filter(sitename = 'MASTER-Amur')
    tunka_ssrv = SecondServer.objects.filter(sitename = 'MASTER-Tunka')
    kislo_ssrv = SecondServer.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_ssrv = SecondServer.objects.filter(sitename = 'MASTER-Tavrida')
    saao_ssrv = SecondServer.objects.filter(sitename = 'MASTER-SAAO')
    iac_ssrv = SecondServer.objects.filter(sitename = 'MASTER-IAC')
    oafa_ssrv = SecondServer.objects.filter(sitename = 'MASTER-OAFA')
    mexico_ssrv = SecondServer.objects.filter(sitename='MASTER-Mexico')

    amur_e21 = Ebox.objects.filter(hostname = 'amur-e21')
    tunka_e203 = Ebox.objects.filter(hostname = 'tunka-e203')
    kislo_e16 = Ebox.objects.filter(hostname = 'kislo-e16')
    kislo_n17 = Ebox.objects.filter(hostname='kislo-n17')
    kislo_e22 = Ebox.objects.filter(hostname='kislo-e22')
    kislo_e33 = Ebox.objects.filter(hostname='kislo-e33')
    tavr_e98 = Ebox.objects.filter(hostname = 'tavrida-e98')
    tavr_e99 = Ebox.objects.filter(hostname='tavrida-e99')
    tavr_e41 = Ebox.objects.filter(hostname='tavrida-e41')
    saao_e98 = Ebox.objects.filter(hostname = 'saao-e98')
    iac_e3 = Ebox.objects.filter(hostname = 'iac-e3')
    oafa_e150 = Ebox.objects.filter(hostname = 'oafa-e150')
    mexico_e100 = Ebox.objects.filter(hostname = 'mexico-e100')

    amur_act = Actuator.objects.filter(sitename = 'MASTER-Amur')
    tunka_act = Actuator.objects.filter(sitename = 'MASTER-Tunka')
    kislo_act = Actuator.objects.filter(sitename = 'MASTER-Kislovodsk')
    tavr_act = Actuator.objects.filter(sitename = 'MASTER-Tavrida')
    saao_act = Actuator.objects.filter(sitename = 'MASTER-SAAO')
    iac_act = Actuator.objects.filter(sitename = 'MASTER-IAC')
    oafa_act = Actuator.objects.filter(sitename = 'MASTER-OAFA')
    mexico_act = Actuator.objects.filter(sitename='MASTER-Mexico')


    return render(request, 'mtable/main_table.html', {  'sites_site': m_sites,
                                                        'amur_site': amur_site[0],
                                                        'tunka_site': tunka_site[0],
                                                        'kislo_site': kislo_site[0],
                                                        'tavr_site': tavr_site[0],
                                                        'saao_site': saao_site[0],
                                                        'iac_site': iac_site[0],
                                                        'oafa_site': oafa_site[0],
                                                        'mexico_site': mexico_site[0],
                                                'amur_msrv': amur_msrv[0],
                                                'tunka_msrv': tunka_msrv[0],
                                                'kislo_msrv': kislo_msrv[0],
                                                'tavr_msrv': tavr_msrv[0],
                                                'saao_msrv': saao_msrv[0],
                                                'iac_msrv': iac_msrv[0],
                                                'oafa_msrv': oafa_msrv[0],
                                                'mexico_msrv': mexico_msrv[0],
                                                        'amur_head': amur_head[0],
                                                        'tunka_head': tunka_head[0],
                                                        'kislo_head': kislo_head[0],
                                                        'tavr_head': tavr_head[0],
                                                        'saao_head': saao_head[0],
                                                        'iac_head': iac_head[0],
                                                        'oafa_head': oafa_head[0],
                                                        'mexico_head': mexico_head[0],
                                                'amur_mount': amur_mount[0],
                                                'tunka_mount': tunka_mount[0],
                                                'kislo_mount': kislo_mount[0],
                                                'tavr_mount': tavr_mount[0],
                                                'saao_mount': saao_mount[0],
                                                'iac_mount': iac_mount[0],
                                                'oafa_mount': oafa_mount[0],
                                                'mexico_mount': mexico_mount[0],
                                                    'amur_dome': amur_dome[0],
                                                    'tunka_dome': tunka_dome[0],
                                                    'kislo_dome': kislo_dome[0],
                                                    'tavr_dome': tavr_dome[0],
                                                    'saao_dome': saao_dome[0],
                                                    'iac_dome': iac_dome[0],
                                                    'oafa_dome': oafa_dome[0],
                                                    'mexico_dome': mexico_dome[0],
                                                        'amur_ccdw': amur_ccdw[0],
                                                        'tunka_ccdw': tunka_ccdw[0],
                                                        'kislo_ccdw': kislo_ccdw[0],
                                                        'tavr_ccdw': tavr_ccdw[0],
                                                        'saao_ccdw': saao_ccdw[0],
                                                        'iac_ccdw': iac_ccdw[0],
                                                        'oafa_ccdw': oafa_ccdw[0],
                                                        'mexico_ccdw': mexico_ccdw[0],
                                                'amur_ccde': amur_ccde[0],
                                                'tunka_ccde': tunka_ccde[0],
                                                'kislo_ccde': kislo_ccde[0],
                                                'tavr_ccde': tavr_ccde[0],
                                                'saao_ccde': saao_ccde[0],
                                                'iac_ccde': iac_ccde[0],
                                                'oafa_ccde': oafa_ccde[0],
                                                'mexico_ccde': mexico_ccde[0],
                                                        'amur_wfcw': amur_wfcw[0],
                                                        'tunka_wfcw': tunka_wfcw[0],
                                                        'kislo_wfcw': kislo_wfcw[0],
                                                        'tavr_wfcw': tavr_wfcw[0],
                                                        'saao_wfcw': saao_wfcw[0],
                                                        'iac_wfcw': iac_wfcw[0],
                                                        'oafa_wfcw': oafa_wfcw[0],
                                                        'mexico_wfcw': mexico_wfcw[0],
                                                'amur_wfce': amur_wfce[0],
                                                'tunka_wfce': tunka_wfce[0],
                                                'kislo_wfce': kislo_wfce[0],
                                                'tavr_wfce': tavr_wfce[0],
                                                'saao_wfce': saao_wfce[0],
                                                'iac_wfce': iac_wfce[0],
                                                'oafa_wfce': oafa_wfce[0],
                                                'mexico_wfce': mexico_wfce[0],
                                                    'tavr_qhyw': tavr_qhyw[0],
                                                    'tavr_qhye': tavr_qhye[0],
                                                        'amur_filterw': amur_filterw[0],
                                                        'tunka_filterw': tunka_filterw[0],
                                                        'kislo_filterw': kislo_filterw[0],
                                                        'tavr_filterw': tavr_filterw[0],
                                                        'saao_filterw': saao_filterw[0],
                                                        'iac_filterw': iac_filterw[0],
                                                        'oafa_filterw': oafa_filterw[0],
                                                        'mexico_filterw': mexico_filterw[0],
                                                'amur_filtere': amur_filtere[0],
                                                'tunka_filtere': tunka_filtere[0],
                                                'kislo_filtere': kislo_filtere[0],
                                                'tavr_filtere': tavr_filtere[0],
                                                'saao_filtere': saao_filtere[0],
                                                'iac_filtere': iac_filtere[0],
                                                'oafa_filtere': oafa_filtere[0],
                                                'mexico_filtere': mexico_filtere[0],
                                                        'amur_focuserw': amur_focuserw[0],
                                                        'tunka_focuserw': tunka_focuserw[0],
                                                        'kislo_focuserw': kislo_focuserw[0],
                                                        'tavr_focuserw': tavr_focuserw[0],
                                                        'saao_focuserw': saao_focuserw[0],
                                                        'iac_focuserw': iac_focuserw[0],
                                                        'oafa_focuserw': oafa_focuserw[0],
                                                        'mexico_focuserw': mexico_focuserw[0],
                                                'amur_focusere': amur_focusere[0],
                                                'tunka_focusere': tunka_focusere[0],
                                                'kislo_focusere': kislo_focusere[0],
                                                'tavr_focusere': tavr_focusere[0],
                                                'saao_focusere': saao_focusere[0],
                                                'iac_focusere': iac_focusere[0],
                                                'oafa_focusere': oafa_focusere[0],
                                                'mexico_focusere': mexico_focusere[0],
                                                        'amur_ssrv': amur_ssrv[0],
                                                        'tunka_ssrv': tunka_ssrv[0],
                                                        'kislo_ssrv': kislo_ssrv[0],
                                                        'tavr_ssrv': tavr_ssrv[0],
                                                        'saao_ssrv': saao_ssrv[0],
                                                        'iac_ssrv': iac_ssrv[0],
                                                        'oafa_ssrv': oafa_ssrv[0],
                                                        'mexico_ssrv': mexico_ssrv[0],
                                                'amur_e21': amur_e21[0],
                                                'tunka_e203': tunka_e203[0],
                                                'kislo_e16': kislo_e16[0],
                                                'kislo_n17': kislo_n17[0],
                                                'kislo_e22': kislo_e22[0],
                                                'kislo_e33': kislo_e33[0],
                                                'tavr_e98': tavr_e98[0],
                                                'tavr_e99': tavr_e99[0],
                                                'tavr_e41': tavr_e41[0],
                                                'saao_e98': saao_e98[0],
                                                'iac_e3': iac_e3[0],
                                                'oafa_e150': oafa_e150[0],
                                                'mexico_e100': mexico_e100[0],
                                                        'amur_act': amur_act[0],
                                                        'tunka_act': tunka_act[0],
                                                        'kislo_act': kislo_act[0],
                                                        'tavr_act': tavr_act[0],
                                                        'saao_act': saao_act[0],
                                                        'iac_act': iac_act[0],
                                                        'oafa_act': oafa_act[0],
                                                        'mexico_act': mexico_act[0],
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
