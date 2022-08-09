import datetime
import json
import math
import numpy as np
import pandas as pd
import re

from db.database import SessionLocal
from logging_format import logger
from tqdm import tqdm
import time

PATH_TO_LOG = 'log/'
NAME_LOG = 'log_.txt'


class TypeErrors:

    # def __init__(self, df: pd.DataFrame, name_table: str, pk: list, df_pmc: pd.DataFrame):
    def __init__(self, df: pd.DataFrame, name_table: str, pk: list):
        self.df = df
        self.name_table = name_table
        self.pk = pk
        # self.df_pmc = df_pmc
        # self.data = {}
        self.data = {
            'Very big value': [],
            'Very small value': [],
            'Wrong sign': [],
            'Small data': [],
            'Big data': [],
            'Error span year': [],
            'Mismatch of values in two tables': [],
        }

    # def progress_bar(self, list_valid):
    #     kol_all_rows = self.df.shape[1]
    #     for i in tqdm(list_valid):
    #         # time.sleep(1)
    #         i()

    @staticmethod
    def find_max_type(type_columns_):
        dict_type_column = dict(zip(type_columns_, [type_columns_.count(i) for i in type_columns_]))
        max_type = ''
        if type_columns_:
            max_type = max(dict_type_column, key=dict_type_column.get)
        return max_type, dict_type_column

    def write_to_dict(self):
        with open('/'.join((PATH_TO_LOG, NAME_LOG)), 'a+') as outfile:
            outfile.write('{"Table": [ \n')
            outfile.write(f'"{self.name_table}",')
            json.dump(self.data, outfile)
            outfile.write(']}, \n')

    @staticmethod
    def func_all_int_float_array(column1, type_columns) -> list:
        # return [column1[i] for i, value in enumerate(column1) if
        #         (type_columns[i] == int or type_columns[i] == float or type_columns[i] == np.float32
        #          or type_columns[i] == np.float64 or type_columns[i] == np.int64 or type_columns[i] == np.int32)]
        return [column1[i] for i, value in enumerate(column1) if
                (not np.isnan(column1[i])) and (type(column1[i]) == int or
                                                type(column1[i]) == float or
                                                type(column1[i]) == np.float32 or
                                                type(column1[i]) == np.float64 or
                                                type(column1[i]) == np.int64 or
                                                type(column1[i]) == np.int32)]

    def sign_warning(self, column_index, begin_table, column1, type_columns) -> list:
        all_int_float_array = self.func_all_int_float_array(column1, type_columns)
        minus_int_float_array = [i for i in all_int_float_array if i < 0]
        error_sign = []
        if len(all_int_float_array) > len(minus_int_float_array) >= 1 and len(minus_int_float_array) < len(
                column1) // 10:
            for row, elem in enumerate(column1):
                if elem in minus_int_float_array:
                    self.print_name_table_row_pk(self.df, column_index, self.name_table,
                                                 self.df.values[row + begin_table - 1][column_index],
                                                 row, True, self.pk, 'Wrong sign')

                    error_sign.append([column_index, row])
        return error_sign

    def big_small_value_warning(self, column_index, column1, type_columns, error_sign):
        all_int_float_array = self.func_all_int_float_array(column1, type_columns)
        if len(all_int_float_array) != len(column1):
            print('Nane in column1')
            column1 = all_int_float_array

        error_sign_values = []
        if error_sign:
            minus_values = [error_sign[j][1] for j in range(len(error_sign)) if column_index == error_sign[j][0]]
            error_sign_values = [column1[i] for i in minus_values]
        try:
            uniq_resource = np.unique(self.df['id_resource'])
            for id_resource in uniq_resource:
                index = [i for i, value in enumerate(self.df['id_resource']) if value == id_resource]
                quant = np.quantile(column1[index], 0.9)
                quant_05 = np.quantile(column1[index], 0.5)
                k = quant * len(column1[index]) // (10 ** (len(str(len(column1[index]))) - 1))
                mean = np.mean(column1[index])

                if k == 0:
                    k = quant
                # print('k = ', k)
                for row, elem in enumerate(column1[index]):
                    if elem in all_int_float_array and elem not in error_sign_values:

                        if elem > k:
                            if elem > mean:
                                self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, index[row],
                                                             True,
                                                             self.pk, 'Very big value')
                                # print(f'{elem} too big. mean = {np.mean(column1)} ')

                                logger.warning(
                                    f'warning big value {elem}, id_resource = {id_resource}, mean = {np.mean(column1)}, k = {k} ')

                        if elem < quant // len(column1[index]) // 10:
                            if elem <= mean:
                                # print("elem = ", elem)
                                # print("quant // len(column1[index]) // 10 = ", quant // len(column1[index]) // 10)
                                self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, index[row],
                                                             True,
                                                             self.pk, 'Very small value')

                                logger.warning(
                                    f'warning small value {elem}, id_resource = {id_resource}, mean = {np.mean(column1)}, k = {k} ')
        except:
            quant = np.quantile(column1, 0.9)
            np.quantile(column1, 0.5)
            # print(f'QUAINTIL = {quant}')
            quant_05 = np.quantile(column1, 0.5)
            column1_big = [column1 > quant * len(column1) // 100]
            column1_small = [column1 < quant // len(column1) // 10]

            # sql_ = f'''
            # select 	* from {}
            #     where parent_id_resource>=5000
            # '''
            if column1_big:
                self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, row, True, self.pk,
                                             'Very big value')
                logger.warning(
                    f'warning big value {elem} in cell : column = {column_index} row = {row}')
            for row, elem in enumerate(column1):
                if elem in all_int_float_array and elem not in error_sign_values:

                    if elem > quant * len(column1) // 100:  # (10**(len(str(len(column1)))-1)):

                        self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, row, True, self.pk,
                                                     'Very big value')
                        logger.warning(
                            f'warning big value {elem} in cell : column = {column_index} row = {row}')

                    if elem < quant // len(column1) // 10:
                        self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, row, True, self.pk,
                                                     'Very small value')

                        logger.warning(
                            f'warning small value {elem} in cell : column = {column_index} row = {row}')

    def big_small_value_warning_sql(self, column_index, column1, type_columns, error_sign, name_column):
        all_int_float_array = self.func_all_int_float_array(column1, type_columns)
        if len(all_int_float_array) != len(column1):
            print('Nane in column1')
            column1 = all_int_float_array

        error_sign_values = []
        if error_sign:
            minus_values = [error_sign[j][1] for j in range(len(error_sign)) if column_index == error_sign[j][0]]
            error_sign_values = [column1[i] for i in minus_values]
        try:
            # TODO: изменить
            uniq_resource = np.unique(self.df['id_resource'])
            for id_resource in uniq_resource:
                index = [i for i, value in enumerate(self.df['id_resource']) if value == id_resource]
                quant = np.quantile(column1[index], 0.9)
                quant_05 = np.quantile(column1[index], 0.5)
                k = quant * len(column1[index]) // (10 ** (len(str(len(column1[index]))) - 1))
                mean = np.mean(column1[index])

                if k == 0:
                    k = quant
                # print('k = ', k)
                for row, elem in enumerate(column1[index]):
                    if elem in all_int_float_array and elem not in error_sign_values:

                        if elem > k:
                            if elem > mean:
                                self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, index[row],
                                                             True,
                                                             self.pk, 'Very big value')
                                # print(f'{elem} too big. mean = {np.mean(column1)} ')

                                logger.warning(
                                    f'warning big value {elem}, id_resource = {id_resource}, mean = {np.mean(column1)}, k = {k} ')

                        if elem < quant // len(column1[index]) // 10:
                            if elem <= mean:
                                self.print_name_table_row_pk(self.df, column_index, self.name_table, elem, index[row],
                                                             True,
                                                             self.pk, 'Very small value')

                                logger.warning(
                                    f'warning small value {elem}, id_resource = {id_resource}, mean = {np.mean(column1)}, k = {k} ')
        except:
            quant = np.quantile(column1, 0.9)
            np.quantile(column1, 0.5)
            big_q = quant * len(column1) // 100
            small_q = quant // len(column1) // 10
            if type(self.pk) == str:
                sql_big = f'''
                            select 	{self.pk}, {name_column} from {self.name_table} 
                                where {self.df.columns[column_index]}>{big_q}
                            '''
                sql_small = f'''select 	{self.pk}, {name_column} from {self.name_table} 
                                  where {self.df.columns[column_index]}< {small_q}
                                            '''
            else:

                sql_big = f'''select 	{self.pk[0]},{self.pk[1]}, {name_column} from {self.name_table} 
                                 where {self.df.columns[column_index]}>{big_q}
                                            '''
                sql_small = f'''select 	{self.pk[0]},{self.pk[1]}, {name_column} from {self.name_table} 
                                 where {self.df.columns[column_index]}< {small_q}
                                                            '''
            with SessionLocal() as db:
                column1_big = db.execute(sql_big).fetchall()
                column1_small = db.execute(sql_small).fetchall()
                if column1_big:
                    self.print_name_table_row_pk_sql(self.df, column_index, self.name_table, column1_big, True, self.pk,
                                                     'Very big value', 0)
                if column1_small:
                    self.print_name_table_row_pk_sql(self.df, column_index, self.name_table, column1_big, True, self.pk,
                                                     'Very small value', 0)

    def check_date(self, column1, column_index):
        date_today = datetime.date.today()

        too_big_year = [i for i, value in enumerate(column1) if value.year > date_today.year + 5]
        # too_big_year = [i for i, value in enumerate(column1) if value.year == date_today.year ]
        too_small_year = [i for i, value in enumerate(column1) if value.year < date_today.year - 5]
        if too_big_year:
            for i in too_big_year:
                self.print_name_table_row_pk(self.df, column_index, self.name_table, column1[i], i, True, self.pk,
                                             'Big data')
                logger.warning(
                    f'warning big year in cell : column = {column_index} row = {i}')
        if too_small_year:
            for i in too_small_year:
                self.print_name_table_row_pk(self.df, column_index, self.name_table, column1[i], i, True, self.pk,
                                             'Small data')
                logger.warning(
                    f'warning small year in cell : column = {column_index} row = {i}')

    def check_date_sql(self, column_index):
        date_today = datetime.date.today()
        big_date = date_today.year + 5
        small_date = date_today.year - 5
        sql_big_year = f'''
            select * from {self.name_table}
            where DATE_PART('year', "{self.df.columns[column_index]}"::date)> {big_date}
            '''
        sql_small_year = f'''
                    select * from {self.name_table}
                    where DATE_PART('year', "{self.df.columns[column_index]}"::date)< {small_date}
                    '''
        with SessionLocal() as db:
            too_big_year = db.execute(sql_big_year).fetchall()
            too_small_year = db.execute(sql_small_year).fetchall()

        if too_big_year:
            self.print_name_table_row_pk_sql(self.df, column_index, self.name_table, too_big_year, True, self.pk,
                                             'Big data', 0)
        if too_small_year:
            self.print_name_table_row_pk_sql(self.df, column_index, self.name_table, too_small_year, True, self.pk,
                                             'Small data', 0)

    @staticmethod
    def conv_type_for_json(column1, two_pk, pk):
        dict_value = {}
        if pk:
            word = 'PK'
            word2 = 'PK_2'
        else:
            word = 'value'
            word2 = 'value_pmc'
        if two_pk:
            print(f'{word} = {column1[0]}')
            print(f'{word2} = {column1[1]}')
            if type(column1[0]) == int and type(column1[1]) == int:
                dict_value = {
                    f'{word}': int(column1[0]),
                    f'{word2}': int(column1[1])}
            elif (type(column1[0]) == float or type(column1[0]) == np.float64 or type(column1[0]) == np.float32) and \
                    (type(column1[1]) == float or type(column1[1]) == np.float64 or type(column1[1]) == np.float32):
                dict_value = {
                    f'{word}': float(column1[0]),
                    f'{word2}': float(column1[1])}
            elif type(column1[0]) == str or type(column1[1]) == datetime.datetime:
                dict_value = {
                    f'{word}': str(column1[0]),
                    f'{word2}': str(column1[1])}
        else:
            print(f'{word} = {column1}')
            if type(column1) == np.float64 or type(column1) == np.float32 or type(column1) == float:
                dict_value = {f'{word}': float(column1)}
            elif type(column1) == np.int:
                dict_value = {f'{word}': int(column1)}
            elif type(column1) == str or type(column1) == datetime.datetime:
                dict_value = {f'{word}': str(column1)}

        return dict_value

    def print_name_table_row_pk(self, df, i, name_table, column1, j, one_table, PK, type_error):
        dict_ = {'name_table': name_table,
                 'name_column': df.columns[i]}
        dict_PK = {}
        dict_value = {}

        print(f'name column = {df.columns[i]}')
        if not one_table:
            if type(PK) == str:
                print(f'PK {PK} = {df[PK].values[j]}')
                dict_PK = {'PK': int(df[PK].values[j])}

                # print(f'PK {PK} = {df[PK].values[j][0]}')
                # dict_PK = {'PK': int(df[PK].values[j][0])}
            else:
                print(f'PK {PK[0]} = {df[PK[0]].values[j]}')
                print(f'PK2 {PK[1]} = {df[PK[1]].values[j]}')
                dict_PK = {
                    PK[0]: int(df[PK[0]].values[j]),
                    PK[1]: int(df[PK[1]].values[j])}

                # print(f'PK {PK[0]} = {df[PK[0]].values[j][0]}')
                # print(f'PK2 {PK[1]} = {df[PK[1]].values[j][0]}')
                # dict_PK = {
                #     PK[0]: int(df[PK[0]].values[j][0]),
                #     PK[1]: str(df[PK[1]].values[j][0])}
            # print(f'{name_table} value = {column1[j][i]}')
            # print(f'{name_table}_pmc value = {column1[j+1][i]} \n')
            # values = [column1[j][i], column1[j][i + (df.shape[1]) // 2]]
            values = [column1[j][i], column1[j + 1][i]]
            dict_value = self.conv_type_for_json(values, True, False)
        else:
            if type(PK) == str:
                print(f'PK {PK} = {df[PK].values[j]}')
                dict_PK = {'PK': int(df[PK].values[j])}
            else:
                print(f'PK {PK[0]} = {df[PK[0]].values[j]}')
                print(f'PK2 {PK[1]} = {df[PK[1]].values[j]}')
                dict_PK = {
                    PK[0]: int(df[PK[0]].values[j]),
                    PK[1]: str(df[PK[1]].values[j])}
            if type(column1) == np.ndarray:
                dict_value = self.conv_type_for_json(column1[j], False, False)
            else:
                dict_value = self.conv_type_for_json(column1, False, False)
        c = {**dict_, **dict_PK, **dict_value}
        self.data[f'{type_error}'].append(c)

    def print_name_table_row_pk_sql(self, df, i, name_table, column1, one_table, PK, type_error, rows):
        if not one_table:
            dict_ = {'name_table': name_table,
                     'name_column': df.columns[i]}
            dict_PK = {}
            dict_value = {}

            print(f'name column = {df.columns[i]}')
            # TODO: изменить!
            if type(PK) == str:
                print(f'PK {PK} = {column1.values[rows][0]}')
                dict_PK = {'PK': int(column1.values[rows][0])}
            else:
                print(f'PK {PK[0]} = {column1.values[rows][0]}')
                print(f'PK2 {PK[1]} = {column1.values[rows][1]}')
                dict_PK = {
                    PK[0]: int(column1.values[rows][0]),
                    PK[1]: int(column1.values[rows][1])}
            values = [column1.values[rows][i], column1.values[rows + column1.shape[0] // 2][i]]
            dict_value = self.conv_type_for_json(values, True, False)
        else:
            for col in column1:
                print(1)
                dict_ = {'name_table': name_table,
                         'name_column': df.columns[i]}
                dict_PK = {}
                dict_value = {}

                print(f'name column = {df.columns[i]}')
            if type(PK) == str:
                # print(f'PK {PK} = {df[PK].values[j]}')
                print(f'PK {PK} = {col[0]}')
                # dict_PK = {'PK': int(df[PK].values[j])}
                dict_PK = {'PK': int(col[0])}
                # dict_value = col[1]
                dict_value = self.conv_type_for_json(col[1], False, False)
            else:
                print(f'PK {PK[0]} = {col[0]}')
                print(f'PK2 {PK[1]} = {col[1]}')
                dict_PK = {
                    PK[0]: int(col[0]),
                    PK[1]: str(col[1])}
                dict_value = self.conv_type_for_json(col[2], False, False)
            # if type(column1) == np.ndarray:
            #     dict_value = self.conv_type_for_json(column1[j], False, False)
            # else:
            #     dict_value = self.conv_type_for_json(column1, False, False)
        c = {**dict_, **dict_PK, **dict_value}
        self.data[f'{type_error}'].append(c)

    def check_target(self):
        if type(self.pk) == list:
            sql = f'''
                        SELECT
                          {self.name_table}.{self.pk[0]},
                          {self.name_table}.{self.pk[1]},
                          {self.name_table}.target_qty,
                          {self.name_table}.remain_qty,
                          {self.name_table}.act_reg_qty
                        FROM
                          {self.name_table}
                        WHERE
                          ROUND({self.name_table}.target_qty)!=ROUND(
                          {self.name_table}.remain_qty+{self.name_table}.act_reg_qty)
                        '''

        else:
            sql = f'''
                        SELECT
                          {self.name_table}.{self.pk},
                          {self.name_table}.target_qty,
                          {self.name_table}.remain_qty,
                          {self.name_table}.act_reg_qty
                        FROM
                          {self.name_table}
                        WHERE
                          ROUND({self.name_table}.target_qty)!=ROUND(
                          {self.name_table}.remain_qty+{self.name_table}.act_reg_qty)
                                                  '''

        with SessionLocal() as db:
            objects = db.execute(sql).fetchall()
        # if len(objects) > 0:
        if objects:
            print(self.name_table)
            print(self.pk)
            k = 1
            for row in range(len(objects)):
                if type(self.pk) == list:
                    print(f'{self.pk[0]} = {objects[row][0]}')
                    print(f'{self.pk[1]} = {objects[row][1]}')
                    dict_ = self.conv_type_for_json(column1=[objects[row][0], objects[row][1]], two_pk=True,
                                                    pk=True)

                    # if self.pk[1] == 'dt' or self.pk[0] == 'dt':
                    #     dict_ = {'name_table': self.name_table,
                    #              f'PK {self.pk[0]}': str(objects[row][0]),
                    #              f'PK_2 {self.pk[1]}': str(objects[row][1]),
                    #              }
                    # else:
                    # dict_ = {'name_table': self.name_table,
                    #          f'PK {self.pk[0]}': objects[row][0],
                    #          f'PK_2 {self.pk[1]}': objects[row][1],
                    #          }
                    k = 2
                else:
                    print(f'{self.pk} = {objects[row][0]}')
                    dict_ = {'name_table': self.name_table,
                             f'PK {self.pk}': objects[row][0]}
                dict_val = {
                    'target_qty': objects[row][k],
                    'remain_qty': objects[row][k + 1],
                    'act_reg_qty': objects[row][k + 2]
                }
                print(f'target_qty = {objects[row][k]}')
                print(f'remain_qty = {objects[row][k + 1]}')
                print(f'act_reg_qty = {objects[row][k + 2]}')
                c = {**dict_, **dict_val}
                self.data['target value not equal (act+remain)'].append(c)

    # def analysis_two_tables(self):
    #     column1 = self.df_pmc.values
    #     if self.df_pmc.shape[0] >= 2:
    #         for j in range(0, self.df_pmc.shape[0] - 1, 2):
    #             for i in range(self.df_pmc.shape[1]):
    #                 if self.df_pmc.columns[i] != 'update_date':
    #                     # if column1[j][i] != column1[j][i+1]:
    #                     if column1[j][i] != column1[j + 1][i]:
    #                         if type(column1[j][i]) != pd._libs.tslibs.nattype.NaTType and \
    #                                 type(column1[j + 1][i]) != pd._libs.tslibs.nattype.NaTType:
    #                             if type(column1[j][i]) == pd._libs.tslibs.timestamps.Timestamp:
    #                                 self.print_name_table_row_pk(self.df_pmc, i, self.name_table, column1, j, False,
    #                                                              self.pk, 'Mismatch of values in two tables')
    #                             elif type(column1[j][i]) == str:
    #                                 self.print_name_table_row_pk(self.df_pmc, i, self.name_table, column1, j, False,
    #                                                              self.pk,
    #                                                              'Mismatch of values in two tables')
    #                             elif type(column1[j][i]) == int:
    #                                 if not math.isnan(column1[j][i]) and not math.isnan(column1[j + 1][i]):
    #                                     if column1[j][i] > column1[j + 1][i]:
    #                                         self.print_name_table_row_pk(self.df_pmc, i, self.name_table, column1, j,
    #                                                                      False,
    #                                                                      self.pk,
    #                                                                      'Mismatch of values in two tables')

    def analysis_two_tables_sql(self):
        sql = f'''
        select * from {self.name_table}_pmc
        '''
        with SessionLocal() as db:
            pmc_table = db.execute(sql).fetchall()
            # exec_column = self.df.columns.get_indexer(['update_date'])[0]
            p = pd.DataFrame(pmc_table)
            if p.shape[0] == 0:
                pass
            else:
                column1 = self.df.loc[:, self.df.columns != 'update_date']
                pmc_column1 = p.loc[:, p.columns != 'update_date']
                if pmc_column1.shape[0] != column1.shape[0]:
                    pass
                else:
                    # TODO: решить проблему с разным кол-вом строк в двух таблицах
                    difference = np.where(column1.sort_index().sort_index(axis=1) != pmc_column1.sort_index().sort_index(axis=1))
                    ne_stacked = (column1 != pmc_column1).stack()
                    changed = ne_stacked[ne_stacked]
                    changed_from = column1.values[difference]
                    changed_to = pmc_column1.values[difference]
                    dif_columns = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)
                    # dif_columns.isnull()
                    # if dif_columns.isnull().any().any():
                    #     pass
                    # else:
                    y = [cl1 for cl1, cl2 in dif_columns.values]
                    y2 = [cl2 for cl1, cl2 in dif_columns.values]
                    two_colmns = pd.concat([column1, pmc_column1])
                    for i, y_ in enumerate(y):
                        rows = changed.index[i][0]
                        name_column = changed.index[i][1]
                        id_column = self.df.columns.get_indexer([name_column])[0]
                        if type(y_) == pd._libs.tslibs.timestamps.Timestamp:
                            # def print_name_table_row_pk_sql(self, pmc_column1, i, name_table, column1, one_table, PK, type_error):
                            self.print_name_table_row_pk_sql(pmc_column1, id_column, self.name_table, two_colmns, False,
                                                             self.pk, 'Mismatch of values in two tables', rows)
                        elif type(y_) == str:
                            # self.print_name_table_row_pk(self.df, i, self.name_table, column1, j, False,
                            #                              self.pk,
                            #                              'Mismatch of values in two tables')
                            self.print_name_table_row_pk_sql(pmc_column1, id_column, self.name_table, two_colmns, False,
                                                             self.pk, 'Mismatch of values in two tables', rows)
                        elif type(y_) == int or type(y_) == float:
                            # if not math.isnan(column1[j][i]) and not math.isnan(column1[j + 1][i]):
                            #     if y > y2:
                            self.print_name_table_row_pk_sql(pmc_column1, id_column, self.name_table, two_colmns,
                                                             False,
                                                             self.pk, 'Mismatch of values in two tables', rows)
                        # self.print_name_table_row_pk(self.df_pmc, i, self.name_table, column1, j,
                        #                              False,
                        #                              self.pk,
                        #                              'Mismatch of values in two tables')


    # @dispatch(object, str, str)
    def analysis_data_df(self):
        start_date_column = []
        begin_table = 1
        dtypes = self.df.dtypes
        for column_index in range(self.df.shape[1]):
            id_ = re.findall(r'(\w{2}_)', self.df.columns[column_index])
            id = re.findall(r'(\w{2})', self.df.columns[column_index])
            word_id = re.findall(r'(_\w{2})', self.df.columns[column_index])
            if id_:
                if id_[0] == 'id_':
                    continue
            if id:
                if id[0] == 'id':
                    continue
            if word_id:
                if word_id[len(word_id) - 1] == '_id':
                    continue
            if dtypes[column_index] == object or dtypes[column_index] == bool:
                continue
            # print(df.columns[column_index])
            column1 = self.df[self.df.columns[column_index]].values
            type_columns_ = [type(column1[i]) for i in range(len(column1)) if column1[i] != '']
            if type_columns_:

                type_columns_ = [type(column1[i]) for i in range(len(column1)) if
                                 type(column1[i]) != pd._libs.tslibs.nattype.NaTType or np.isnat(column1[i])]
                type_columns = [type(column1[i]) for i in range(len(column1))]
                max_type, dict_type_column = self.find_max_type(type_columns_)
                # error_type = find_type_error(max_type, type_columns, df, begin_table,
                #                              column_index, name_table)
                if max_type == int or max_type == float or max_type == np.float64 or max_type == np.float32 \
                        or max_type == np.int64 or max_type == np.int32:

                    error_sign = self.sign_warning(column_index, begin_table, column1, type_columns)

                    std_ = np.std(self.func_all_int_float_array(column1, type_columns))
                    if std_ > 100:
                        try:
                            if list(self.df.columns).index('remain_qty') != column_index and \
                                    list(self.df.columns).index('act_reg_qty') != column_index:
                                self.big_small_value_warning(column_index, column1, type_columns, error_sign)
                        except:
                            pass

                if max_type == pd._libs.tslibs.timestamps.Timestamp or max_type == np.datetime64:
                    self.check_date([pd.to_datetime(column1[i]).date() for i in range(len(column1))], column_index)
                    start_ = re.findall(r'(StartDate)', self.df.columns[column_index])
                    finish_ = re.findall(r'(FinishDate)', self.df.columns[column_index])
                    if start_:
                        start_date_column = column1
                    if finish_:
                        finish_date_column = column1
                        if start_date_column.all() > finish_date_column.all():
                            error_date_interval = [i for i, value in enumerate(start_date_column)
                                                   if value > finish_date_column[i]]
                            for i in error_date_interval:
                                self.print_name_table_row_pk(self.df, column_index, self.name_table,
                                                             self.df.values[i],
                                                             i, column_index, 'Error span year')
                                logger.warning(
                                    f'warning check span year in cell : column = {column_index} row = {i}')

    def analysis_data_df_sql_query(self):
        # sql_type = f'''SELECT  DATA_TYPE   FROM INFORMATION_SCHEMA.COLUMNS
        #                WHERE  table_name = '{self.name_table}' AND COLUMN_NAME != '{self.pk}';
        #                '''
        if type(self.pk) == str:
            sql_types = f'''
            SELECT  COLUMN_NAME, DATA_TYPE   FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{self.name_table}' AND COLUMN_NAME != '{self.pk}';
            '''
        else:
            sql_types = f'''
                        SELECT  COLUMN_NAME, DATA_TYPE   FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_NAME = '{self.name_table}' AND COLUMN_NAME != '{self.pk[0]}'
                                AND COLUMN_NAME != '{self.pk[1]}';
                        '''
        with SessionLocal() as db:
            name_types = db.execute(sql_types).fetchall()

            for ind, n_type in enumerate(name_types):
                id_ = re.findall(r'(\w{2}_)', n_type[0])
                id = re.findall(r'(\w{2})', n_type[0])
                word_id = re.findall(r'(_\w{2})', n_type[0])
                word_id_word = re.findall(r'(_\w{2}_)', n_type[0])
                if id_:
                    if id_[0] == 'id_':
                        continue
                if id:
                    if id[0] == 'id':
                        continue
                if word_id:
                    if word_id[len(word_id) - 1] == '_id':
                        continue
                if word_id_word:
                    if word_id_word[len(word_id_word) - 1] == '_id_':
                        continue
                if n_type[1] == object or n_type[1] == bool:
                    continue
                # print(1)
                if n_type[1] == 'integer' or n_type[1] == 'double precision':  # or _type[0]==''
                    column1 = self.df[n_type[0]].values
                    if self.df[n_type[0]].values.all() != None:
                        column_ind = int(self.df.columns.get_indexer([f'{n_type[0]}']))
                        error_sign = self.sign_warning(column_ind, 1, column1, n_type[1])

                        std_ = np.std(self.func_all_int_float_array(column1, n_type[1]))
                        if std_ > 100:
                            try:
                                if 'remain_qty' != n_type[0] and 'act_reg_qty' != n_type[0]:
                                    self.big_small_value_warning_sql(column_ind, column1, n_type[1], error_sign, n_type[0])
                            except:
                                pass
                if n_type[1] == pd._libs.tslibs.timestamps.Timestamp \
                        or n_type[1] == np.datetime64 \
                        or n_type[1] == 'timestamp without time zone':
                    column1 = self.df[n_type[0]].values
                    column_ind = int(self.df.columns.get_indexer([f'{n_type[0]}']))
                    self.check_date_sql(column_ind)
                    start_ = re.findall(r'(StartDate)', self.df.columns[column_ind])
                    finish_ = re.findall(r'(FinishDate)', self.df.columns[column_ind])
                    if start_:
                        start_date_column = column1
                    if finish_:
                        finish_date_column = column1
                        if start_date_column.all() > finish_date_column.all():
                            error_date_interval = [i for i, value in enumerate(start_date_column)
                                                   if value > finish_date_column[i]]
                            for i in error_date_interval:
                                self.print_name_table_row_pk(self.df, column_ind, self.name_table,
                                                             self.df.values[i],
                                                             i, column_ind, 'Error span year')
                                logger.warning(
                                    f'warning check span year in cell : column = {column_ind} row = {i}')


class Project(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.progress_bar([self.analysis_data_df,
        #                    self.analysis_two_tables,
        #                    self.write_to_dict])
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class ISR(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class Activity(TypeErrors):
    def validate(self):
        self.data = {
            'Very big value': [],
            'Very small value': [],
            'Wrong sign': [],
            'Small data': [],
            'Big data': [],
            'Error span year': [],
            'Mismatch of values in two tables': [],
            'another errors': []
        }
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
        self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        data = self.check_dictionary_activity_code_and_activity()
        if data:
            self.data['another errors'].append('Warning (No codes are assigned to any table!)')
        self.write_to_dict()

    @staticmethod
    def check_dictionary_activity_code_and_activity():
        sql = '''
                SELECT
                  activity.id_activity,
                  activity.activity_code,
                  activity.activity_name,
                  dictionary_activity_code."Dictionary_Name"
                FROM
                  public.activity activity
                  INNER JOIN public.dictionary_activity_code dictionary_activity_code ON dictionary_activity_code.code = activity.activity_code
                WHERE
                  dictionary_activity_code."Dictionary_Name" IN ('Виды работ', 'Конструктив для отчета');
                '''

        with SessionLocal() as db:
            objects = db.execute(sql).fetchall()

        if len(objects) == 0:
            logger.warning("Ни на одну работу не назначены коды!")
            return 1
        else:
            return 0


class Resource(TypeErrors):
    def validate(self):
        # list_valid = [self.analysis_data_df,
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class Resassignment(TypeErrors):
    def validate(self):
        self.data = {
            'Very big value': [],
            'Very small value': [],
            'Wrong sign': [],
            'Small data': [],
            'Big data': [],
            'Error span year': [],
            'Mismatch of values in two tables': [],
            'Dublicate rows in resassagment': [],
            'target value not equal (act+remain)': []
        }
        list_valid = [#self.analysis_data_df_sql_query,
        #               self.analysis_two_tables_sql,
                      self.analysis_resassagnment,
                      self.check_target,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()

        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.analysis_resassagnment()
        # self.check_target()
        # self.write_to_dict()

    def analysis_resassagnment(self):
        if True:
            df1 = self.df[['id_resource', 'id_project', 'id_wbs', 'id_activity']]
            rm_dublicates_df = df1.drop_duplicates()
            if rm_dublicates_df.shape != df1.shape:
                print('Find_ diblicates')

                df_find_dubl = df1.drop(rm_dublicates_df.index)
                rm = df_find_dubl.drop_duplicates()
                dubl = rm[['id_project', 'id_resource', 'id_wbs', 'id_activity']].values
                # dubl = df_find_dubl[['id_project', 'id_resource', 'id_wbs', 'id_activity']].values
                for i_dubl in dubl:
                    l = list(df1.loc[(self.df[['id_project', 'id_resource', 'id_wbs', 'id_activity']] == i_dubl)
                             .all(axis=1)].index)

                    ind_list = [self.df['id_resassignment'][i_ind] for i_ind in l]
                    #
                    # print("ind_list = ", ind_list)
                    # print("l", l)
                    # print("len(ind_list)-1  = ", len(ind_list) - 1)
                    for i in range(0, len(ind_list), 1):
                        # print(l[i])
                        # print(i)
                        self.print_name_table_row_pk(self.df, 0, 'resassignment', [], l[i],
                                                     True, 'id_resassignment', 'Dublicate rows in resassagment')
                        # logger.warning(f'Dublicate rows id = {ind_list[i]} and id = {ind_list[i + 1]}')


class UDFCodeProject(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class UDFCodeActivity(TypeErrors):
    # TODO: русский язык в log
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class UDFCodeResource(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class UDFCodeResassignment(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class DictionaryActivityCode(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class DictionaryProjectCode(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class DictionaryResourceCode(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class ActvRel(TypeErrors):
    def validate(self):
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.write_to_dict()


class ResassignmentSpred(TypeErrors):
    def validate(self):
        self.data = {
            'Very big value': [],
            'Very small value': [],
            'Wrong sign': [],
            'Small data': [],
            'Big data': [],
            'Error span year': [],
            'Mismatch of values in two tables': [],
            'target value not equal (act+remain)': []
        }
        # list_valid = [self.analysis_data_df,
        list_valid = [self.analysis_data_df_sql_query,
                      self.analysis_two_tables_sql,
                      self.check_target,
                      self.write_to_dict]
        for i in tqdm(list_valid):
            i()
        # self.analysis_data_df()
        # self.analysis_two_tables()
        # self.check_target()
        # self.write_to_dict()
