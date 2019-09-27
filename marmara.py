import os
import signal
import hashlib
import time

from urllib2 import Request, urlopen, URLError

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

from threading import Thread

APPINDICATOR_ID = 'marmaradeprem'


def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(
        'sample_icon.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    update = Thread(target=get_new_eq)
    update.setDaemon(True)
    update.start()
    gtk.main()


def build_menu():
    menu = gtk.Menu()
    item_last_eq = gtk.MenuItem('Last Earth Quake')
    item_last_eq.connect('activate', last_eq_menu)
    menu.append(item_last_eq)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def fetch_all_eqs():
    request = Request('http://www.koeri.boun.edu.tr/scripts/lst4.asp')
    response = urlopen(request).read()
    eq_raws = filter(lambda x: "MARMARA DENIZI" in x, response.split("\r\n"))
    eqs = [' '.join(eq_raw.split()).split() for eq_raw in eq_raws]
    return eqs


def format_eq(eq):
    formatted = eq[6] + " Earth Quake at " + eq[1]
    return formatted


def fetch_last_eq():
    eq = fetch_all_eqs()
    return format_eq(eq[0])


def get_new_eq():
    delay = 60
    while True:
        time.sleep(delay)
        eq = fetch_last_eq()
        if is_new(eq):
            print eq
            new_eq_notification(eq)


def is_new(eq):
    is_new = False
    home = os.path.expanduser("~")
    hashfile_path = home + "/.config/lateseqhash"
    cur_hash_result = hashlib.md5(str.encode(eq)).hexdigest()
    if os.path.isfile(hashfile_path):
        f = open(hashfile_path, "r")
        last_hash_result = f.read()
        if last_hash_result.strip() != cur_hash_result.strip():
            print last_hash_result
            print cur_hash_result
            is_new = True
    else:
        is_new = True

    f = open(hashfile_path, "w")
    f.write(cur_hash_result)
    f.close()
    return is_new


def new_eq_notification(eq):
    notify.Notification.new("<b>Last EQ</b>", eq, None).show()


def last_eq_menu(_):
    notify.Notification.new("<b>Last EQ</b>", fetch_last_eq(), None).show()


def quit(_):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
