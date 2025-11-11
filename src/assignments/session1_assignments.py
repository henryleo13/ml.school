import mlflow

# Write a short Python script that logs an experiment to a local MLflow server. 
# Create an experiment, start a run, log at least two parameters and one small artifact. 
# Open the MLflow UI and verify that everything was logged correctly.

# #mlflow.set_tracking_uri("http://localhost:5000")
# mlflow.set_experiment("my_experiment")
# with mlflow.start_run():
#     mlflow.log_param("param1", 5)
#     mlflow.log_param("param2", "test")
#     mlflow.log_artifact("src/assignments/artifact1.txt")

# Start the MLflow server with a SQLite backend store and a filesystem artifact root. 
# Run a Python script that logs an experiment, and confirm the database and artifacts were written to disk.

# To start the MLflow server, use the following command in your terminal:
# mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./
# Then run this script to log the experiment.
mlflow.set_experiment("my_experiment_sqlite")
with mlflow.start_run():
    mlflow.log_param("param_sqlite1", 10)
    mlflow.log_param("param_sqlite2", "sqlite_test")
    mlflow.log_artifact("src/assignments/artifact1.txt")
