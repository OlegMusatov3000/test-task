from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import BalanceSheet

@csrf_exempt
@login_required
def show_data(request, id):
    context = {'balance_sheet': get_object_or_404(BalanceSheet, id=id)}
    return render(request, 'show_data.html', context)
