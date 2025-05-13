from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_verification_email(request, user, verification_token):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    
    context = {
        'user': user,
        'verification_url': f"{request.scheme}://{request.get_host()}/verify-email/{uid}/{token}/",
        'token': verification_token,  # The 150-char token
    }
    
    email = EmailMultiAlternatives(
        subject="Verify Your Email",
        body=render_to_string('email/verification_email.txt', context),
        from_email="noreply@example.com",
        to=[user.email]
    )
    email.attach_alternative(
        render_to_string('email/verification_email.html', context),
        "text/html"
    )
    email.send()