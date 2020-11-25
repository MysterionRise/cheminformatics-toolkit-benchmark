import time

import psycopg2
from rdkit import Chem
from rdkit import rdBase


def read_data():
    suppl = Chem.SDMolSupplier('../data/pubchem/Compound_000000001_000500000.sdf')
    data = [(Chem.MolToSmiles(x), x.GetProp('PUBCHEM_COMPOUND_CID')) for x in suppl if x is not None]
    return data


if __name__ == '__main__':
    print("{} rdkit={}".format(time.asctime(), rdBase.rdkitVersion))

    start_time = time.time()

    data = read_data()

    print("--- {} seconds for reading data ---".format(time.time() - start_time))

    conn = psycopg2.connect(host='localhost', database='rdkit_demo', user='admin', password='admin')

    curs = conn.cursor()
    curs.execute('create extension if not exists rdkit')
    curs.execute('drop table if exists raw_data')
    curs.execute('create table raw_data (smiles text,pubchem_id text)')
    curs.executemany('insert into raw_data values (%s,%s)', data)
    conn.commit()

    curs.execute('drop table if exists mols')
    curs.execute('select pubchem_id,mol_from_smiles(smiles::cstring) as m into mols from raw_data')
    conn.commit()

    curs.execute('create index molidx on mols using gist(m)')
    curs.execute('alter table mols add primary key (pubchem_id)')

    curs.execute('drop table if exists fps')
    curs.execute('select pubchem_id,morganbv_fp(m) as mfp2 into fps from mols')
    curs.execute('create index fps_mfp2_idx on fps using gist(mfp2)')
    curs.execute('alter table fps add primary key (pubchem_id)')
    conn.commit()

    print("--- {} seconds for puting data into PostgreSQL---".format(time.time() - start_time))

    curs.execute(
        "select count(*) from fps where mfp2%morganbv_fp('Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1')")
    print(curs.fetchone())

    print("--- {} seconds ---".format(time.time() - start_time))
