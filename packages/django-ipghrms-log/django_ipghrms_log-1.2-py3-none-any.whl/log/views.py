from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from contract.models import Contract, EmpSalary, EmpPlacement
from settings_app.decorators import allowed_users
from log.models import Log
import datetime
from attendance.models import Month
from settings_app.utils import f_monthname
def get_years():
    current_year = datetime.datetime.now().year
    return [year for year in range(2022, current_year + 1)]

@login_required
def LogList(request):
    objects = []
    page = ''
    monthname = ''
    year = None
    years = get_years()
    months = Month.objects.all()
    curYear = datetime.datetime.now().year
    curMonth = datetime.datetime.now().month
    if request.method == 'POST':
        getYear = request.POST.get('tinan')
        getMonth = request.POST.get('fulan')
        if getYear != '0' and getMonth != '0':
            page = 'filter'
            monthname = f_monthname(int(getMonth))
            year = int(getYear)
            obj = Log.objects.filter(timestamp__year=getYear)
            for j in obj:
                if j.timestamp.month == int(getMonth):
                    objects.append(j)
        elif getMonth != '0':
            page = 'filter'
            year = int(curYear)
            monthname = f_monthname(int(getMonth))
            obj = Log.objects.filter(timestamp__year=curYear)
            for j in obj:
                if j.timestamp.month == int(getMonth):
                    objects.append(j)
        elif getYear != '0':
            page = 'filter'
            year = int(getYear)
            monthname = f_monthname(int(curMonth))
            obj = Log.objects.filter(timestamp__year=curYear)
            for j in obj:
                if j.timestamp.month == int(curMonth):
                    objects.append(j)
        else:
            data = Log.objects.all().order_by('-pk')
            for i in data:
                objects.append(i)
    else:
        data = Log.objects.all().order_by('-pk')
        for i in data:
            objects.append(i)
    context = {
        'title': 'Log List', 'legend': 'Log List',
        'objects': objects, 'monthname':monthname, 'year':year,
        'years': years, 'months': months, 'page': page
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