from django.contrib.sessions.models import Session


def get_current_session(request):
    session = Session.objects.get(
        session_key=request.session.session_key
        )
    return session