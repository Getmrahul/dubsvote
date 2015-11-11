#! usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import urllib2
import json

class db(object):
	def counts(self):
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
		c = db1.cursor()
		q = "select count(*) from dubvideos;"
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		db1.close()
		return row
	def video(self, id):
		q = "select url, ol from dubvideos where id=%d;" % id
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*******", db="dv")
		c = db1.cursor()
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		db1.close()
		return row
	def videoIds(self, id):
		q = "select id from dubvideos where lang=%d" % id
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="****", db="dv")
		c = db1.cursor()
		c.execute(q)
		record = c.fetchall()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		db1.close()
		return row
	def videoUrl(self, url):
		q = "select id, url from dubvideos where url='%s'" % url
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
		c = db1.cursor()
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		db1.close()
		return row

	def votes(self, vid):
		try:
			q = "insert into votes (vid) values('%d')" % vid
			db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
			c = db1.cursor()
			c.execute(q)
			db1.commit()
			db1.close()
			return True
		except Excpetion as EXP:
			#db1.commit()
			db1.close()
			print EXP
			return False

	def custom(self, url, lang):
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
		c = db1.cursor()
		try:
			tq = "select count(1) from dubvideos where url='%s';" % url
			c.execute(tq)
			tdb = c.fetchone()
			if tdb[0]:
				db1.commit()
				db1.close()
				#print "\nDuplicate found-%s" % ol
				return False
			else:
				q = "insert into dubvideos (url, ol, lang) values('%s','%s','%d')" % (url,'#'+url, lang)
				c.execute(q)
				db1.commit()
				db1.close()
				return True
		except Exception as EXP:
			db1.commit()
			db1.close()
			print EXP
			return False

	def dubs(self, url, ol):
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
		c = db1.cursor()
		try:
			tq = "select count(1) from dubs where ol='%s';" % ol
			c.execute(tq)
			tdb = c.fetchone()
			if tdb[0]:
				db1.commit()
				db1.close()
				print "\nDuplicate found-%s" % ol
			else:
				q = "insert into dubs (url, ol, votes) values('%s','%s','%d')" % (url,ol, 0)
				c.execute(q)
				db1.commit()
				db1.close()
				print ol
		except Exception as EXP:
			db1.commit()
			db1.close()
			print EXP
	def topVideos(self,no):
		q = 'select vid from votes group by vid order by count(*) desc limit %d;' % no
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
		c = db1.cursor()
		c.execute(q)
		record = c.fetchall()
		row = []
		if not record:
		    return row
		for r in record:
		    row.append(r)
		db1.close()
		return row
