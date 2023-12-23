from django.contrib.sessions.models import Session

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