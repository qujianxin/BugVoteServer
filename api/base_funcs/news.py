from api.models import News

__author__ = 'hason'


def get_order_news(oder_by, start=0, end=None):
    result = News.objects.order_by(oder_by)
    return result[start:end], result.count()


def get_one_news(_id):
    try:
        record = News.objects.get(id=_id)
    except News.DoesNotExist:
        return None
    return record


def process_content_newline(content):
    return content.split("\n")
