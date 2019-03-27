import requests
from datetime import date
from db_connect import db

class WebStartup:

	def __init__(self, startup_id):
		self.id = startup_id

	def get_info(self, required_fields=False):
		if not required_fields:
			db_result = db.Startups.find_one({"id":self.id})
		else:
			db_result = db.Startups.find_one({"id":self.id}, required_fields)
		if not db_result:
			db_result = db.Startups.find_one({"email":self.id})
		return db_result

class WebInvestor:

	def __init__(self, investor_id):
		self.id = investor_id

	def get_info(self, required_fields=False):
		if not required_fields:
			db_result = db.Investors.find_one({"id":self.id})
		else:
			db_result = db.Investors.find_one({"id":self.id}, required_fields)
		if not db_result:
			db_result = db.Investors.find_one({"email":self.id})
		if not db_result:
			db_result = db.Investors.find_one({"name":self.id})
		return db_result

class WebUser:

	def __init__(self, investor_id):
		self.id = investor_id

	def get_info(self, required_fields=False):
		if not required_fields:
			db_result = db.Internal.find_one({"id":self.id})
		else:
			db_result = db.Internal.find_one({"id":self.id}, required_fields)
		if not db_result:
			db_result = db.Internal.find_one({"email":self.id})
		if not db_result:
			db_result = db.Internal.find_one({"name":self.id})
		return db_result

def pushStartup(startup):
	db.Startups.insert_one(startup)

def updateStartup(startup, updates):
	db.Startups.update_one({'_id': startup['_id']}, {'$set': updates}, upsert=False)

def pushInvestor(investor):
	db.Investors.insert_one(investor)

def updateInvestor(investor, updates):
	db.Investors.update_one({'_id': investor['_id']}, {'$set': updates}, upsert=False)

def parse_multi_form(form):
    data = {}
    for url_k in form:
        v = form[url_k]
        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data
