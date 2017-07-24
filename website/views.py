from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max
from operator import itemgetter
from .models import *
from .forms import *

def index(request):
    if request.user.is_authenticated():
        members = Members.objects.all()
        members_list = []
        for member in members:
            check_member = Weighins.objects.filter(member=member)
            if not check_member:
                continue
            wi = Weighins.objects.filter(member=member).latest('date')
            member = Members.objects.get(name=member.name.id)
            bwp = ((float(member.initial_weight) - float(wi.weight)) / float(member.initial_weight)) * 100
            mbwp = {}
            mbwp['member'] = wi.member.name.first_name
            mbwp['initial_weight'] = member.initial_weight
            mbwp['weight'] = wi.weight
            mbwp['bwp'] = bwp
            mbwp['photo'] = member.photo.url
            members_list.append(mbwp)
        ml = sorted(members_list, key=itemgetter('bwp'), reverse=True)
        return render(request, 'website/home.html',{'weighins':ml})
    else:
        return render(request, 'website/index.html',{})

def registration(request):
    if request.method == 'POST':
        uf = UserForm(request.POST or None, prefix='user')
        mf = MemberForm(request.POST or  None, request.FILES or  None, prefix='userprofile')
        if uf.is_valid() * mf.is_valid():
            gw = request.POST.get('userprofile-goal_weight','')
            iw = request.POST.get('userprofile-initial_weight','')
            photo = request.FILES.get('photo', False)
            user = uf.save()
            mp = mf.save(commit=False)
            mp.name = user
            mp.goal_weight = gw
            mp.initial_weight = iw
            if photo:
                mp.photo = photo
            mp.save()
            messages.success(request,'Registration Completed!')
        else:
            messages.error(request,'Yo! You did something wrong, try again!')
    else:
        uf = UserForm(prefix='user')
        mf = MemberForm(prefix='userprofile')
    return render(request,'registration/register.html',{'userform':uf,'memberform':mf})

@login_required
def profile(request):
    member = Members.objects.get(name=request.user)
    weighins = Weighins.objects.filter(member=member)
    payments = Payments.objects.filter(member=member)
    weight_list = []
    for w in weighins:
        wl = float(member.initial_weight) - float(w.weight)
        bwp = ((float(member.initial_weight) - float(w.weight)) / float(member.initial_weight)) * 100
        nwi = {'date':w.date,'weight':w.weight,'photo':w.photo.url,'member':member,'weight_loss':wl,'body_weight_percentage':bwp}
        weight_list.append(nwi)

    total = 0
    for p in payments:
        total += p.amount
    return render(request,'website/profile.html',{'member':member, 'weighins':weighins,'weight_list':weight_list,'payment_total':total})

@login_required
def add_weighin(request):
    member = Members.objects.get(name=request.user)
    weighins = Weighins.objects.filter(member=member)
    if request.method == 'POST':
        wi = WeighinForm(request.POST or None, request.FILES or None, prefix='weighin')
        photo = request.FILES.get('photo', False)
        if wi.is_valid():
            wi.save()
            messages.success(request,'Weighin Added Successfully!')
            return render(request, 'website/profile.html', {'member':member,'weighins':weighins})
        else:
            messages.error(request,'Something went wrong, try again.')
    else:
        wi = WeighinForm(prefix='weighin')
    return render(request,'website/add_weighin.html',{'member':member, 'weighins':weighins, 'weighinform':wi})

@login_required
def add_progress_photos(request):
    user = Members.objects.get(name=request.user)
    if request.method == 'POST':
        form = AddProgressPhotos(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Progress photo added successfully! Looking good! :)')
            return redirect('add_progress_photos')
    else:
        form = AddProgressPhotos(instance=user)
    return render(request, 'website/add_progress_photos.html')
