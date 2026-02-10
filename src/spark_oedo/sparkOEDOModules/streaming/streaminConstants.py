from pyspark.sql.functions import window, col
from pyspark.sql import DataFrame

WATERMARK_WINDOW = "10 seconds"
WATERMARK_TS_COL = "stream_uts"
