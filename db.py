#! usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2

from os.path import exists
from os import makedirs
import os
import urllib2
import json
import urlparse

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ.get('DATABASE_URL',"postgres://axecxeqjnmwkze:DLX3qKpnBJqykUiZ2O1oEzmcnc@ec2-23-21-140-156.compute-1.amazonaws.com:5432/deuv2gal5pgae2"))

det = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

def connect():
	return psycopg2.connect(det)

class db(object):
	def counts(self):
		con = connect()
		c = con.cursor()
		q = "select count(*) from dubs;"
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def video(self, id):
		q = "select url, ol from dubs where id='%d'" % id
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def votes(self, vid):
		try:
			q = "insert into votes (vid) values('%d')" % vid
			con = connect()
			c = con.cursor()
			c.execute(q)
			con.commit()
			con.close()
			return True
		except Excpetion:
			#con.commit()
			con.close()
			return False

	def account_check(self, email):
		q = "select id, username from clients where email='%s'" % email
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchone()
		con.close()
		if not record:
			return 1
		else:
			return 0
	def custom(self, url):
		con = connect()
		c = con.cursor()
		try:
			tq = "select count(1) from dubs where url='%s';" % url
			c.execute(tq)
			tdb = c.fetchone()
			if tdb[0]:
				con.commit()
				con.close()
				#print "\nDuplicate found-%s" % ol
				return False
			else:
				q = "insert into dubs (url, ol, votes) values('%s','%s','%d')" % (url,'#', 0)
				c.execute(q)
				con.commit()
				con.close()
				return True
		except Exception as EXP:
			con.commit()
			con.close()
			print False

	def dubs(self, url, ol):
		con = connect()
		c = con.cursor()
		try:
			tq = "select count(1) from dubs where ol='%s';" % ol
			c.execute(tq)
			tdb = c.fetchone()
			if tdb[0]:
				con.commit()
				con.close()
				print "\nDuplicate found-%s" % ol
			else:
				q = "insert into dubs (url, ol, votes) values('%s','%s','%d')" % (url,ol, 0)
				c.execute(q)
				con.commit()
				con.close()
				print ol
		except Exception as EXP:
			con.commit()
			con.close()
			print EXP
	def selectall(self, tab, cName, cValue):
		q = "select * from %s where %s='%s' order by id desc" % (tab, cName, cValue)
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchall()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def select(self, tab, cName, cValue):
		q = "select * from %s where %s='%s'" % (tab, cName, cValue)
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def vcheck(self, tab, cName1, cValue1, cName2, cValue2 , cName3, cValue3):
		q = "select * from %s where %s='%s' and %s='%s' and %s='%s'" % (tab, cName1, cValue1, cName2, cValue2, cName3, cValue3)
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchone()
		con.close()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def select2(self, tab, cName1, cValue1, cName2, cValue2):
		q = "select * from %s where %s='%s' and %s='%s'" % (tab, cName1, cValue1, cName2, cValue2)
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchone()
		con.close()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def vupdate(self, id, vote):
		q = "update vote set vote=%d where id=%d" % (vote, id)
		con = connect()
		c = con.cursor()
		c.execute(q)
		con.commit()
		con.close()
	def pv(self, pollId, vote, ip, device, dname, email, cc):
		q = "insert into vote (pollId, vote, ip, device, dname, email, country_city) values ('%s', '%d', '%s', '%d', '%s', '%s', '%s')" % (pollId, vote, ip, device, dname, email, cc)
		con = connect()
		c = con.cursor()
		c.execute(q)
		con.commit()
		con.close()
	def totalVotes(self, pid):
		q = "select count(id) from vote where pollId='%s'" % pid
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchall()
		con.close()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def getPolls(self, email):
		q = "select pid, question from poll where email='%s' order by id desc" % email
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchall()
		con.close()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def delete(self, tab, cName, cValue):
		q = "delete from %s where %s='%s'" % (tab, cName, cValue)
		con = connect()
		c = con.cursor()
		c.execute(q)
		con.commit()
		con.close()
