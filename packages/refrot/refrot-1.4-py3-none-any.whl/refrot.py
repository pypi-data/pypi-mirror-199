#!/usr/bin/env python3
import argparse
from importlib.metadata import version
from timeit import default_timer as timer

import requests

import hparser


def formatter(prog): return argparse.HelpFormatter(prog, max_help_position=52)
parser = argparse.ArgumentParser(
                    formatter_class=formatter, prog='refrot',
                    usage='%(prog)s [options]')
parser.add_argument(dest='url')
parser.add_argument('--ignore-external-links', '-i',
                    action='store_true',
                    help='ignore external links')
parser.add_argument('--user-agent', '-u', metavar='AGENT',
                    help='user agent')
parser.add_argument('-v', '--version',
                    action='version',
                    version='refrot version ' + version('refrot'))


def check():
    checked, errors = get_links(args.url)
    print(f'\nLinks checked: {len(checked)}. Errors found: {len(errors)}.')
    for key in errors:
        print(errors[key], key)


def get_links(url, checked=[], errors={}):
    """Recursively check links found at url."""
    if url in checked:
        return
    if args.ignore_external_links and not url.startswith(args.url):
        return
    checked.append(url)
    try:
        if args.user_agent:
            headers = {'user-agent': args.user_agent}
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url)
        if r.history:
            status_code = r.history[0].status_code
            reason = r.history[0].reason
            print(status_code, url)
            # Ignore temporary redirects.
            if status_code != 302:
                errors[url] = f'{status_code} {reason}'
        else:
            print(r.status_code, url)
        if r.status_code != 200:
            errors[url] = f'{r.status_code} {r.reason}'
    except requests.exceptions.SSLError:
        print('SSL Cert Fail', url)
        errors[url] = 'SSL Cert Fail'
        return checked, errors
    except requests.exceptions.ConnectionError:
        print('Connection error', url)
        errors[url] = 'Connection error'
        return checked, errors

    # Don't spider external links. They can check their own pages!
    if not url.startswith(args.url):
        return
    parser = hparser.LinkParser()
    parser.feed(r.text)
    parser.make_links_absolute(url)
    for link in parser.links:
        get_links(link, checked, errors)
    return checked, errors


def main():
    start = timer()
    global args
    args = parser.parse_args()
    check()
    end = timer()
    print(f'Run time: {end - start:.2f} seconds')


if __name__ == "__main__":
    main()

