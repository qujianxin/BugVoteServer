from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render_to_response
from math import ceil

from api.base_funcs import admins, users, news, records
from api.base_funcs.admins import check_manager_identity
from api.base_funcs.util import get_start_end
from api.models import News, User, BugRecord

__author__ = 'hason'

NUMBER_PER_PAGE = 8


def index_view(req):
    context = {}
    last_days = (admins.get_end_time() - datetime.now()).days
    if last_days >= 0:
        context['last_days'] = last_days
    else:
        context['last_days'] = "已结束"
    ran_li, count = users.get_order_users("-bonus", end=6)
    context['rank_list'] = dict(map(lambda entry: (entry[0] + 1, entry[1]), enumerate(ran_li)))
    news_li, count = news.get_order_news("time", end=4)
    context['news_list'] = news_li
    pic_list = admins.get_publicity_pictures()
    context['pic_list'] = pic_list
    context['pic_index'] = range(len(pic_list))
    name = req.session.get("name", '')
    if name:
        context['name'] = name
    return render_to_response("index.html", context)


def login_view(req):
    name = req.session.get('name', '')
    if not name:
        return render_to_response("login.html")
    else:
        return HttpResponseRedirect("/")


def register_view(req):
    name = req.session.get('name', '')
    if not name:
        return render_to_response("register.html")
    else:
        return HttpResponseRedirect("/")


def submit_view(req):
    name = req.session.get('name', '')
    if not name:
        return HttpResponseRedirect("/login/")
    else:
        context = {'name': name, 'type_list': admins.get_bug_types()}
        return render_to_response("submit.html", context)


def person_view(req):
    phone = req.session.get('phone_number', '')
    if not phone:
        return HttpResponseRedirect("/login/")
    user = users.get_one_user(phone)
    context = {"user": user, "name": req.session.get('name', '')}
    return render_to_response("pers.html", context)


def news_view(req, pk):
    ne = news.get_one_news(pk)
    if not ne:
        return HttpResponse(status=404)
    new_list = News.objects.all()[0:6]
    news_content = news.process_content_newline(ne.context)

    context = {"name": req.session.get("name", ''), "news": ne, "news_list": new_list, "news_content": news_content}
    return render_to_response("news.html", context)


def rank_list_view(req):
    user_list, count = users.get_order_users("-bonus", end=50)
    context = {'name': req.session.get("name", ''),
               "rank_list": dict(map(lambda entry: (entry[0] + 1, entry[1]), enumerate(user_list)))}
    return render_to_response("user_rank.html", context)


def news_list_view(req):
    news_li = News.objects.all()
    context = {'name': req.session.get("name", ''), "news_list": news_li}
    return render_to_response("news_list.html", context)


def manage_view(req):
    username = req.session.get("admin", "")
    if not username:
        return render_to_response("admins/admin_login.html")
    else:
        return render_to_response("admins/admin.html", {"username": username, "number_per_page": NUMBER_PER_PAGE})


@check_manager_identity
def manage_user_list(req):
    start, end, index = get_start_end(req, NUMBER_PER_PAGE)
    order_by = req.GET.get("order_by", "-created")
    page = 1
    user_list, length = users.get_order_users(order_by, start, end)
    if length != 0:
        page = ceil(length / NUMBER_PER_PAGE)
    return render_to_response("admins/users.html",
                              {"user_list": user_list, "oder_by": order_by, "page": range(1, page + 1), "index": index})


@check_manager_identity
def manage_news_list(req):
    start, end, index = get_start_end(req, NUMBER_PER_PAGE)
    order_by = req.GET.get("order_by", "-time")
    page = 1
    news_list, length = news.get_order_news(order_by, start, end)
    if length != 0:
        page = ceil(length / NUMBER_PER_PAGE)
    return render_to_response("admins/newss.html",
                              {"news_list": news_list, "oder_by": order_by, "page": range(1, page + 1), "index": index})


@check_manager_identity
def manage_bug_list(req):
    start, end, index = get_start_end(req, NUMBER_PER_PAGE)
    have_seen = req.GET.get("have_seen", "null")
    phone_number = req.GET.get("phone_number", "null")
    length = 0
    page = 1
    user = None
    if phone_number != "null":
        user = users.get_one_user(phone_number)
        if not user:
            record_list = []
        else:
            if have_seen == "null":
                record_list = user.bugrecord_set.all()[start:end]
                length = user.bugrecord_set.count()
            else:
                have_seen = have_seen == "true"
                record_list, length = records.get_records_filter(user.bugrecord_set, have_seen, start, end)
    else:
        if have_seen == "null":
            record_list, length = records.get_records(start, end)
        else:
            have_seen = have_seen == "true"
            record_list, length = records.get_records_filter(BugRecord.objects, have_seen, start, end)
    if length != 0:
        page = ceil(length / NUMBER_PER_PAGE)
    if have_seen == "true":
        have_seen = "true"
    elif have_seen == "false":
        have_seen = "false"
    else:
        have_seen = "null"
    return render_to_response("admins/records.html",
                              {"record_list": record_list, "have_seen": have_seen, "page": range(1, page + 1),
                               "index": index, "user":
                                   user, "phone_number": phone_number})


@check_manager_identity
def manage_system_setting(req):
    end_time = admins.get_end_time()
    publicity_pictures = admins.get_publicity_pictures()
    bug_types = admins.get_bug_types()
    context = {"end_time": end_time.date(), "publicity_pictures": publicity_pictures,
               "bug_types": bug_types}
    return render_to_response("admins/system.html", context)


@check_manager_identity
def manage_post_news(req):
    return render_to_response("admins/post_news.html")


@check_manager_identity
def manage_check_news(req):
    news_id = req.GET.get("id", None)
    try:
        news_id = int(news_id)
    except (ValueError, TypeError):
        return HttpResponse(status=400)
    the_news = news.get_one_news(news_id)
    if the_news is None:
        return HttpResponse(status=404)
    news_content = news.process_content_newline(the_news.context)
    return render_to_response("admins/check_news.html", {"news": the_news, "news_content": news_content})


@check_manager_identity
def manage_rank_list(req):
    start, end, index = get_start_end(req, NUMBER_PER_PAGE)
    length = 0
    page = 1
    user_list, count = users.get_order_users("-bonus", start, end)
    if length != 0:
        page = ceil(length / NUMBER_PER_PAGE)
    ranks = range(start + 1, end + 1)

    return render_to_response("admins/rank.html",
                              {"user_dict": dict(zip(ranks, user_list)), "page": range(1, page + 1), "index": index})
