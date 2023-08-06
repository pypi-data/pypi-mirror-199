"""Whois client wrapper producing a terse, single-line format."""

import datetime
import logging
from argparse import ArgumentParser, FileType
from time import sleep

import pkg_resources
from tabulate import tabulate
from whois import whois  # type: ignore


__application_name__ = "whois-format"
__version__ = pkg_resources.get_distribution(__application_name__).version
__full_version__ = f"{__application_name__} {__version__}"

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

DEFAULT_STR = "-"
NUM_SLEEP_SECONDS = 15


def get_ns_domains(nameservers: list) -> list:
    """Return parent domain(s) for list of DNS server FQDNs."""
    x = set()
    for fqdn in nameservers:
        dom: str = ".".join(fqdn.split(".")[1:]).lower()
        x.add(dom)
    return list(x)


def cli():
    """CLI entry point."""
    description = "Whois client wrapper producing a terse, single-line format."
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-s",
        "--sleep",
        type=int,
        default=NUM_SLEEP_SECONDS,
        help=(
            "number of seconds to sleep for a pause between lookups of "
            "multiple domains (default: %(default)s)"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-d", "--domain", nargs="+", help="domain name(s) to query"
    )
    group.add_argument(
        "-f", "--in-file", type=FileType("r"), help="input file of domains"
    )
    group.add_argument(
        "-V",
        "--version",
        action="version",
        version=__full_version__,
        help="print package version",
    )
    args = parser.parse_args()

    resp_data = []

    if args.in_file:
        lookup_domains = args.in_file.readlines()
    else:
        lookup_domains = args.domain

    for domain in lookup_domains:
        data = []
        w = whois(domain.strip().lower())

        # Field ordering matters - keep to this format:
        # domain, creation_date, registrar, nameservers, registrant name or
        # organization, registrant email(s)

        data.append(w.domain.upper())
        creation = w.get("creation_date")
        if isinstance(creation, list):
            dt = creation[0]
        else:
            dt = creation
        if isinstance(dt, datetime.datetime):
            data.append(dt.strftime("%Y-%m-%d"))
        else:
            data.append(DEFAULT_STR)
        data.append(w.get("registrar", DEFAULT_STR))
        ns_list = get_ns_domains(w.get("name_servers", []))
        data.append(", ".join(ns_list or ["-"]))
        data.append(w.get("name") or w.get("org", DEFAULT_STR))
        emails = w.get("emails", [DEFAULT_STR])
        if not isinstance(emails, list):
            emails = [emails]
        data.append(", ".join(emails))

        resp_data.append(data)
        sleep(args.sleep)

    print(tabulate(resp_data, tablefmt="plain"))
