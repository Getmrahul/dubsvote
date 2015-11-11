#! usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb


q = 'select vid from votes group by vid order by count(*) desc limit 5;'
db1 = MySQLdb.connect(host="localhost", user="man", passwd="***", db="dv")
c = db1.cursor()
c.execute(q)
record = c.fetchall()
row = []
if not record:
    print 'o'
for r in record:
    row.append(r)
db1.close()

for r in row:
    print r
