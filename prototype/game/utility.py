from django.contrib.auth.models import User
from django.http import HttpResponse
import json


def json_response(ret, data="", msg=""):
    resp = {"msg": msg, "ret": ret, "data": data}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# User-related
# Return true if a username has been registered before and false otherwise
def check_exist(username, email):
    try:
        User.objects.get(username=username)
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False


# Create a new user in the database
def save_user(username, password, email):
    try:
        user = User.objects.create_user(username, email, password)
    except Exception as e:
        return None, str(e)
    return user
