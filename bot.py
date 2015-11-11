#! usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import urllib2
import json

class db(object):
	def dubs(self, url, ol):
		db1 = MySQLdb.connect(host="localhost", user="man", passwd="*****", db="dv")
		c = db1.cursor()
		try:
			tq = "select count(1) from dubvideos where ol='%s';" % ol
			c.execute(tq)
			tdb = c.fetchone()
			if tdb[0]:
				db1.commit()
				db1.close()
				print "\nDuplicate found-%s" % ol
			else:
				q = "insert into dubvideos (url, ol, lang) values('%s','%s','%d')" % (url,ol, 2)
				c.execute(q)
				db1.commit()
				db1.close()
				print ol
		except Exception as EXP:
			db1.commit()
			db1.close()
			print EXP

url = "https://api.instagram.com/v1/tags/dubsmashtamil/media/recent?access_token=1718233349.1fb234f.a3ce3d1ff2864de1914ce73b342481ad"
mC = 0
while mC < 439:
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
