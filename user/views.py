from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import UserCreateSerializer, EmailSerializer, ChangePasswordSerializer
from .tokens import account_activation_token


def activate(request, uid64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation')
        return redirect('token_obtain_pair')
    else:
        messages.error(request, 'Activation link is invalid')

    return redirect('token_obtain_pair')


def activateEmail(request, user, to_email):
    main_subject = 'Click the link to activate your account for Ulul-Trip ecommerce'
    message = render_to_string('user/activate_account.html',
                {
                    'user': user.username,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http'
                }
    )
    email = EmailMessage(main_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            # user.is_active = False
            data['response'] = 'Succsessfully regsitered new user'
            data['email'] = user.email
            data['username'] = user.username
            activateEmail(request, user, user.email)
            if user.is_active:
                return redirect('token_verify')
            else:
                confirmation = 'Please check your email to confirm signing up'
                if user.is_active:
                    print('2')
                    return redirect('token_verify')
        else:
            data = serializer.errors
        return Response(data)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
