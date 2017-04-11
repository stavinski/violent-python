#!/usr/bin/env python

import sys

from argparse import ArgumentParser
from sqlite3 import connect, Row, OperationalError

def _execute_select(conn, mappings, heading, from_table, where=None):
    cur  = conn.cursor()
    fields = ", ".join(mappings.iterkeys())
    sql = "select %s from %s;" % (fields, from_table)
    if where is not None:
        sql + "where %s" % where

    cur.execute(sql)
    
    for row in cur:
        print "[*] %s" % heading
        for key, val in mappings.iteritems():
            print "[+] %s: %s" % (val, row[key])

def print_profile(conn):
    mappings = {
        "fullname": "user",
        "skypename": "username",
        "city": "city",
        "country": "country",
        "datetime(profile_timestamp, 'unixepoch')": "profile date"
    }
        
    _execute_select(conn, mappings, heading="found profile", from_table="Accounts")


def print_contacts(conn):
    mappings = {
        "fullname": "user",
        "skypename": "username",
        "city": "city",
        "country": "country",
        "phone_mobile": "Mobile No.",
        "birthday": "Birthday"
    }

    _execute_select(conn, mappings, heading="found contacts", from_table="Contacts")

def print_calls(conn):
    mappings = {
        "datetime(begin_timestamp, 'unixepoch')": "time",
        "identity": "partner",
    }

    _execute_select(conn, mappings, heading="found call logs", from_table="Calls, Conversations", where="Calls.conv_dbid = Conversations.id")
    
def print_messages(conn):
    cur  = conn.cursor()
    cur.execute("select datetime(timestamp, 'unixepoch') as time, dialog_partner, author, body_xml from messages order by time;")
    
    print "[*] found messages"
    for row in cur:
        print "[+] time: %s" % row["time"]
        print "[+] partner: %s" % row["dialog_partner"]
        print "[+] author: %s" % row["author"]
        #print "[+] message: %s" % row["body_xml"]

def search_messages(conn, pattern):
    
    print "[*] searching for pattern: %s" % pattern
    cur  = conn.cursor()
    cur.execute("select datetime(timestamp, 'unixepoch') as time, dialog_partner, author, body_xml from messages where body_xml like '%%%s%%';" % pattern)

    for row in cur:
        print "[*] found message =>"
        print "[+] %s" % row["time"]
        print "[+] %s" % row["body_xml"]

def main():
    parser = ArgumentParser("skype parser")

    parser.add_argument("db_file", type=str, help="sqlite skype db file typically main.db")
    parser.add_argument("-s", "--search", help="search message text")
    parser.add_argument("-p", "--profile", help="show profile", action="store_true")
    parser.add_argument("-co", "--contacts", help="show contacts", action="store_true")
    parser.add_argument("-cl", "--calllogs", help="show calls", action="store_true")
    parser.add_argument("-m", "--messages", help="show message", action="store_true")

    args = parser.parse_args()    
    
    try:
        with connect(args.db_file) as conn:
            conn.row_factory = Row # allow colunm names to be used

            if args.profile:
                print_profile(conn)
            if args.contacts:
                print_contacts(conn)
            if args.calllogs:
                print_calls(conn)
            if args.messages:
                print_messages(conn)
            if args.search is not None:
                search_messages(conn, args.search)
    except OperationalError as e:
        print "[!] could not open DB: %s" % str(e)
        exit(1)

if __name__ == "__main__":
    main()
