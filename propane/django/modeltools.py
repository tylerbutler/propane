# coding=utf-8

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

def smart_content_type_for_model(model):
    """
    Returns the Django ContentType for a given model. If model is a proxy model, the proxy model's ContentType will
    be returned. This differs from Django's standard behavior - the default behavior is to return the parent
    ContentType for proxy models.
    """
    try:
        from django.contrib.contenttypes.models import ContentType
    except ImportError:
        print "Django is required but cannot be imported."
        raise

    if model._meta.proxy:
        return ContentType.objects.get(app_label=model._meta.app_label,
            model=model._meta.object_name.lower())
    else:
        return ContentType.objects.get_for_model(model)
