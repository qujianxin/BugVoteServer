from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response

from api.base_funcs import users, admins, news, records, util
from api.models import Config, BugRecord
from api.serializers import UserSerializer, BugRecordSerializer, NewsSerializer, ImageItemSerializer


class SimpleResponse(HttpResponse):
    def __init__(self, is_success, msg=None, **kwargs):
        data = {"is_success": is_success}
        if msg:
            data['msg'] = msg
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(SimpleResponse, self).__init__(content, **kwargs)


@api_view(['POST'])
def register(req):
    phone = req.session.get("phone", "")
    password = req.session.get('password', "")
    if not phone:
        return SimpleResponse(False, "请先验证手机")
    else:
        del req.session['phone']
    req.data["phone_number"] = phone
    req.data['password'] = password
    ser = UserSerializer(data=req.data)
    if ser.is_valid():
        ser.save()
        return SimpleResponse(True)
    else:
        return SimpleResponse(False, ser.error_messages)


@api_view(['POST'])
def login_user(req):
    err_msg = users.user_login(req)
    if not err_msg:  # 没有消息才是好消息
        return SimpleResponse(True)
    else:
        return SimpleResponse(False, err_msg)


@api_view(['POST'])
def edit_user(req):
    phone = req.session.get('phone_number', '')
    if not phone:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    user = users.get_one_user(phone)
    users.update_user(user, req.data)
    req.session['name'] = req.data['name']
    return SimpleResponse(True)


@api_view(['GET'])
def logout_user(req):
    return SimpleResponse(users.user_logout(req))


@api_view(['POST'])
def send_msg(req):
    token = util.get_token()
    req.session["verify_code"] = token
    req.session.set_expiry(180)
    util.send_template_sms(req.POST.get("phone_number", ""), [token, "3"])
    return SimpleResponse(True)


@api_view(['POST'])
def check_phone(req):
    phone = req.POST.get('phone_number', '')
    if phone and not users.check_exist(phone):
        return SimpleResponse(True)
    else:
        return SimpleResponse(False)


@api_view(['POST'])
def validate_phone(req):
    phone = req.POST.get('phone_number', '')
    password = req.POST.get('password', '')
    code = req.POST.get('verify_code', '')
    if phone and password and code and req.session.get("verify_code", "") == code:
        del req.session['verify_code']
        req.session['phone'] = phone
        req.session['password'] = password
        req.session.set_expiry(1800)
        return SimpleResponse(True)
    else:
        return SimpleResponse(False)


@api_view(['POST'])
def post_one_record(req):
    phone = req.session.get('phone_number', '')
    if not phone:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    req.data['commit_person'] = phone
    ser = BugRecordSerializer(data=req.data)
    if ser.is_valid():
        ser.save()
        return SimpleResponse(True)
    else:
        return SimpleResponse(False, "Bug类型有所变化,请刷新后重新提交。记得复制原文。")


@api_view(['POST'])
def manage_login(req):
    err_msg = admins.admin_login(req)
    if not err_msg:  # 没有消息才是好消息
        return SimpleResponse(True)
    else:
        return SimpleResponse(False, err_msg)


@api_view(['GET'])
def manage_logout(req):
    return SimpleResponse(admins.admin_logout(req))


@api_view(['POST'])
@admins.check_manager_identity
def post_news(req):
    ser = NewsSerializer(data=req.data)
    if ser.is_valid():
        ser.save()
        return SimpleResponse(True)
    else:
        return SimpleResponse(False, ser.errors)


@api_view(['GET'])
@admins.check_manager_identity
def delete_news(req):
    news_id = req.GET.get("id", None)
    try:
        news_id = int(news_id)
    except (TypeError, ValueError):
        return HttpResponse(status=400)
    the_news = news.get_one_news(news_id)
    if the_news is None:
        return HttpResponse(status=404)
    the_news.delete()
    return SimpleResponse(True)


@api_view(['POST'])
@admins.check_manager_identity
def update_news(req):
    news_id = req.POST.get("id", None)
    try:
        news_id = int(news_id)
    except (TypeError, ValueError):
        return HttpResponse(status=400)
    the_news = news.get_one_news(news_id)
    if the_news is None:
        return HttpResponse(status=404)
    ser = NewsSerializer(the_news)
    ser.update(the_news, req.data)
    return SimpleResponse(True)


@api_view(['GET'])
@admins.check_manager_identity
def delete_publicity(req):
    publicity_id = req.GET.get("id", None)
    try:
        publicity_id = int(publicity_id)
    except (TypeError, ValueError):
        return SimpleResponse(False, "请输入正确的id")
    the_publicity = admins.get_one_publicity(publicity_id)
    if the_publicity is None:
        return SimpleResponse(False, "没有这条信息")
    the_publicity.delete()
    return SimpleResponse(True)


@api_view(['POST'])
@admins.check_manager_identity
def post_publicity(req):
    ser = ImageItemSerializer(data=req.data)
    if ser.is_valid():
        ser.save()
        pub_config, flag = Config.objects.get_or_create(name="publicity")
        pub_config.images.add(ser.instance)
        return SimpleResponse(True)
    else:
        return SimpleResponse(False, ser.errors)


@api_view(['GET'])
@admins.check_manager_identity
def update_end_time(req):
    end_time = req.GET.get("end_time", None)
    import re
    if not end_time or not re.match(r"\d{4}-\d{2}-\d{2}", end_time):
        return SimpleResponse(False, "请输入正确的日期")
    pub_config, flag = Config.objects.get_or_create(name="end_time")
    pub_config.context = end_time
    pub_config.save()
    return SimpleResponse(True)


@api_view(['POST'])
@admins.check_manager_identity
def update_bonus(req):
    bonus = req.POST.get("bonus", "0")
    try:
        bonus = int(bonus)
    except (TypeError, ValueError):
        return SimpleResponse(False, "请输入正确的钱数")
    record_id = req.POST.get("id", None)
    if not record_id:
        return SimpleResponse(False, "id是必须的")
    try:
        record_id = int(record_id)
    except (TypeError, ValueError):
        return SimpleResponse(False, "请输入正确的id")
    record = records.get_one_record(record_id)
    if not record:
        return SimpleResponse(False, "没有这条记录")

    ser = BugRecordSerializer(record)
    ser.update(record, {"bonus": bonus, "have_seen": True})

    return SimpleResponse(True)


@api_view(['POST'])
@admins.check_manager_identity
def update_bug_type(req):
    the_id = req.POST.get("id", "")
    new_type = req.POST.get("new_type", "")
    if not the_id or not new_type:
        return SimpleResponse(False, "不可为空")
    try:
        the_id = int(the_id)
    except (TypeError, ValueError):
        return SimpleResponse(False, "请输入正确的id")
    return SimpleResponse(admins.update_bug_type(the_id, new_type))


@api_view(['POST'])
@admins.check_manager_identity
def add_bug_type(req):
    new_type = req.POST.get("new_type", "")
    return SimpleResponse(admins.add_bug_type(new_type))
