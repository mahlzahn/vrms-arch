# If you consider the output of this program to be legal advice,
# you're insane.

import os
import os.path

from optparse import OptionParser

import pyalpm

# DFSG/OSI-approved licenses, and the various variants in naming them
# I see in my package database

from .license_finder import LicenseFinder
from .disambiguation import UnambiguousDb

def vrms():
    parser = OptionParser()

    parser.add_option("-g", "--global-repos",
                      dest="use_global_repos",
                      action="store_true",
                      default=False,
                      help="Check licenses in all packages in all synced repositories (might exclude the AUR!), rather than that of locally installed packages")
    parser.add_option("-a", "--list-licenses",
                      dest="list_all_licenses",
                      action="store_true",
                      default=False,
                      help="List all licenses")
    parser.add_option("-e", "--list-ethical",
                      dest="list_ethical",
                      action="store_true",
                      default=False,
                      help="List only non-free packages with 'ethical source' licenses")
    parser.add_option("-u", "--list-unknowns",
                      dest="list_unknowns",
                      action="store_true",
                      default=False,
                      help="List packages of unknown license instead of non-free packages")

    (options, _) = parser.parse_args()

    h = pyalpm.Handle("/", "/var/lib/pacman")

    dbs_to_visit = []

    if options.use_global_repos:
        for d in set(os.path.splitext(f)[0] for f in os.listdir("/var/lib/pacman/sync")):
            h.register_syncdb(d, 0)
        dbs_to_visit = h.get_syncdbs()
    else:
        # print("There are %d installed packages." % len(h.get_localdb()))
        dbs_to_visit.append(h.get_localdb())

    visitor = LicenseFinder()

    for db in dbs_to_visit:
        # print("Reading pacman DB: %s" % db.name, file=sys.stderr)
        db = UnambiguousDb(db)
        visitor.visit_db(db)

    if options.list_unknowns:
        visitor.list_all_unknown_packages()
    elif options.list_ethical:
        visitor.list_all_ethical_packages()
    elif options.list_all_licenses:
        visitor.list_all_licenses_as_python()
    else:
        visitor.list_all_nonfree_packages()
