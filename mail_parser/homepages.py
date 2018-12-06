
import turbodbc
import pandas as pd


def create_connection_string_turbo(server, database):
    options = turbodbc.make_options(prefer_unicode=True)
    constr = 'Driver={ODBC Driver 13 for SQL Server};Server=' + \
        server + ';Database=' + database + ';Trusted_Connection=yes;'
    con = turbodbc.connect(connection_string=constr, turbodbc_options=options)
    return con


def query():
    return """
        SELECT Kundennummer = [Nr.], Name, Homepage
        FROM BDL.DES.Debitor d
        WHERE Homepage > '' AND Name NOT LIKE '§%'
        AND EXISTS ( SELECT Kunde
                      FROM BDL.DES.[Kundenstamm CRHT] k
                      WHERE k.Kunde = d.[Nr.]
                    )
         """


def sql_to_dataframe(connection, query, *args, **kwargs):
    df = pd.read_sql(query, connection, *args, **kwargs)
    return df


def dataframe_to_dict(df):
    d = {i[1][0]: (i[1][1], i[1][2]) for i in df.iterrows()}
    return d


def clean_url(d):
    for i in d:
        url = d[i][1]
        if not url.startswith("http"):
            url = "http://" + url
            d[i] = (d[i][0], url)
    return d


def get_homepage_dict():
    con = create_connection_string_turbo(
        "CRHBUSADWH51", 'Operations')
    df = sql_to_dataframe(con, query())
    d = dataframe_to_dict(df)
    d = clean_url(d)
    return d


DICT_OF_HOMEPAGES = get_homepage_dict()
