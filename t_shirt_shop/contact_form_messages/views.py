from django.shortcuts import render, redirect

from t_shirt_shop.contact_form_messages.forms import MessagesForm


# Create your views here.


def contact_messages(request):
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = MessagesForm()

    context = {
        'form': form
    }

    return render(request, 'contact-us.html', context=context)
