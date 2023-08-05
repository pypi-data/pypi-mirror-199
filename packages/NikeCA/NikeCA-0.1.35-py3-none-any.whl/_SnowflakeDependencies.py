

class SnowflakeDependencies:
    import pandas

    def snowflake_dependencies(self,
                               tables: str | list,
                               username: str,
                               warehouse: str,
                               role: str,
                               database: str | None = None,
                               schema: str | list | None = None,
                               save_path: str | None = None):

        """
        Searches the snowflake database and finds instances where the table is referenced and where the reference is not
        in the actual creation of the table itself

        :param save_path:
        :param tables: This is a list or string to check for in the database
        :param username: username for Snowflake
        :param warehouse: warehouse for Snowflake
        :param role: role for Snowflake
        :param database: database to search in must provide
        :param schema: filling this in can really help to speed up the query
        :return: pandas Dataframe
        """

        # snowflake connection packages:
        import pandas as pd
        import snowflake.connector
        import time
        import json
        import os

        if type(tables) == str:
            tables = [tables]

        print('opening snowflake connection...')

        cnn = snowflake.connector.connect(
            user=username,
            account='nike',
            authenticator='externalbrowser',
            role=role,
            warehouse=warehouse,
        )
        cs = cnn.cursor()
        process_complete = 0
        process_pass = 0
        counter = 0

        # fetch schema and table names
        query = 'SELECT * FROM ' + database + '.INFORMATION_SCHEMA.TABLES'
        if schema is not None:
            if type(schema) == str:
                schema = [schema]
            query = query + " WHERE TABLE_SCHEMA IN ('" + schema[0] + "'"
            if len(schema) > 1:
                for i in schema[1:]:
                    query = query + ", '" + i + "'"
            query = query + ')'

        cs.execute(query)
        df_tables = cs.fetch_pandas_all()

        query_ddl = {}

        for k, i in df_tables.iterrows():
            if i['TABLE_TYPE'] == 'VIEW':
                query_ddl[i['TABLE_CATALOG'] + '.' + i['TABLE_SCHEMA'] + '.' + i['TABLE_NAME']] = \
                    "SELECT GET_DDL('" + i['TABLE_TYPE'] + "', '" + i['TABLE_CATALOG'] + '.' + i[
                        'TABLE_SCHEMA'] + '.' \
                    + i['TABLE_NAME'] + "')"
            elif i['TABLE_TYPE'] == 'BASE TABLE':
                query_ddl[i['TABLE_CATALOG'] + '.' + i['TABLE_SCHEMA'] + '.' + i['TABLE_NAME']] = \
                    "SELECT GET_DDL('TABLE', '" + i['TABLE_CATALOG'] + '.' + i['TABLE_SCHEMA'] + '.' + \
                    i['TABLE_NAME'] + "')"

        df = pd.DataFrame([query_ddl]).T

        searchfor = ['NGP_DA_PROD.ODM_EMOPS.PG2NTABLE_EXT_SEC',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.KEY_ACCNTS_snpsht_2020_02_04',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.raju_temp_20200604',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.KEY_ACCNTS_snpsht_2020_06_15',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_BOOKING_NDDC_DF_cv',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.FRNCH_SILH_4SEASONS_Test',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_BOOKING_NDDC_EMEA_DF_cv',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_EMEA_temp1',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.test_pv',
                     'NGP_DA_PROD.POS_STG_T.ACCESS_HISTORY_TEST_0801_new',
                     'NGP_DA_PROD.POS_STG_T.Test_Table',
                     'NGP_DA_PROD.POS_STG_T.Test_Table',
                     '.INFORMATION_SCHEMA.',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC.PE_V5.2_JAN2020_2021MARCH23_APLA',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.KEY_ACCNTS_snpsht_2020_03_02',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.raju_temp_20200602_fw_corefocus',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_STG_T.test_STOCKOUT_FLGS',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_EMEA_temp',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.PYTHIA_PE_ETL_CV',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_CV',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.raju_temp_20200602_fw_corefocus',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_temp1',
                     'NGP_DA_PROD.POS_MKTPL_ANLYTC_T.MCB_STYLE_COLOR_DF_NDDC_temp2',
                     'NGP_DA_PROD.POS_STG_T.pos_rtlr_sc_trend_agg_0331']

        df = df[~df.index.str.contains('|'.join(searchfor), case=False)]

        df_index = df.index

        df_return = pd.DataFrame(index=df_index)
        df_return['sfqid'] = ''

        queries = len(df)
        print('Pulling ' + str(queries) + ' queries')

        query_list = []
        db_list = []
        complete = []

        for item in range(queries):
            query_list.append(item)
            db_list.append(item)
            complete.append(0)

        for k, v in df.iterrows():
            sql = v[0]
            cs.execute_async(sql)
            query_list[counter] = cs.sfqid
            df_return['sfqid'][k] = cs.sfqid
            counter += 1
        counter = 1
        if save_path is not None:
            if os.path.isfile(save_path):
                with open(save_path) as f:
                    d = json.load(f)
            else:
                d = {}
        else:
            d = {}
        while process_complete == 0:
            item = -1
            process_pass += 1
            if sum(complete) == queries or process_pass == 1000:
                process_complete = 1
            for result in query_list:
                item += 1
                if complete[item] == 0:
                    print('Running ' + df_return[df_return['sfqid'] == result].index[0])
                    status = cnn.get_query_status_throw_if_error(result)
                    print('the status for ' + df_return[df_return['sfqid'] == result].index[0] + ' is ' +
                          str(status) + ' ' + str(counter))
                    if str(status) == 'QueryStatus.SUCCESS':
                        complete[item] = 1
                        cs.get_results_from_sfqid(result)
                        data = cs.fetch_pandas_all()
                        for table in tables:
                            try:
                                if table.upper() + ' ' in data.iloc[0, 0][data.iloc[0, 0].upper().index(
                                        table.upper()):data.iloc[0, 0].upper().index(table.upper()) + len(table) + 1]\
                                        and table.upper() not in data.iloc[0,0][:data.iloc[0, 0].index('(')]:
                                    d[table] = {}
                                    d[table][df_return[df_return['sfqid'] == result].index[0]] = data.to_dict('index')
                            except ValueError:
                                continue
                    else:
                        time.sleep(.1)
                counter += 1
        cnn.close()

        if save_path is not None:
            with open(save_path, "w+") as f:
                json.dump(d, f, indent=4)

        print('process complete')

        return d
