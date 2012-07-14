# coding=utf-8

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

def context_overload(request):
    """
    Adds the contents of the ``settings.PROPANE_CONTEXT_OVERLOAD`` dictionary to the template context.

    In order to use this context processor, add it to your ``TEMPLATE_CONTEXT_PROCESSORS`` setting::

        TEMPLATE_CONTEXT_PROCESSORS = (
            ... other context processors ...,
            'propane.django.context_processors.context_overload',
        )

    Then set the ``PROPANE_CONTEXT_OVERLOAD`` setting to a dictionary including whatever additional context you
    want available within your templates::

        PROPANE_CONTEXT_OVERLOAD = {
            'less_enabled': True,
            }
    """
    try:
        from django.conf import settings
    except ImportError:
        print "Django is required but cannot be imported."
        raise
    return settings.PROPANE_CONTEXT_OVERLOAD
