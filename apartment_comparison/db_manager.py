import sqlite3


class ApartmentsDBManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    def _execute(self, sql, params=None):
        with self.connection as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor

    def _get_column_names_from_table(self, table):
        data = self._execute('select * from apartments limit 1')
        columns = [d[0] for d in data.description if d[0] != 'id']
        return columns

    def _create_column_insert_query(self, columns):
        names = ', '.join(columns)
        sql_values = ', '.join([f':{name}' for name in columns])
        query = f'''
        insert into apartments ({names})
        values
        ({sql_values});
        '''
        return query

    def get_all_apartments(self):
        rows = self._execute('select * from apartments').fetchall()
        return [dict(row) for row in rows]

    def get_apartment(self, id):
        apt = self._execute(f'select * from apartments where id = {id}').fetchone()
        return dict(apt)

    def add_apartment(self, apartment):
        columns = self._get_column_names_from_table('apartments')
        insert_query_sql = self._create_column_insert_query(columns)
        self._execute(insert_query_sql, params=apartment)

    def update_apartment(self, info):
        id = info.pop('id')
        info.pop('name')
        info.pop('address')
        info.pop('url')
        columns = list(info.keys())
        col_placeholders = ', '.join([f'{column} = ?' for column in columns])
        values = tuple(list(info.values()) + [id])
        update_sql = f'update apartments set {col_placeholders} where id = ?'
        self._execute(update_sql, values)

    def delete_apartment(self, id):
        apartment = self._execute(f'select * from apartments where id = {id}').fetchone()
        if apartment:
            self._execute(f'delete from apartments where id = {id}')
            return f'Deleted apartment: {dict(apartment)}'
        else:
            return f'No apartment with id: {id}'

    def execute_sql_file(self, file):
        with open(file, 'r') as f:
            with self.connection as conn:
                cursor = conn.cursor()
                sql = f.read()
                cursor.executescript(sql)

    def get_feature_types(self):
        rows = self._execute('select name, type from feature_types_mapping').fetchall()
        tuples = [tuple(row) for row in rows]
        return {t[0]: t[1] for t in tuples}

    def _add_feature_to_apartments(self, column_name, column_type):
        alter_table_sql = (
            f'alter table apartments add column {column_name} {column_type};'
        )
        self._execute(alter_table_sql)

    def _add_feature_to_feature_map(self, column_name, column_type):
        update_mapping_sql = f"""
        insert into feature_types_mapping(name, type)
        values ('{column_name}', '{column_type}');
        """
        self._execute(update_mapping_sql)

    def add_feature(self, feature_name, column_name):
        self._add_feature_to_apartments(feature_name, column_name)
        self._add_feature_to_feature_map(feature_name, column_name)