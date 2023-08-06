#!/usr/bin/python3
# coding=utf-8

import sys

from xarg import xarg

from .xgit_modify_author import add_cmd_modify_author, run_cmd_modify_author
from .xgit_modify_committer import add_cmd_modify_committer
from .xgit_modify_committer import run_cmd_modify_committer
from .xgit_summary import add_cmd_summary, run_cmd_summary


def run_sub_command(args):
    if args.debug:
        sys.stdout.write("{}\n".format(args))
        sys.stdout.flush()
    {
        "summary": run_cmd_summary,
        "modify-author": run_cmd_modify_author,
        "modify-committer": run_cmd_modify_committer,
    }[args.sub](args)


def main():
    try:
        _arg = xarg(
            "xgit",
            description="Git tool based on GitPython",
            epilog="For more, please visit https://github.com/zoumingzhe/xgit")
        _arg.add_opt_on('-d', '--debug', help="show debug information")
        _arg.add_subparsers(dest="sub", required=True)
        add_cmd_modify_author(_arg.add_parser("modify-author"))
        add_cmd_modify_committer(_arg.add_parser("modify-committer"))
        add_cmd_summary(_arg.add_parser("summary"))
        args = _arg.parse_args()
        run_sub_command(args)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stderr.write("{}\n".format(e))
        sys.stderr.flush()
