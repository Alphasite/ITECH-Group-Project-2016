from game.themes import themes
from game.models import UserProfile


def common(request):
    if request.user.is_authenticated():
        profile = UserProfile.objects.get(user=request.user)
    else:
        profile = None

    return {
        "themes": themes,
        "profile": profile
    }
