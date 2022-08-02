import logging

from service_buddy.service.loader import walk_service_map


def pretty_print_application(app):
    logging.error(f"{app}")


def pretty_print_service(service_definition):
    logging.warn(f"\t {service_definition.get_role()}")
    for dat in service_definition:
        secondary_indent = '\t\t' if len(dat) <= 10 else '\t'
        logging.info(f"\t\t {dat}{secondary_indent}- {service_definition[dat]}")


def pretty_print_services(application_map):
    walk_service_map(application_map, pretty_print_application, pretty_print_service)