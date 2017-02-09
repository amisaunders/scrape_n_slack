#!/usr/bin/env python

""" define a database
which will be used to store the results 
after each scrape 
and compare to past scrapes to avoid duplicates """


# import external library modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
	"""
	A table to store data on craigslist listings.
	"""

	__tablename__ = 'listings'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	link = Column(String, unique=True)
	price = Column(Float)
	where = Column(String)
	cl_id = Column(Integer, unique=True)
	# created = Column(DateTime)
	created = Column(String)
	area = Column(String)
	##############################
	# geotag = Column(String)
	# lat = Column(Float)
	# lon = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def filter_new_post(result):
	""" 
	Filters out of scrape a new post
	Appends all new posts into an SQL database 
	Returns a set of new posts to be posted to Slack
	"""

	# try:
	# 	result = next(post)
	# except StopIteration:
	# 	break
	# except Exception:
	# 	continue
	# listing = session.query(Listing).filter_by(cl_id=post["id"]).first()
	# listing = session.query(Listing).filter(Listing.cl_id == result["id"]).first()
	listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

	# Don't post the listing if it already exists, AND
	# Don't store the listing if it already exists.
	if listing is None:

		# Try parsing the price.
		price = 0
		try:
			price = float(result["price"].replace("$", ""))
		except Exception:
			pass

		# Try parsing the where.
		where = ""
		try:
			where = String(result["where"].replace(""))
		except Exception:
			pass

		# Create the listing object.
		listing = Listing(
			name=result["name"],
			link=result["url"],
			price=price,
			where=where,
			cl_id=result["id"],
			# area=result["area"],
			area="sfo",
			created=(result["datetime"])
			)

		# Save the listing so we don't grab it again.
		session.add(listing)
		session.commit()

		# return the listing for posting in slack
		# new_posts.append(result)

		# return new_post
		return result

	else:
		return None
		# comment out after it's working
		print "Old"

