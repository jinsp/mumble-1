#!/usr/bin/python
"""Set phpMumbleAdmin Default Super User password and Edit Config Files
Option:
    --pass=     unless provided, will ask interactively
"""

import sys
import getopt
import bcrypt

from executil import system
from dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "phpMumbleAdmin superuser Password",
            "Enter SuperUser Password.")

    hashpw = bcrypt.hashpw(password, bcrypt.gensalt())
    system('sed', '-i', "s#^\( *'SA_pw' =>\) .*$#\\1 '%s',#" % hashpw, '/var/www/phpMumbleAdmin/config/config.php')

if __name__ == "__main__":
    main()
