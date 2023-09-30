from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


from t_shirt_shop.accounts.forms import ShopUserRegistrationForm, ShopUserLoginForm, ViewUserInfo, ViewProfileInfo, \
    AddCustomDesigns
from t_shirt_shop.accounts.models import ShopUserModel, UserProfileModel, MyDesignsModel


# Create your views here.

class UserRegisterView(generic.CreateView):
    model = ShopUserModel
    form_class = ShopUserRegistrationForm
    template_name = 'accounts/user-register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user_profile = UserProfileModel.objects.create(user=self.object)

        return response


class UserLoginView(LoginView):
    template_name = 'accounts/user-login.html'
    form_class = ShopUserLoginForm
    next_page = reverse_lazy('homepage')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')


def user_details_view (request):
    user_instance = ShopUserModel.objects.get(id=request.user.id)
    profile_instance = UserProfileModel.objects.get(user=request.user)
    form_user = ViewUserInfo(request.POST or None, instance=user_instance)
    form_profile = ViewProfileInfo(request.POST or None, instance=profile_instance)

    if request.method == 'POST':
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            return redirect('user_details_view')

    context = {
        'form_user': form_user,
        'form_profile': form_profile,
    }

    return render(request, template_name='accounts/user-details.html', context=context)


def my_designs(request):
    user = request.user
    designs = MyDesignsModel.objects.filter(user=user)

    if request.method == 'POST':
        form = AddCustomDesigns(request.POST, request.FILES)
        if form.is_valid():
            design_instance = form.save(commit=False)
            design_instance.user = user
            design_instance.save()
            return redirect('my_designs')
    else:
        form = AddCustomDesigns()

    context = {
        'user': user,
        'designs': designs,
        'form': form
    }
    return render(request, template_name='accounts/my-designs.html', context=context)
