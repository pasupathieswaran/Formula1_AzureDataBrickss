# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using Service Principal
# MAGIC 1. Register Azure AD application/ Service Principal
# MAGIC 1. Generate secret/password for application
# MAGIC 1. Set Spark config with App/Client Id, Directory/Tenent Id & secrets
# MAGIC 1. Assign role "Storage Blob Data Contributor" to the data lake

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

client_id=dbutils.secrets.get("formula1-scope", "formula1-app-client-id")
tenant_id=dbutils.secrets.get("formula1-scope", "formula1-app-tenant-id")
client_secret =dbutils.secrets.get("formula1-scope", "formula1-app-client-secret")

# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type.formula1dl360.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.formula1dl360.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.formula1dl360.dfs.core.windows.net", client_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.formula1dl360.dfs.core.windows.net", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.formula1dl360.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dl360.dfs.core.windows.net"))

# COMMAND ----------

display(spark.read.csv("abfss://demo@formula1dl360.dfs.core.windows.net/circuits.csv"))

# COMMAND ----------

