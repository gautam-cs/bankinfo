import csv
import os
import psycopg2


class DumpData:
    def __init__(self):
        self.conn = psycopg2.connect(database="localdb",
                                     user="gautam",
                                     password="password@12",
                                     host="127.0.0.1",
                                     port="5432")

    def make_dump_csv(self):
        branch_list = list()
        bank_list = list()
        with open('{}/../bank_branches.csv'.format(os.getcwd()), 'r') as csvFile:
            reader = csv.reader(csvFile)
            header = True
            for row in reader:
                if header:
                    header = False
                else:
                    branch_list.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    if len(bank_list) == 0:
                        bank_list.append((row[1], row[7]))
                    elif row[1] not in [bank[0] for bank in bank_list]:
                        bank_list.append([row[1], row[7]])
        if bank_list:
            table = 'banks_banks'
            query = """INSERT INTO {} (bank_id, bank_name) VALUES (%s, %s) ON CONFLICT DO NOTHING""".format(table)
            self.insert_into_db(query, table, bank_list)
        if branch_list:
            table = 'banks_branches'
            query = """INSERT INTO {} (ifsc, bank_id_id, branch, address, city, district, state) VALUES 
                       (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;""".format(table)
            self.insert_into_db(query, table, branch_list)

    def insert_into_db(self, query, table, data):
        """
        :param query:
        :param table:
        :param data:
        :return:
        """
        cursor = self.conn.cursor()
        cursor.executemany(query, data)
        self.conn.commit()
        print(cursor.rowcount, "Record inserted successfully into {}".format(table))


if __name__ == "__main__":
    DumpData().make_dump_csv()
