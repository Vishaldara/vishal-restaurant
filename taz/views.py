from django.shortcuts import render


# Create your views here.


def get_index(request):
    return render(request, 'index.html')


def get_menu(request):
    return render(request, 'menu.html')


def get_voucher(request):
    return render(request, 'voucher.html')


def get_reservation(request):
    return render(request, 'reservation.html')


def get_contact(request):
    return render(request, 'contacts.html')


def get_opening(request):
    return render(request, 'opening.html')


def get_location(request):
    return render(request, 'location.html')



