# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest races.csv file

# COMMAND ----------

dbutils.widgets.text("p_data_source", "")
v_data_source = dbutils.widgets.get("p_data_source")

# COMMAND ----------

dbutils.widgets.text("p_file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("p_file_date")    

# COMMAND ----------

# MAGIC %run "../includes/configuration"

# COMMAND ----------

# MAGIC %run "../includes/common_functions"

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 1 - Read the CSV file using the spark Dataframe Reader API

# COMMAND ----------

from pyspark.sql.types import IntegerType, StructField, StructType, StringType, DateType

# COMMAND ----------

races_schema = StructType(fields= [StructField("raceId", IntegerType(), False),
                                   StructField("year", IntegerType(), True),
                                   StructField("round", IntegerType(), True),
                                   StructField("circuitId", IntegerType(), True),
                                   StructField("name", StringType(), True),
                                   StructField("date", DateType(), True),
                                   StructField("time", StringType(), True),
                                   StructField("url", StringType(), True),
                                   ])

# COMMAND ----------

races_df = spark.read \
    .option("header", True) \
    .schema(races_schema) \
    .csv(f"{raw_folder_path}/{v_file_date}/races.csv")

# COMMAND ----------

display(races_df)

# COMMAND ----------

from pyspark.sql.functions import col, concat, current_timestamp, to_timestamp, lit

# COMMAND ----------

races_with_timestamp_df = races_df.withColumn("race_timestamp", to_timestamp(concat(col("date"), lit(" "), col("time")),"yyyy-MM-dd HH:mm:ss")) \
    .withColumn("data_source", lit(v_data_source)) \
        .withColumn("file_date", lit(v_file_date))

# COMMAND ----------

races_with_ingestion_date_df = add_ingestion_date(races_with_timestamp_df)

# COMMAND ----------

races_selected_df = races_with_ingestion_date_df.select(col("raceId").alias("race_id"),col("year").alias("race_year"),col("round"),
                                                   col("ingestion_date"),col("race_timestamp"),col("name"), col("circuitId").alias("circuit_id"))

# COMMAND ----------

races_selected_df.write.mode("overwrite").partitionBy("race_year").format("delta").saveAsTable("f1_processed.races")

# COMMAND ----------

dbutils.notebook.exit("Success")