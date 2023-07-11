# Databricks notebook source
# MAGIC %md
# MAGIC #### Mount Azure Data Lake containers for project
# MAGIC

# COMMAND ----------

def mount_adls(storage_account_name, container_name):

    #Get the secrets from the key_vault
    client_id=dbutils.secrets.get("formula1-scope", "formula1-app-client-id")
    tenant_id=dbutils.secrets.get("formula1-scope", "formula1-app-tenant-id")
    client_secret =dbutils.secrets.get("formula1-scope", "formula1-app-client-secret")

    #set the spark configurations
    configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": client_id,
          "fs.azure.account.oauth2.client.secret": client_secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}
    
    if any(mount.mountPoint == f"/mnt/{storage_account_name}/{container_name}" for mount in dbutils.fs.mounts()):
        dbutils.fs.unmount(f"/mnt/{storage_account_name}/{container_name}")

    #mount the storage account container
    dbutils.fs.mount(
        source = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/",
        mount_point = f"/mnt/{storage_account_name}/{container_name}",
        extra_configs = configs)
    
    display(dbutils.fs.mounts())


# COMMAND ----------

mount_adls("formula1dl360","raw")

# COMMAND ----------

