import hashlib
from api.models import User
from api.serializers import UserSerializer

__author__ = 'hason'


def check_exist(phone_number):
    try:
        User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return False
    return True


def user_login(req):
    """
    没有消息才是好消息
    :param req:
    :return:
    """
    phone = req.POST.get('phone_number', '')
    password = req.POST.get('password', '')
    remember = req.POST.get('remember', '') == 'true'
    flag, msg = author_user(phone, password)
    if flag:
        req.session['phone_number'] = phone
        req.session['name'] = msg
        if not remember:
            req.session.set_expiry(0)
        return None
    else:
        return msg


def user_logout(req):
    if req.session.get('phone_number', ''):
        del req.session['phone_number']
        del req.session['name']
        return True
    else:
        return False


def author_user(phone_number, password):
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return False, "用户不存在"
    if user.password == hashlib.sha1(password.encode()).hexdigest():
        return True, user.name
    else:
        return False, "密码错误"


def get_one_user(phone_number):
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return False
    return user


def update_user(instance, validated_data):
    UserSerializer(instance).update(instance, validated_data)


def get_order_users(oder_by, start=0, end=None):
    result = User.objects.order_by(oder_by)
    return result[start:end], result.count()
