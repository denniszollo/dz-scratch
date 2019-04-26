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



    fields = ['serial_id', 'accel_bias', 'accel_mat', 'gyro_bias', 'gyro_g', 'gyro_mat']
    cur = conn.cursor()
    cur.execute("SELECT %s FROM imus WHERE serial_id = '%s'" %
                (", ".join(fields), serial_id))
    rows = cur.fetchall()
    assert(len(rows) == 1)

    d = dict(zip(fields, rows[0]))
    d['accel_mat'] = chunks(d['accel_mat'], 3)
    d['gyro_g'] = chunks(d['gyro_g'], 3)
    d['gyro_mat'] = chunks(d['gyro_mat'], 3)

    print(json.dumps(d))