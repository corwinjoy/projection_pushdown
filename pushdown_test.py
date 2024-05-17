import pandas as pd
import numpy as np
import duckdb
from time import perf_counter

n = 100_000
columns = 10
pd_df = pd.DataFrame({f'col{i}': 1000 * np.random.sample(n) for i in range(columns)})
query = """
SELECT col0
FROM 
(
    SELECT 
    DISTINCT ON (floor(col0))
    {columns}
    FROM pd_df
    ORDER by col0 DESC
)
"""
results = dict()
for columns in ['col0', '*',]:
    start = perf_counter()
    results[columns] = duckdb.query(query.format(columns=columns)).df()
    print(f'The query using `{columns}` took {perf_counter() - start} s')
print(f"The results are equal: {results['*'].equals(results['col0'])}")