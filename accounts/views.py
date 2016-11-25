from django.contrib import messages, auth
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime
import stripe
import arrow
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import User
from forms import ContactForm, ReservationForm
from django.core.mail import BadHeaderError,send_mail


stripe.api_key = settings.STRIPE_SECRET


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=499,
                    currency="USD",
                    description=form.cleaned_data['email'],
                    card=form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined!")
            if customer.paid:
                form.save()
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('profile'))
            else:
                messages.error(request, "unable to log you in at this time!")
        else:
            messages.error(request, "We were unable to take a payment with that card!")

    else:
        today = datetime.date.today()
        form = UserRegistrationForm()

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'register.html', args)


def profile(request):
    return render(request, 'profile.html')


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email or password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'profile.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('index'))


stripe.api_key = settings.STRIPE_SECRET


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             try:
#                 customer = stripe.Customer.create(
#                     email=form.cleaned_data['email'],
#                     card=form.cleaned_data['stripe_id'],  # this is currently the card token/id
#                     plan='REG_MONTHLY',
#                 )
#             except stripe.error.CardError, e:
#                 messages.error(request, "Your card was declined!")
#
#             if customer:
#                 user = form.save()
#                 user.stripe_id = customer.id
#                 user.subscription_end = arrow.now().replace(weeks=+4).datetime
#                 user.save()
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, "You have successfully registered")
#                 return redirect(reverse('profile'))
#             else:
#                 messages.error(request, "unable to log you in at this time!")
#         else:
#             messages.error(request, "We were unable to take a payment with that card!")
#
#     else:
#         today = datetime.date.today()
#         form = UserRegistrationForm()
#
#         args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
#         args.update(csrf(request))
#
#         return render(request, 'register.html', args)


@login_required(login_url='/login/')
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        customer.cancel_subscription(at_period_end=True)
    except Exception, e:
        messages.error(request, e)
    return redirect('profile')


@csrf_exempt
def subscriptions_webhook(request):
    event_json = json.loads(request.body)
    # Verify the event by fetching it from Stripe
    try:
        event = stripe.Event.retrieve(event_json['object']['id'])
        cust = event_json['object']['customer']
        paid = event_json['object']['paid']
        user = User.objects.get(stripe_id=cust)
        if user and paid:
            user.subscription_end = arrow.now().replace(weeks=+4).datetime  # add 4 weeks from now
            user.save()

    except stripe.InvalidRequestError, e:
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def get_contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['vishaldara01@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "contacts.html", {'form': form})


def thanks(request):
    return render(request, 'thanks.html')


def get_reservation(request):
    if request.method == 'GET':
        form = ReservationForm()
    else:
        form = ReservationForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['vishaldara01@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "reservation.html", {'form': form})

def booking(request):
    return render(request, 'booking.html')