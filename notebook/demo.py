import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full")

with app.setup:
    import pathlib
    from pathlib import Path
    import os, sys, pathlib, importlib.util

    # JAVA_HOME = "./source/jdk-17.0.10+7"
    # os.environ["JAVA_HOME"] = JAVA_HOME
    # os.environ["PATH"] = f"{JAVA_HOME}/bin:" + os.environ.get("PATH", "")

    spec = importlib.util.find_spec("pyspark")
    pyspark_home = str(pathlib.Path(spec.origin).parent) 
    os.environ["SPARK_HOME"] = pyspark_home

    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    tmp = os.path.expanduser("~/tmp/pyspark")
    os.makedirs(tmp, exist_ok=True)
    os.environ["TMPDIR"] = tmp
    os.environ["SPARK_LOCAL_DIRS"] = tmp
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
    os.environ["PYSPARK_VERBOSE"] = "1"

    from pyspark.sql import SparkSession, Row, functions as F, types as T
    from pyspark.sql.functions import pandas_udf
    from pyspark.sql import functions as F, Window

    import marimo as mo
    import spark_oedo.bin as decode 


@app.cell
def _():
    _basedir = './rawdata/'
    _input = 'run001077.dat'
    _output = 'run001077.parquet'

    _input_info = [
        "streamingv1_to_parquet.py",
        _basedir + _input,
        _basedir + _output,
        "--max-blocks",
        "10000",
        "--verbose"
    ]

    sys.argv =_input_info

    decode.streamingv1_to_parquet.main()
    return


@app.cell
def _():
    spark = SparkSession.builder.master("local[*]") \
            .config("spark.driver.memory","20g") \
            .config("spark.executor.memory","20g") \
            .config("spark.sql.shuffle.partitions","32") \
            .config("spark.jars","/home/h487/opt/spark-oedo/scala_package/target/scala-2.13/spark-oedo-package_2.13-1.0.jar,/home/h487/opt/rapids/rapids-4-spark_2.13-25.10.0.jar") \
            .config("spark.rapids.sql.explain","NONE") \
            .config("spark.rapids.sql.concurrentGpuTasks","2") \
            .config("spark.rapids.memory.pinnedPool.size","2g") \
            .config("spark.sql.files.maxPartitionBytes","512m") \
            .config("spark.kryo.registrator","com.nvidia.spark.rapids.GpuKryoRegistrator") \
            .config("spark.plugins","com.nvidia.spark.SQLPlugin") \
            .config("spark.rapids.memory.gpu.allocFraction","0.3") \
            .config("spark.rapids.memory.gpu.minAllocFraction","0.01") \
            .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read.parquet('/Users/fendo/tmp/hh015/nestdaq-data/run001077.parquet')
    return (df,)


@app.cell
def _(df):
    df.printSchema()
    return


@app.cell
def _(df):
    df.show()
    return


if __name__ == "__main__":
    app.run()
