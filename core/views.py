from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

from .models import Profile, Listing
from .forms import RegisterForm, ProfileForm, ListingForm, ChemForm


@ensure_csrf_cookie
def home(request):
    return render(request, 'index.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def me_api(request):
    csrf = get_token(request)
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False, 'csrf': csrf})

    profile = getattr(request.user, 'profile', None)
    profile_data = None
    if profile:
        profile_data = {
            'role': profile.role,
            'name': profile.name,
            'org': profile.org,
            'contact': profile.contact,
            'bio': profile.bio,
            'fields': profile.fields,
        }

    return JsonResponse({
        'authenticated': True,
        'isAdmin': request.user.is_staff,
        'userId': request.user.id,
        'username': request.user.username,
        'csrf': csrf,
        'profile': profile_data,
    })


@login_required
@require_POST
def save_profile(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'contact': request.user.email or '',
        }
    )
    data = request.POST.copy()
    data.setlist('fields', request.POST.getlist('fields'))

    form = ProfileForm(data, instance=profile)
    if form.is_valid():
        p = form.save(commit=False)
        p.fields = list(form.cleaned_data['fields'])
        p.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


@login_required
@require_POST
def delete_profile(request):
    try:
        request.user.profile.delete()
        return JsonResponse({'ok': True})
    except Profile.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'no_profile'}, status=404)


def _listing_to_dict(l):
    return {
        'id': l.id,
        'kind': l.kind,
        'title': l.title,
        'org': l.org,
        'extra': l.extra,
        'desc': l.desc,
        'contact': l.contact,
        'fields': l.fields or [],
        'status': l.status,
        'createdAt': int(l.created_at.timestamp() * 1000),
        'ownerId': l.owner_id,
        'cat': l.cat,
        'cas': l.cas,
        'grade': l.grade,
        'qty': l.qty,
        'price': l.price,
        'city': l.city,
    }


def listings_api(request):
    qs = Listing.objects.filter(status='approved')
    return JsonResponse([_listing_to_dict(l) for l in qs], safe=False)


@login_required
def my_submissions_api(request):
    qs = Listing.objects.filter(owner=request.user)
    return JsonResponse([_listing_to_dict(l) for l in qs], safe=False)


@staff_member_required
def pending_api(request):
    qs = Listing.objects.filter(status='pending')
    return JsonResponse([_listing_to_dict(l) for l in qs], safe=False)


@login_required
@require_POST
def submit_listing(request):
    kind = request.POST.get('kind', '')
    if kind not in ('need', 'res', 'chem'):
        return JsonResponse({'ok': False, 'error': 'invalid_kind'}, status=400)

    if kind == 'chem':
        form = ChemForm(request.POST)
    else:
        form = ListingForm(request.POST)

    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    listing = form.save(commit=False)
    listing.owner = request.user
    listing.kind = kind

    if kind != 'chem':
        listing.fields = list(form.cleaned_data['fields'])

    listing.status = 'approved' if request.user.is_staff else 'pending'
    listing.save()
    return JsonResponse({'ok': True, 'id': listing.id})


@staff_member_required
@require_POST
def approve_listing(request, pk):
    l = get_object_or_404(Listing, pk=pk)
    l.status = 'approved'
    l.save()
    return JsonResponse({'ok': True})


@staff_member_required
@require_POST
def reject_listing(request, pk):
    l = get_object_or_404(Listing, pk=pk)
    l.status = 'rejected'
    l.save()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def delete_listing(request, pk):
    l = get_object_or_404(Listing, pk=pk)
    if l.owner == request.user or request.user.is_staff:
        l.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'error': 'forbidden'}, status=403)