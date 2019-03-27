from pymongo import MongoClient

MONGODB_URI = "mongodb://admin:willwontwin1!@ds113692.mlab.com:13692/incub8sf"
client = MongoClient(MONGODB_URI, connectTimeOutMS=30000)
db = client.get_default_database()
# db = client.admin
investors_database = db.Investors
startups_database = db.Startups