import sqlite3


class Database:

    def __init__(self, name=None):
        self.__conn = None
        self.__cursor = None

        if name:
            self.open_connection(name)

    def open_connection(self, name):
        try:
            self.__conn = sqlite3.connect(name)
            self.__cursor = self.__conn.cursor()
        except sqlite3.Error as e:
            print('Error connecting to database: ', e)

    def close_connection(self):
        if self.__conn:
            self.__conn.commit()
            self.__cursor.close()
            self.__conn.close()

    def get(self, table, headings, limit=None):
        '''
        Function that returns records from specified table
        :param table:
        :param headings:
        :param limit:
        :return:
        '''
        try:
            data_result = []
            query = "SELECT " + ', '.join(headings) + ' FROM {};'.format(table)
            for row in self.__cursor.execute(query):
                data_result.append([row[0], row[1], row[2], row[3], row[4]])
            return data_result
        except sqlite3.Error as e:
            print("Error retrieving data: ", e)

    def get_specified(self, table, headings, condition):
        '''
        Function that returns records filtered by the condition
        :param table:
        :param headings:
        :param condition:
        :return: iterator
        '''
        try:
            query = "SELECT " + ', '.join(headings) + ' FROM {} '.format(table) + condition
            return self.__cursor.execute(query)
        except sqlite3.Error as e:
            print("Error retrieving data: ", e)

    def write(self, table,  data):
        '''
        Function to write data from the interface into the database.
        :param table:
        :param data:
        :return: None
        '''
        try:
            if data['-MOVIMENTO_ENTRATA-']:
                self.__cursor.execute("INSERT INTO {} (TIPO_DI_MOVIMENTO,CATEGORIA,DATA,IMPORTO) VALUES (?,?,?,?);".format(table), ('Entrata', data['-TIPO_ENTRATA-'], data['-DATA_MOVIMENTO-'], data['-ENTRATA-']))
            elif data['-MOVIMENTO_USCITA-']:
                self.__cursor.execute("INSERT INTO {} (TIPO_DI_MOVIMENTO,CATEGORIA,DATA,IMPORTO) VALUES (?,?,?,?);".format(table), ('Uscita', data['-TIPO_USCITA-'], data['-DATA_MOVIMENTO-'], data['-USCITA-']))
        except sqlite3.Error as e:
            print('Error writing data: ', e)

    def create_table(self, name):
        try:
            query = ('''CREATE TABLE {}
                    (ID                     INTEGER     PRIMARY KEY,
                     TIPO_DI_MOVIMENTO      TEXT        NOT NULL,
                     CATEGORIA              TEXT        NOT NULL,
                     DATA                   TEXT        NOT NULL,
                     IMPORTO                REAL        NOT NULL);'''.format(name))
            self.__cursor.execute(query)
        except sqlite3.Error as e:
            print('Error creating database: ', e)

    def list_tables(self):
        '''
        Function that shows all tables in the database
        :return:
        '''
        try:
            tables = []
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            self.__cursor.execute(query)
            for row in self.__cursor.fetchall():
                tables.append(row[0])
            return tables
        except sqlite3.Error as e:
            print('Error retrieving tables: ', e)

    def delete_table(self, name):
        '''
        Function that delete the specified table from the database
        :param name:
        :return:
        '''
        self.__conn.execute("DROP TABLE {}".format(name))

    def delete_row(self, name, row_id):
        '''
        Function that delete the specified row from the specified table
        :param name:
        :param row_id:
        :return:
        '''
        try:
            query = ('DELETE FROM {0} WHERE ID = {1};'.format(name, row_id))
            self.__cursor.execute(query)
        except sqlite3.Error as e:
            print('Error deleting row: ', e)





