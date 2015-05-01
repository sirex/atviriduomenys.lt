#!/usr/bin/env python3
"""
Run  project tests.

This script mostly useful for running tests in single file.

"""

import sys
import argparse
import subprocess
import pathlib


def get_cover_package(path):
    if ':' in path:
        path = path[:path.index(':')]

    base = pathlib.Path(__file__).parents[1].resolve()
    path = pathlib.Path(path).resolve()
    path = path.relative_to(base)
    if len(path.parts) > 1:
        return '.'.join(path.parts[:2])
    else:
        return path.parts[0]


def get_paths(paths):
    if paths:
        for path in paths:
            if ':' in path:
                path = path[:path.index(':')]
            yield path
    else:
        yield 'adlt'


def is_coverage_enabled(args):
    if args.nocoverage or args.profile:
        return False
    else:
        return True


def run_tests(args):
    if args.fast:
        settings = 'adlt.settings.fasttesting'
    else:
        settings = 'adlt.settings.testing'

    cmd = [
        'bin/django', 'test',
        '--settings=%s' % settings,
        '--nocapture',
        '--nologcapture',
        '--all-modules',
        '--with-doctest',
        '--doctest-tests',
        '--noinput',
    ] + args.paths

    if args.profile:
        cmd = [
            'bin/kernprof',
            '--line-by-line',
            '--builtin',
            '--outfile=/dev/null',
            '--view',
        ] + cmd
    elif is_coverage_enabled(args):
        coverage_modules = list(set(map(get_cover_package, args.paths)))
        subprocess.call(['bin/coverage', 'erase'])
        cmd = [
            'bin/coverage', 'run',
            '--source=%s' % ','.join(coverage_modules),
        ] + cmd

    return subprocess.call(cmd)


def run_flake8(args):
    cmd = [
        'bin/flake8',
        '--exclude=migrations',
        '--ignore=E501',
    ] + list(get_paths(args.paths))
    return subprocess.call(cmd)


def run_pylint(args):
    cmd = [
        'bin/pylint',
        '--msg-template="%s"' % (
            '{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}',
        )
    ] + list(get_paths(args.paths))
    return subprocess.call(cmd)


def run_coverage_report(args):
    # Also see .coveragerc
    return subprocess.call(['bin/coverage', 'report', '--show-missing'])


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', help='paths to test files')
    parser.add_argument(
        '--fast', action='store_true', default=False,
        help='run tests with adlt.settings.fasttests settings',
    )
    parser.add_argument(
        '--profile', action='store_true', default=False,
        help='run tests with line profiler',
    )
    parser.add_argument(
        '--nocoverage', action='store_true', default=False,
        help='run tests without test coverage report',
    )
    args = parser.parse_args(args)

    sys.exit(run_tests(args))


if __name__ == '__main__':
    main()
