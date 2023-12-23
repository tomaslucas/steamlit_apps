import polars as pl
import polars.selectors as cs
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

penguin_df = pl.read_csv('penguins.csv').drop_nulls()

expr = (
    penguin_df
    .select(pl.col('species'))
    .with_columns(rank = pl.col('species').rank('dense')-1)
)

uniques = expr.unique().sort('rank').select('species').to_numpy()
output = expr.select('rank').to_series().to_numpy()

features = (penguin_df
            .select(pl.all().exclude(['species', 'year']))
            .to_dummies(cs.string())
            .select(
                ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g',
                 'island_Biscoe', 'island_Dream', 'island_Torgersen', 'sex_female',
                 'sex_male']
            )
           )

x_train, x_test, y_train, y_test = train_test_split(
    features.to_numpy(), output, test_size=.8, random_state=15)
rfc = RandomForestClassifier(random_state=15)
rfc.fit(x_train, y_train)
y_pred = rfc.predict(x_test)
score = accuracy_score(y_pred, y_test)
print(f'Our accuracy score for this model is {score}')
      
rf_pickle = open('random_forest_penguin.pickle', 'wb')
pickle.dump(rfc, rf_pickle)
rf_pickle.close()

output_pickle = open('output_penguin.pickle', 'wb')
pickle.dump(uniques, output_pickle)
output_pickle.close()