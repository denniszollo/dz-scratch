#!/usr/bin/env python3

import json
import os
import psycopg2
import sys


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(sys.argv[0]+": <serial_id>")
        sys.exit(1)
    else:
        serial_id = sys.argv[1]

    try:
        host = os.environ['PROVISION_URL']
        user = os.environ['PROVISION_USER']
        password = os.environ['PROVISION_PASSWORD']
        database = os.environ['PROVISION_DB']
    except KeyError:
        print("\n\t".join(['Must set:',
                          'PROVISION_URL',
                          'PROVISION_USER',
                          'PROVISION_PASSWORD',
                          'PROVISION_DB']))
        sys.exit(1)

    conn = psycopg2.connect(host=host,
                            user=user,
                            password=password,
                            database=database)



    cur = conn.cursor()
    cur.execute("SELECT device_dna FROM devices WHERE serial_id = '%s'" %
                serial_id)
    rows = cur.fetchall()
    print rows
