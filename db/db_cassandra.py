#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by longqi on 05/04/15
"""
__author__ = 'longqi'
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

session = None


def init_db():
    ap = PlainTextAuthProvider(username='dashboard', password='YvHSeWH3DYCPZrbai8MZ')
    cluster = Cluster(['155.69.214.102', '172.21.77.197'], auth_provider=ap)
    global session
    session = cluster.connect()
    session.default_timeout = 30  # default is 10, always fail for BBB, 30 is better,


def check_keyspace():
    global session
    rows = session.execute(
        "SELECT * FROM system.schema_keyspaces WHERE keyspace_name='mybbbs'")
    print('rows', rows)
    if rows:
        msg = ' It looks like you already have a mybbbs keyspace.\nDo you '
        msg += 'want to delete it and recreate it? All current data will '
        msg += 'be deleted! (y/n): '
        resp = input(msg)
        if not resp or resp[0] != 'y':
            print("Ok, then we're done here.")
            return
        session.execute("DROP KEYSPACE mybbbs")

    session.execute("""
        CREATE KEYSPACE mybbbs
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
        """)

    # create tables
    session.set_keyspace("mybbbs")

    session.execute("""
        CREATE TABLE bbb (
            hostname text PRIMARY KEY,
            date timestamp,
            ip_info text,
        )
        """)

    print('All done!')


def update_host_info(hostname, time_rec, ip):
    print('begin update_host_info...')

    # for the type timestamp,tha parameter must be float, otherwise you will get a exception
    time_rec = float(time_rec)

    get_hostname_query = session.prepare("""
            SELECT * FROM mybbbs.bbb WHERE hostname=?
            """)

    insert_hostname_query = session.prepare("""
            INSERT INTO mybbbs.bbb (hostname, date , ip_info )
            VALUES (?, ?, ?)
            """)

    update_hostname_query = session.prepare("""
            UPDATE mybbbs.bbb
            SET date = ?, ip_info = ?
            WHERE hostname = ?
            """)
    print('prepare...')
    rows = session.execute(get_hostname_query, (hostname,))
    print('check...', rows)
    # noinspection PyBroadException
    try:
        if not rows:
            res = session.execute(insert_hostname_query, (hostname, time_rec, ip))
        else:
            res = session.execute(update_hostname_query, (time_rec, ip, hostname))
    except:

        print('insertion failed... ', res)


def get_hosts_list(quantity):
    get_hosts_list_query = session.prepare("""
            SELECT * FROM mybbbs.bbb LIMIT ?
            """)
    try:
        rows = session.execute(get_hosts_list_query, (quantity,))
        if rows:
            return rows
        else:
            pass
    except:
        print("lost connection to Casandra server!!!")


        # init_db()
        # B1 - 1416412784.71 - 10.42.0.12 ; 192.168.7.2 ;
        #update_host_info('B1',1416412784.71,'10.42.0.12 ; 192.168.7.2')