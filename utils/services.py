<<<<<<< HEAD
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpRequest

from PIL import Image as pil_image


def save_model_image(self, size, field):

    image_field = self.__getattribute__(field)

    img = pil_image.open(image_field.path)

    x = img.width
    y = img.height
    ratio = x/y
    min_dimension = size

    if x > y:
        output_size = (min_dimension * ratio, min_dimension)
    else:
        output_size = (min_dimension, min_dimension * ratio)
    img.thumbnail(output_size)
    img.save(image_field.path)



def get_current_session(request):
    session = Session.objects.get(
        session_key=request.session.session_key
        )
    return session


def create_user_or_session_filter_dict(request):
    filter_dict = {}

    if request.user.is_authenticated:
        filter_dict['user'] = request.user
    elif request.session.session_key != None:
        session = get_current_session(request)
        filter_dict['session'] = session
    return filter_dict


def password_reset_for_new_user(request, email):
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'https://vitanow.ru'
        request.META['SERVER_PORT'] = '443'
        form.save(
            request=request,
            use_https=True,
            from_email="no-reply@vitanow.ru", 
            email_template_name='registration/password_reset_email.html')
=======
import uuid

from slugify import slugify

from django.contrib.sessions.models import Session
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpRequest

from PIL import Image as pil_image


def save_model_image(self, size, field):

    image_field = self.__getattribute__(field)

    img = pil_image.open(image_field.path)

    x = img.width
    y = img.height
    ratio = x/y
    min_dimension = size

    if x > y:
        output_size = (min_dimension * ratio, min_dimension)
    else:
        output_size = (min_dimension, min_dimension * ratio)
    img.thumbnail(output_size)
    img.save(image_field.path)



def get_current_session(request):
    session = Session.objects.get(
        session_key=request.session.session_key
        )
    return session


def create_user_or_session_filter_dict(request):
    filter_dict = {}

    if request.user.is_authenticated:
        filter_dict['user'] = request.user
    elif request.session.session_key != None:
        session = get_current_session(request)
        filter_dict['session'] = session
    return filter_dict


def password_reset_for_new_user(request, email):
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'https://vitanow.ru'
        request.META['SERVER_PORT'] = '443'
        form.save(
            request=request,
            use_https=True,
            from_email="no-reply@vitanow.ru", 
            email_template_name='registration/password_reset_email.html')
        
        
def unique_slug_generator(obj, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(obj.name)

    slug_exists = obj.__class__.objects.filter(slug=slug).exists()
    if slug_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=str(uuid.uuid4())[:4]
        )
        return unique_slug_generator(new_slug=new_slug)

    obj.slug = slug
>>>>>>> 1203ec5 (item, category slug, fixed duplicated buttons)
