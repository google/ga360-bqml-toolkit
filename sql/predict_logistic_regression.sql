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
  UNNEST(predicted_label_probs) AS pred
WHERE
  pred.label = 1