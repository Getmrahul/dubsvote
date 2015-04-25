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
	def create(self, q):
		con = connect()
		c = con.cursor()
		c.execute(q)
		con.commit()
		con.close()
	def login_e(self, email):
		con = connect()
		c = con.cursor()
		q = "select name,status from clients where email='%s'" % (email)
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def login_ep(self,email,password):
		con = connect()
		c = con.cursor()
		q = "select * from clients where email='%s' and password='%s'" % (email, password)
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def pro(self, username):
		con = connect()
		c = con.cursor()
		q = "select * from clients where username='%s'" % (username)
		c.execute(q)
		record = c.fetchone()
		row = []
		if not record:
			return row
		for r in record:
			row.append(r)
		con.close()
		return row
	def signup_username(self, username):
		q = "select id, username from clients where username='%s'" % username
		con = connect()
		c = con.cursor()
		c.execute(q)
		record = c.fetchone()
		con.close()
		if not record:
			return 1
		else:
			return 0
	def createPoll(self, pollId, question, textvalue, textprop, tbl, ibl, nop, otype, email):
		q = "insert into poll (pid, question, textvalue, textproperty, textblacklist, imageblacklist, noi, otype, email) values('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s')" % (pollId, question, textvalue, textprop, tbl, ibl, int(nop), int(otype), email)
		con = connect()
		c = con.cursor()
		c.execute(q)
		con.commit()
		con.close()

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

url = "https://api.instagram.com/v1/tags/dubsmash/media/recent?access_token=1718233349.1fb234f.a3ce3d1ff2864de1914ce73b342481ad"
mC = 0
while mC < 500:
	i = 0
	r1 = urllib2.urlopen(url).read()
	js = json.loads(r1)
	url = js["pagination"]["next_url"]
	dc = len(js["data"])
	while i < dc:
		try:
			video = js["data"][i]["videos"]["low_bandwidth"]["url"]
			sp = video.split('.')
			lv = len(sp)
			ol = js["data"][i]["link"]
			if sp[lv-1].lower() == "mp4":
				obj = db()
				try:
					obj.dubs(video,ol)
					mC = mC + 1
				except Exception as Exp:
					print Exp
		except Exception:
			dd = 1
			print "nv"
		i = i + 1
print "done"