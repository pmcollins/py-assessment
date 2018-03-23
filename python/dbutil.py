class DbUtil:

    def __init__(self, _connection):
        self._connection = _connection
        pass

    def execute_sql_files(self, fnames):
        """Executes multiple sql files. Useful for DDL statements and the like."""
        cursor = self.cursor()
        for fname in fnames:
            with open('../sql/' + fname + '.sql', 'r') as sql_file:
                sql = sql_file.read()
                cursor.execute(sql)
        cursor.close()

    def execute_sql(self, sql):
        cursor = self.cursor()
        cursor.execute(sql)
        cursor.close()

    def fetchall(self, fname):
        with open('../sql/' + fname + '.sql', 'r') as sql_file:
            sql = sql_file.read()
            cursor = self.cursor()
            cursor.execute(sql)
            out = cursor.fetchall()
            cursor.close()
        return out

    def get_proc_results(self, proc_name):
        cursor = self.cursor()
        cursor.callproc(proc_name)
        stored_results = cursor.stored_results()
        result = next(stored_results)
        out = result.fetchall()
        cursor.close()
        return out

    def cursor(self):
        # Convenience
        return self._connection.cursor()

    def commit(self):
        # Convenience
        self._connection.commit()
