import logging

from service_buddy.ci.ci import BuildCreator
from service_buddy.code.code_creator import CodeCreator
from service_buddy.service.loader import safe_mkdir, walk_service_map, \
    ensure_app_directory_exists
from service_buddy.service.service import Service
from service_buddy.service.service_template_generator import ServiceTemplateGenerator
from service_buddy.util.pretty_printer import pretty_print_service


class Initializer(object):
    def __init__(self, vcs, destination_directory, dry_run, code_template_directory,
                 skip_code_creation=False,
                 skip_build_creation=False,
                 skip_git_creation=False):
        super(Initializer, self).__init__()
        self.skip_code_creation = skip_code_creation
        self.skip_build_creation = skip_build_creation
        self.skip_git_creation = skip_git_creation
        self.code_generator = CodeCreator(code_template_directory=code_template_directory,
                                          dry_run=dry_run)
        self.build_creator = BuildCreator(template_directory=code_template_directory,
                                          dry_run=dry_run)
        self.dry_run = dry_run
        safe_mkdir(directory=destination_directory)
        self.destination_directory = destination_directory
        self.vcs = vcs

    def init_app(self, app):
        pass

    def init_service(self, definition):
        # type: (Service ) -> None
        app_dir = ensure_app_directory_exists(self.destination_directory, service_defintion=definition)
        if definition.repo_exists():
            logging.info("Service exists - {}".format(definition.get_fully_qualified_service_name()))
            if definition.force_recreate_build():
                self.build_creator.create_project(service_definition=definition,app_dir=app_dir)
            return
        logging.info("Creating Service -{}".format(definition.get_fully_qualified_service_name()))
        pretty_print_service(definition)
        if not self.skip_code_creation: self.code_generator.create_project(definition, app_dir)
        if not self.skip_git_creation: self.vcs.create_project(definition, app_dir)
        if not self.skip_build_creation: self.build_creator.create_project(definition,app_dir)

    def initialize_services(self, application_map):
        walk_service_map(application_map=application_map, application_callback=self.init_app,
                         service_callback=self.init_service)
