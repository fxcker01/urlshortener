from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ShortURLForm
from .models import ShortURL

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

import string
import random


def home_view(request):
    error = None
    short_url = None

    if "anon_links" not in request.session:
        request.session["anon_links"] = []

    if request.method == "POST":
        form = ShortURLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            while True:
                short_code = generate_short_code()
                if not ShortURL.objects.filter(short_code=short_code).exists():
                    break

            new_link = form.save(commit=False)

            if request.user.is_authenticated:
                new_link.user = request.user
            else:
                request.session["anon_links"].append({
                    "original_url": original_url,
                    "short_code": short_code,
                })
                request.session.modified = True

            new_link.short_code = short_code
            new_link.save()

            # 👉 Рятує від повторного створення після reload
            request.session['last_short_url'] = short_code
            return redirect('home')
    else:
        form = ShortURLForm()

    # Отримуємо коротке посилання після редіректу
    if 'last_short_url' in request.session:
        short_url = request.build_absolute_uri(f"/{request.session.pop('last_short_url')}")

    if request.user.is_authenticated:
        links = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    else:
        links = list(reversed(request.session.get("anon_links", [])))

    return render(request, 'shortener/home.html', {
        'form': form,
        'links': links,
        'error': error,
        'short_url': short_url,
        'is_anon': not request.user.is_authenticated,
    })







def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def redirect_short_url(request, short_code):
    url = get_object_or_404(ShortURL, short_code=short_code)
    return  HttpResponseRedirect(url.original_url)




@login_required
def delete_link(request, short_code):
    link = get_object_or_404(ShortURL, short_code=short_code, user=request.user)
    link.delete()
    return redirect('home')