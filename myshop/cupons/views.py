from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Cupon
from .forms import CuponApplyForm

# Create your views here.

@require_POST
def CuponApply(request):
    now = timezone.now()
    form = CuponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            cupon = Cupon.objects.get(code__iexact=code,
                                      valid_from__lte=now,
                                      valid_to__gte=now,
                                      active=True)
            request.session['cupon_id'] = cupon.id
        except Cupon.DoesNotExist:
            request.sessioon['cupon_id'] = None
    return redirect('cart:CartDetail')