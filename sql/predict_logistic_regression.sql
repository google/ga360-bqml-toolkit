SELECT
  clientId,
  pred.prob as user_score
FROM
  ML.PREDICT(MODEL `{model_name}`,
    (
    SELECT
      *
    FROM
      `{daily_users_table}`) ) z,
  UNNEST(predicted_<label column>_probs) AS pred
WHERE
  pred.label = 1