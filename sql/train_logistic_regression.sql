-- Train a logistic regression using BQML.
CREATE OR REPLACE MODEL {model_name}
OPTIONS(model_type='logistic_reg'
, INPUT_LABEL_COLS = ['{label_col}']
, L1_REG = 1
, DATA_SPLIT_METHOD = 'RANDOM'
, DATA_SPLIT_EVAL_FRACTION = 0.20
) AS
SELECT * EXCEPT(clientId)
FROM {training_set}