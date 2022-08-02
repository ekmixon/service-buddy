import json
import os

import logging
from cookiecutter.main import cookiecutter


def _make_cookie_safe(service_definition):
    return {
        key.replace('-', "_"): valey
        for key, valey in service_definition.iteritems()
    }


class CookeCutterProjectCreator(object):
    def __init__(self, template_dir, dry_run, templates):
        super(CookeCutterProjectCreator, self).__init__()
        self.template_dir = template_dir
        self.templates =templates
        self.dry_run = dry_run

    def create_project(self, service_definition, app_dir,extra_config=None):
        template = self._lookup_service_template(service_definition.get_service_type())
        if template['type'] == 'file':
            location = os.path.abspath(os.path.join(self.template_dir, template['location']))
        else:
            location = template['location']
        extra_context = _make_cookie_safe(service_definition)
        if extra_config:
            extra_context.update(_make_cookie_safe(extra_config))
        if self.dry_run:
            logging.error(f"Creating project from template {location} ")
        else:
            return cookiecutter(location, no_input=True, extra_context=extra_context, output_dir=app_dir)

    def _lookup_service_template(self, service_type):
        if service_type not in self.templates:
            raise Exception(f"Unknown code template - {service_type}")
        return self.templates[service_type]

    @classmethod
    def get_type(cls):
        return "cookiecutter"

