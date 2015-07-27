# coding=utf-8
from urlparse import urlsplit
from xml.dom.minidom import Text
from path import Path

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

template_path = Path(__file__).parent / 'templates'


class WOPIApp(object):
    def __init__(self):
        from jinja2 import Template

        self.template = Template((template_path / 'wopi/_discovery.xml').text())

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def favicon_url(self):
        raise NotImplementedError()

    @property
    def actions(self):
        # should return an iterable of 3-tuples of (action_name, extension, url_src) (or use the DiscoveryAction class)
        raise NotImplementedError()

    @property
    def zones(self):
        zones = set()
        for action in self.actions:
            for zone in action.zones:
                zones.add(zone)
        return zones

    @property
    def discovery_xml(self):
        return self.template.render(app=self)

    def actions_for_zone(self, zone):
        return [a for a in self.actions if zone in a.zones]


class WOPIApplication(object):
    _name = ''
    _actions = []

    def __init__(self, name):
        self.name = name
        self.favicon_url = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def actions(self):
        # should return an iterable of 3-tuples of (action_name, extension, url_src) (or use the WOPIAction class)
        raise NotImplementedError()

    # @actions.setter
    # def actions(self, value):
    #     self._actions = value

    @property
    def discovery_xml(self):
        from jinja2 import Template

        with open('templates/wopi/_discovery.xml', mode='rb') as template_file:
            template = Template(template_file)
        template.render()
        return

    def add_action(self, action):
        self._actions.append(action)


class WOPIAction(object):
    def __init__(self, name, extension, url, zones=('external-https',),
                 prog_id=None, requirements=None, mime_type=None):
        from jinja2 import Template

        self.name = name
        self.extension = extension
        self.url = url
        self.zones = zones
        self.prog_id = prog_id
        self.requirements = requirements
        self.mime_type = mime_type

        self.template = Template((template_path / 'wopi/_action.xml').text())

    @property
    def urlsrc(self):
        return self.url.urlsrc

    @property
    def xml(self):
        return self.template.render(action=self)


class WOPIActionUrl(object):
    def __init__(self, base_url, placeholders):
        self.base_url = base_url
        self.placeholders = placeholders

    @property
    def netloc(self):
        return urlsplit(self.base_url).netloc

    @property
    def query(self):
        return urlsplit(self.base_url).query

    @property
    def urlsrc(self):
        prepend = self.base_url + '&' if self.query else self.base_url + '?' if self.placeholders else self.base_url
        return prepend + ''.join([p.xml for p in self.placeholders])


class WopiActionUrlPlaceholder(object):
    def __init__(self, placeholder_name, query_param):
        self.placeholder_name = placeholder_name
        self.query_param = query_param

    @property
    def xml(self):
        element = Text()
        raw = '<%s=%s&>' % (self.query_param, self.placeholder_name)
        element.data = raw
        to_return = element.toxml()
        return to_return
