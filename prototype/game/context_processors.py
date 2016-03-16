from game.themes import themes


def common(request):
    return {
        "themes": themes
    }
