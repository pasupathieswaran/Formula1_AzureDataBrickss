# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using Access Keys
# MAGIC 1. Set the spark config fs.azure.account.key
# MAGIC 1. List the files from demo container
# MAGIC 1. Read data from circuits.csv file

# COMMAND ----------

dbutils.secrets.list('formula1-scope')

# COMMAND ----------

formula1dl_account_key = dbutils.secrets.get('formula1-scope', 'formula1dl-account-key')

# COMMAND ----------

spark.conf.set("fs.azure.account.key.formula1dl360.dfs.core.windows.net",
               formula1dl_account_key)

# COMMAND ----------

dbutils.fs.ls("abfss://demo@formula1dl360.dfs.core.windows.net")

# COMMAND ----------

display(spark.read.csv("abfss://demo@formula1dl360.dfs.core.windows.net/circuits.csv"))

# COMMAND ----------

