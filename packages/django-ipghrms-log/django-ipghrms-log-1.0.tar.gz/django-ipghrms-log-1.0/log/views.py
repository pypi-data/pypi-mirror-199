from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from contract.models import Contract, EmpSalary, EmpPlacement
from settings_app.decorators import allowed_users
from log.models import Log


@login_required
def LogList(request):
    objects = Log.objects.all().order_by('-pk')
    context = {
        'title': 'Log List', 'legend': 'Log List',
        'objects': objects
    }
    return render(request,'log/list.html', context)

@login_required
def LogDetail(request, hashid):
    objects = Log.objects.get(hashed=hashid)
    context = {
        'title': 'Log Detail', 'legend': 'Log Detail',
        'objects': objects
    }
    return render(request,'log/detail.html', context)