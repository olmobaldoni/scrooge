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
        data_result = []
        try:
            query = "SELECT " + ', '.join(headings) + ' FROM {};'.format(table)
            for row in self.__cursor.execute(query):
                data_result.append([row[0], row[1], row[2], row[3]])
            return data_result
        except sqlite3.Error as e:
            print("Error retrieving data: ", e)

        # query = 'SELECT {0} from {1};'.format(columns, table)
        # self.__cursor.execute(query)
        # rows = self.__cursor.fetchall()
        # return rows[len(rows) - limit if limit else 0:]

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

    def get_last(self, table, columns):
        return self.get(table, columns, limit=1)[0]

    def write(self, table,  data):
        '''
        Function to write data from the interface into the database.
        :param table:
        :param data:
        :return: None
        '''
        print(data)
        print(data['-TIPO_ENTRATA-'], data['-DATA_MOVIMENTO-'], data['-ENTRATA-'])
        self.__cursor.execute("INSERT INTO {} VALUES (?,?,?,?);".format(table), ( 'Entrata' if data['-MOVIMENTO_ENTRATA-'] else 'Uscita', data['-TIPO_ENTRATA-'], data['-DATA_MOVIMENTO-'], data['-ENTRATA-']))
        self.__conn.commit()
        # per scrivere in tutti i campi della tabella
        # self.__cursor.execute("INSERT INTO {} VALUES (?,?,?,?);".format(table), (data[0], data[1], data[2], data[3]))
        # per scrivere solo nel campo ID
        # self.__cursor.execute("INSERT INTO {} (ID) VALUES (?);".format(table), (data[0], ))
        # per scrivere tutti i campi eccetto ID
        # self.__cursor.execute("INSERT INTO {} (NOME, INDIRIZZO, NUMERO_DI_TELEFONO) VALUES (?,?,?);".format(table), (data[0], data[1], data[2]))

    def update(self, name):
        self.__cursor.execute("UPDATE {} SET ID = 2000".format(name))

    def create_table(self, name, headings):
        '''
        Function that shows all tables in the database
        :param name:
        :param headings:
        :return:
        '''
        try:
            query = "CREATE TABLE {} (".format(name) + ', '.join(headings) + ');'
            self.__cursor.execute(query)
        except sqlite3.Error as e:
            print('Error creating database: ', e)

    def list_tables(self):
        '''
        Function that shows all tables in the database
        :return:
        '''
        tables = []
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.__cursor.execute(query)
        for row in self.__cursor.fetchall():
            tables.append(row[0])
        return tables

    def delete_table(self, name):
        '''
        Fuction that delete the specified table from the database
        :param name:
        :return:
        '''
        self.__conn.execute("DROP TABLE {}".format(name))





