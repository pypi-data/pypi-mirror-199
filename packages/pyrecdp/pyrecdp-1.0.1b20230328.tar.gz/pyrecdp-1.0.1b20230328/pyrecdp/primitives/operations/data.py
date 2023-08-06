from .base import BaseOperation
import pandas as pd

class DataFrameOperation(BaseOperation):
    def __init__(self, op_base):
        super().__init__(op_base)
        self.support_spark_dataframe = False
        self.support_spark_rdd = True

    def set(self, dataset):
        if self.op.children is None or len(self.op.children) == 0:
            self.cache = dataset[self.op.config]
        
    def get_function_pd(self):
        def get_dataframe(df):
            return df
        return get_dataframe
    
class DataLoader(BaseOperation):
    def __init__(self, op_base):
        super().__init__(op_base)
        self.support_spark_dataframe = True
        self.support_spark_rdd = False
        
    def get_function_pd(self):
        def get_dataframe():
            file_path = self.op.config['file_path']
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.parquet'):
                return pd.read_parquet(file_path)
            else:
                raise NotImplementedError("now sample read only support csv and parquet")
        return get_dataframe
    
    def get_function_spark(self, rdp, method = None):
        def get_dataframe():
            file_path = self.op.config['file_path']
            if file_path.endswith('.csv'):
                return rdp.spark.read.csv(file_path, header=True, inferSchema=True)
            elif file_path.endswith('.parquet'):
                return rdp.spark.read.parquet(file_path)
            else:
                raise NotImplementedError("now sample read only support csv and parquet")
        return get_dataframe