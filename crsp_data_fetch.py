from sqlite3 import connect
import wrds

DB_NAME = "bachelor.db"

def cik_mapping(db):
    ccm_lookup = db.get_table(library='crspa', table='ccm_lookup')
    with connect(DB_NAME) as conn:
        ccm_lookup.to_sql(name='ccm_lookup', con=conn, if_exists='replace')

def available_tables(db):
    libs = db.list_libraries()
    mapping = {}
    for lib in libs:
        mapping[lib] = db.list_tables(lib)

    import json
    with open('tables.json', 'w') as f_out:
        json.dump(mapping, f_out, indent=4)

def crsp_daily_data(db):
    dsf = db.raw_sql("""select * from crspa.dsf where date > '2008-01-01'""")
    with connect(DB_NAME) as conn:
        dsf.to_sql(name='crsp_daily_data', con=conn, if_exists='replace')



def test(db):

    # print(db.raw_sql('select count(*) from secsamp.wciklink_names'))
    # print(db.get_table(library='secsamp', table='wciklink_names', obs=10))
    # print(db.raw_sql('select count(*) from crspa.ccmxpf_lnkhist where lpermno is not null'))


    # print(db.raw_sql('select count(*) from crsp.crsp_cik_map'))
    # print(db.get_table(library='crsp', table='crsp_cik_map', obs=10))

    # print(db.get_table(library='crspq', table='crsp_cik_map', obs=10))
    # print(db.raw_sql('select count(*) from crspq.crsp_cik_map'))

    # ccm_lookup = db.get_table(library='crspa', table='ccm_lookup')

    # print(db.get_table(library='crspa', table='ccm_lookup'))
    # print(db.raw_sql('select count(*) from crspa.ccm_lookup where cik is not null and lpermno is not null'))

    print(db.get_table(library='crspa', table='dsf', obs=10))
    print(db.raw_sql("""select count(*) from crspa.dsf where date > '2008-01-01'"""))



def main():
    import sys
    if len(sys.argv) != 2:
        print("Specify function")
        return
    function = sys.argv[1]
    all_globals = globals()
    if function in all_globals and callable(all_globals[function]):
        db = wrds.Connection()
        all_globals[function](db)



if __name__ == '__main__':
    main()

    