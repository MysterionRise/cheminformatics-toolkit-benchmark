import time
from pathlib import Path

from bingo_elastic.model.record import IndigoRecord
from bingo_elastic.queries import SimilarityMatch
from bingo_elastic.elastic import ElasticRepository
from bingo_elastic.model import helpers
from indigo import Indigo

if __name__ == '__main__':
    indigo = Indigo()
    start_time = time.time()

    repository = ElasticRepository(host="127.0.0.1", port=9200)
    # try:
    #     sdf = helpers.iterate_sdf("../data/pubchem/Compound_000000001_000500000.sdf")
    #     repository.index_records(sdf)
    # except ValueError as e:
    #     print(e)
    #
    #
    # time.sleep(300)

    print("--- {} seconds for reading and indexing data ---".format(time.time() - start_time))

    mol = indigo.loadMolecule("Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1")
    target = IndigoRecord(indigo_object=mol)

    alg = SimilarityMatch(target, 0.5)
    similar_records = repository.filter(similarity=alg, limit=20)
    print(similar_records
          )
    print("--- {} seconds ---".format(time.time() - start_time))
