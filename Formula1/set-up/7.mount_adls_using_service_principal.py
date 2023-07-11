# Databricks notebook source
# MAGIC %md
# MAGIC #### Mount Azure Data Lake using Service Principal
# MAGIC 1. Get client_id, tenant_id, client_secret from key vault
# MAGIC 1. Set Spark config with App/Client Id, Directory/Tenent Id & secrets
# MAGIC 1. Call file system utility mount to mount the storage
# MAGIC 1. Explore other file system utilities related to mount(List all mounts, unmount)

# COMMAND ----------

client_id=dbutils.secrets.get("formula1-scope", "formula1-app-client-id")
tenant_id=dbutils.secrets.get("formula1-scope", "formula1-app-tenant-id")
client_secret =dbutils.secrets.get("formula1-scope", "formula1-app-client-secret")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": client_id,
          "fs.azure.account.oauth2.client.secret": client_secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}


# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://demo@formula1dl360.dfs.core.windows.net/",
  mount_point = "/mnt/formula1dl360/demo",
  extra_configs = configs)

# COMMAND ----------

display(dbutils.fs.ls("/mnt/formula1dl360/demo"))

# COMMAND ----------

display(spark.read.csv("/mnt/formula1dl360/demo/circuits.csv"))

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

