import os
import sqlite3
import unittest
 
class TestDatabase(): 
  db_url = "test_database.sqlite"
  def setUp(self):
      """
      Setup a temporary database
      """
      conn = sqlite3.connect(db_url)
      c = conn.cursor()

      # create a table
      c.execute("""CREATE TABLE albums
                        (title text, artist text, release_date text,
                         publisher text, media_type text)
                     """)
      # insert some data
      c.execute("INSERT INTO albums VALUES "
                     "('Glow', 'Andy Hunter', '7/24/2012',"
                     "'Xplore Records', 'MP3')")

      # save data to database
      conn.commit()

      # insert multiple records using the more secure "?" method
      albums = [('Exodus', 'Andy Hunter', '7/9/2002',
                 'Sparrow Records', 'CD'),
                ('Until We Have Faces', 'Red', '2/1/2011',
                 'Essential Records', 'CD'),
                ('The End is Where We Begin', 'Thousand Foot Krutch',
                 '4/17/2012', 'TFKmusic', 'CD'),
                ('The Good Life', 'Trip Lee', '4/10/2012',
                 'Reach Records', 'CD')]
      c.executemany("INSERT INTO albums VALUES (?,?,?,?,?)",
                         albums)
      conn.commit()

  def tearDown(self):
      os.remove(db_url)