import os
import joblib
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler, MinMaxScaler
from pyspark.ml import Pipeline
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        
        self.rating_df = None
        self.anime_df = None
        self.X_train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None
        
        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}
        
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info('Data processing initiated')

    def load_data(self, usecols):
        try:
            # Read the CSV file using PySpark
            spark = SparkSession.builder.appName("Data Processing").getOrCreate()
            self.rating_df = spark.read.csv(self.input_file, header=True, inferSchema=True).select(*usecols)
            logger.info('Data loaded successfully for Data processing')
        except Exception as e:
            raise CustomException('Failed to load data', sys)

    def filter_users(self, min_rating=400):
        try:
            # Filter users with at least 400 ratings
            user_counts = self.rating_df.groupby('user_id').count()
            valid_users = user_counts.filter(user_counts['count'] >= min_rating)
            self.rating_df = self.rating_df.join(valid_users, on="user_id", how="inner")
            logger.info('Filtered data successfully')
        except Exception as e:
            raise CustomException('Failed to Filter user data', sys)

    def scale_ratings(self):
        try:
            # Use MinMaxScaler from MLlib
            scaler = MinMaxScaler(inputCol="rating", outputCol="scaled_rating")
            self.rating_df = scaler.fit(self.rating_df).transform(self.rating_df)
            logger.info('Standardized the rating column successfully')
        except Exception as e:
            raise CustomException('Failed to standardize the ratings', sys)

    def encode_data(self):
        try:
            # Use StringIndexer to encode user and anime
            user_indexer = StringIndexer(inputCol="user_id", outputCol="user")
            anime_indexer = StringIndexer(inputCol="anime_id", outputCol="anime")
            
            self.rating_df = user_indexer.fit(self.rating_df).transform(self.rating_df)
            self.rating_df = anime_indexer.fit(self.rating_df).transform(self.rating_df)
            logger.info('Encoded user and anime data')

        except Exception as e:
            raise CustomException('Failed to encode data', sys)

    def split_data(self, test_size=0.2):
        try:
            # Randomly split the data into train and test sets
            train_data, test_data = self.rating_df.randomSplit([1 - test_size, test_size], seed=43)
            self.X_train_array = [train_data.select('user', 'anime').rdd.map(lambda row: row[0]).collect(), 
                                  train_data.select('anime').rdd.map(lambda row: row[0]).collect()]
            self.X_test_array = [test_data.select('user', 'anime').rdd.map(lambda row: row[0]).collect(), 
                                 test_data.select('anime').rdd.map(lambda row: row[0]).collect()]
            self.y_train = train_data.select('scaled_rating').rdd.map(lambda row: row[0]).collect()
            self.y_test = test_data.select('scaled_rating').rdd.map(lambda row: row[0]).collect()
            logger.info('Data split successfully')
        except Exception as e:
            raise CustomException('Failed to split data', sys)

    def save_artifacts(self):
        try:
            artifacts = {
                'user2user_encoded': self.user2user_encoded,
                'user2user_decoded': self.user2user_decoded,
                'anime2anime_encoded': self.anime2anime_encoded,
                'anime2anime_decoded': self.anime2anime_decoded,
            }

            for name, data in artifacts.items():
                joblib.dump(data, os.path.join(self.output_dir, f'{name}.pkl'))
                logger.info(f'{name} saved successfully')

            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)
            logger.info('All training and testing data saved')

        except Exception as e:
            raise CustomException('Failed to save artifacts', sys)

    def run(self):
        try:
            self.load_data(usecols=['user_id', 'anime_id', 'rating'])
            self.filter_users()
            self.scale_ratings()
            self.encode_data()
            self.split_data()
            self.save_artifacts()
            logger.info('Data Processing Pipeline Run Successfully')
        except CustomException as e:
            logger.error(str(e))


if __name__ == "__main__":
    data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()
