from datetime import datetime
import hashlib
from django.http import HttpResponse
from api.models import Config, Administration, ImageItem, BugType

__author__ = 'hason'


def get_end_time():
    try:
        config = Config.objects.get(name="end_time")
    except Config.DoesNotExist:
        config = Config.objects.create(name="end_time", context="1970-01-01")
    end_time = config.context
    return datetime.strptime(end_time, "%Y-%m-%d")


def get_publicity_pictures():
    config, flag = Config.objects.get_or_create(name="publicity")
    pictures = config.images.all()
    return pictures


def get_one_publicity(the_id):
    return ImageItem.objects.get(id=the_id)


def get_bug_types():
    types = BugType.objects.all()
    return types


def update_bug_type(the_id, new_type):
    try:
        bug_type = BugType.objects.get(id=the_id)
        bug_type.name = new_type
        bug_type.save()
    except:
        return False
    return True


def add_bug_type(new_type):
    try:
        BugType.objects.create(name=new_type)
    except:
        return False
    return True


def admin_logout(req):
    if req.session.get('admin', ''):
        del req.session['admin']
        return True
    else:
        return False


def admin_login(req):
    """
    没有消息才是好消息
    :param req:
    :return:
    """
    username = req.POST.get('username', '')
    password = req.POST.get('password', '')
    remember = req.POST.get('remember', '') == 'true'
    flag, msg = author_admin(username, password)
    if flag:
        req.session['admin'] = username
        if not remember:
            req.session.set_expiry(0)
        return None
    else:
        return msg


def author_admin(username, password):
    try:
        admin = Administration.objects.get(username=username)
    except Administration.DoesNotExist:
        return False, "用户不存在"
    if admin.password == hashlib.sha1(password.encode()).hexdigest():
        return True, admin.username
    else:
        return False, "密码错误"


def check_manager_identity(manage_func):
    """
    装饰manage，确认身份
    :param manage_func:
    :return:
    """

    def decorate(req):
        username = req.session.get("admin", "")
        if not username:
            return HttpResponse(status=401)
        return manage_func(req)

    return decorate
