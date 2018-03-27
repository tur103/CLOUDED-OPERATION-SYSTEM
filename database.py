import sqlite3
from constants import *


class Database(object):
    def __init__(self):
        self.database = sqlite3.connect(DATABASE_PATH)

    def create_last_edited_table(self):
        self.database.execute("create table last(name text, first text, second text, "
                              "third text, forth text, fifth text);")
        self.database.execute("insert into last (name, first, second, third, forth, fifth) "
                              "values ('last', '', '', '', '', '')")
        self.database.commit()

    def drop_last_edited_table(self):
        self.database.execute("drop table if exists last")

    def update_last_edited_database(self, new_file):
        order_list = self.get_last_edited_table()
        if order_list[0] != new_file:
            if new_file in order_list:
                order_list.remove(new_file)
                order_list.append(new_file)
            for place in range(1, len(order_list)):
                order_list[place * -1] = order_list[(place + 1) * -1]
            order_list[0] = new_file
            self.database.execute("update last set first = '%s', second = '%s', "
                                  "third = '%s', forth = '%s', fifth = '%s' "
                                  "where name = 'last'" % (order_list[0], order_list[1], order_list[2],
                                                           order_list[3], order_list[4]))
            self.database.commit()

    def get_last_edited_table(self, name=False):
        cursor = self.database.execute("select first, second, third, forth, fifth from last where name = 'last'")
        order_list = []
        for row in cursor:
            for file in row:
                if name:
                    file = file.split("\\")[-1]
                order_list.append(file)
        return order_list

    def close_database(self):
        self.database.close()