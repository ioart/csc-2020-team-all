# encoding: UTF-8

## Веб сервер
import json
import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import create_connection, connection_factory
from static  import index
from peewee import *

# класс для волонтеров
class Test:
  def __init__(self, name):
    self.name = name

  def get_name(self):
    return self.name


class Volunteers:
  def __init__(self, id, name, phone, task_id, start_datetime):
    self.id = id
    self.name = name
    self.phone = phone
    self.task_id = task_id
    self.start_datetime = start_datetime

  def get_id(self):
    return self.id

  def get_name(self):
    return self.name

  def get_phone(self):
    return self.phone

  def get_task_id(self):
    return self.task_id

  def get_start_datetime(self):
    return self.start_datetime


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
      return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def planets(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Planet P")
            result = []
            planets = cur.fetchall()
            for p in planets:
                result.append({"id": p[0], "name": p[1]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sportsman(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT id, name, country_id, volunteer_id  FROM Sportsmens")
          result = []
          commanders = cur.fetchall()
          for c in commanders:
              result.append({"id": c[0], "name": c[1], "counry_id":c[2], "volunteer_id":c[3]})
          return result
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * FROM Countries;")
          result = []
          commanders = cur.fetchall()
          for c in commanders:
            result.append({"id": c[0], "name": c[1]})
          return result
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def tasks(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * FROM Task;")
          result = []
          commanders = cur.fetchall()
          for c in commanders:
            result.append({"id": c[0], "name": c[1]})
          return result
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_tasks(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("INSERT INTO Task (volunteer_id, start_datetime, text) VALUES (1,'2020-11-19 12:00', 'a'), (2,'2020-11-19 13:00', 'b'), (1,'2020-11-19 14:00', 'c')")
          db.commit()
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        db = connection_factory.getconn()
        try:
              cur = db.cursor()
              cur.execute("SELECT * FROM Volunteers;")
              result = []
              volunteers = cur.fetchall()
              for c in volunteers:
                  result.append({"id": c[0], "name": c[1]})
              return result
        finally:
          connection_factory.putconn(db)

# получение волонтеров через пиви
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def new_volunteers(self):
        db = connection_factory.getconn()
        try:
            volunteers = Table('volunteers').bind(db)
            v= volunteers.select(volunteers.c.name)
            v = v.objects(Test)
            result = []
            for c in v:
                  result.append({"name": c.get_name()})
            return result
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_volunteers(self):
        db = connection_factory.getconn()
        try:
              cur = db.cursor()
              cur.execute("INSERT INTO Volunteers VALUES (3,'a', '34'), (4,'b', '43')")
              cur.execute("SELECT * FROM Volunteers;")
              result = []
              db.commit()
              volunteers = cur.fetchall()
              for c in volunteers:
                  result.append({"id": c[0], "name": c[1]})
              return result

        finally:
          connection_factory.putconn(db)




    @cherrypy.expose
    def register(self, sportsman, country, volunteer_id):
        status_message = 'SUCCESS'
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT id FROM Countries WHERE Countries.name=%s;", (country,))
          country_id, volunteer_id = int(cur.fetchone()[0]), int(volunteer_id)
          if sportsman.isdigit():
            sportsman_id = int(sportsman)
            cur.execute("UPDATE Sportsmens SET country_id=%s, volunteer_id=%s WHERE id=%s;", (country_id, volunteer_id, sportsman_id))
          else:
            cur.execute("INSERT INTO Sportsmens(name, gender, country_id, object_id, volunteer_id) VALUES(%s, %s, %s, 1, %s);", (sportsman, 'm', country_id, volunteer_id))  
        except Exception as e:
          status_message = f"Error: {e}"
        finally:
          connection_factory.putconn(db)
        return status_message


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id = None, sportsman_count = None, total_task_count = None):
      
        db = connection_factory.getconn()
        try:
            #tab_sportsmens = Table('sportsmens').bind(db)
            tab_task = Table('task').bind(db)
            tab_volunteers = Table('volunteers').bind(db)


            v = tab_volunteers.select(tab_volunteers.c.id,tab_volunteers.c.name, tab_volunteers.c.phone, tab_task.c.id.alias('task_id'), tab_task.c.start_datetime).join(tab_task, on=(tab_volunteers.c.id == tab_task.c.volunteer_id))
            v = v.objects(Volunteers)
            result = []
            for c in v:
                result.append({"name": c.get_name()})
            return result
        finally:
          connection_factory.putconn(db)





    # @cherrypy.expose
    # @cherrypy.tools.json_out()
    # def volunteers(self):
    # def volunteer_load(self, volunteer_id = None, sportsman_count = None, total_task_count = None):
    #     db = connection_factory.getconn()
    #     try:
    #       Volunteers = Table('Volunteers').bind(db)
    #       Task = Table('Task').bind(db)
    #       Sportsmens = Table('Sportsmens').bind(db)
    #       volunt = Volunteers.select(Volunteers.c.ID, Volunteers.c.name)
    #       if volunteer_id is not None:
    #         volunt = volunt.where(Volunteers.c.id == volunteer_id)
    #       Task = Table('Task').bind(db)
    #       volunt = volunt.select().join(Task, on=(Task.volunteer_id == volunt.ID))

    #       if total_task_count is not None:
    #         volunt_count = volunt.select(Volunteers.c.ID, fn.COUNT(Volunteers.c.ID)).groupby(volunt.ID).having(fn.COUNT(Volunteers.c.ID) >= total_task_count)
    #         volunt = volunt.select().join(Task, on=(Task.volunteer_id == volunt.ID))

    #         volunt = volunt_count.select(volunt_count.c.ID).join(volunt, on=(volunt_count.ID == volunt.ID))

    #       volunt = volunt.select().join(Sportsmens, on=(Sportsmens.volunteer_id == volunt.ID))
    #       if sportsman_count is not None:
    #         volunt_count = volunt.select(Volunteers.c.ID, fn.COUNT(Volunteers.c.ID)).groupby(volunt.ID).having(fn.COUNT(Volunteers.c.ID) >= sportsman_count)
    #         volunt = volunt.select().join(Task, on=(Task.volunteer_id == volunt.ID))

    #     finally:
    #       connection_factory.putconn(db)

  

def run():
    cherrypy_cors.install()    
    cherrypy.config.update({
      'server.socket_host': '0.0.0.0',
      'server.socket_port': 8080,
    })
    config = {
        '/': {
            'cors.expose.on': True,
        },
    }
    cherrypy.quickstart(App(parse_cmd_line()), config=config)

if __name__ == '__main__':
  run()
