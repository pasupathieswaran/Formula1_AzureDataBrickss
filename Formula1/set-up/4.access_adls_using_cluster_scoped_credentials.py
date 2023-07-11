# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using Cluster Scoped Credentials
# MAGIC 1. Set the spark config fs.azure.account.key in cluster
# MAGIC 1. List the files from demo container
# MAGIC 1. Read data from circuits.csv file

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dl360.dfs.core.windows.net"))

# COMMAND ----------

display(spark.read.csv("abfss://demo@formula1dl360.dfs.core.windows.net/circuits.csv"))

# COMMAND ----------

