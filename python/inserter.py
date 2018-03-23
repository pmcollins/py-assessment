class Inserter:
    """Given a table name and column names, inserts rows into a table."""

    def __init__(self, table_name, cols):
        """
        :param table_name: the name of the table
        :param cols: a tuple containing a the names of the columns
        """
        self._table_name = table_name
        self._cols = cols
        self._sql = self._generate_sql()

    def _generate_sql(self):
        fmt = ','.join(('%s',) * len(self._cols))
        return 'INSERT INTO ' + self._table_name + ' (' + ','.join(self._cols) + ') VALUES (' + fmt + ')'

    def insert(self, cursor, row):
        """Row should be in the same order as the columns defined in the constructor.

        If there are cells missing in the row, they will be appended.
        """
        row += [None] * (len(self._cols) - len(row))
        cursor.execute(self._sql, row)
