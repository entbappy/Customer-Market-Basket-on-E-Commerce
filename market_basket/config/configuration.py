import os
import sys
from market_basket.logger.log import logging
from market_basket.utils.util import read_yaml_file
from market_basket.exception.exception_handler import AppException
from market_basket.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelRecommendationConfig
from market_basket.constant import *


class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_ingestion_config = self.configs_info['data_ingestion_config']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['raw_data_dir'])

            response = DataIngestionConfig(
                dataset_download_url = data_ingestion_config['dataset_download_url'],
                raw_data_dir = raw_data_dir,
                ingested_dir = ingested_data_dir
            )

            logging.info(f"Data Ingestion Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_config = self.configs_info['data_validation_config']
            data_ingestion_config = self.configs_info['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            customer_csv_file = data_validation_config['customer_csv_file']
            product_class_csv_file = data_validation_config['product_class_csv_file']
            product_csv_file = data_validation_config['product_csv_file']
            region_csv_file = data_validation_config['region_csv_file']
            sales_csv_file = data_validation_config['sales_csv_file']
            store_csv_file = data_validation_config['store_csv_file']
            time_by_day_csv_file = data_validation_config['time_by_day_csv_file']

            customer_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], customer_csv_file)
            product_class_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], product_class_csv_file)
            product_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], product_csv_file)
            region_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], region_csv_file)
            sales_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], sales_csv_file)
            store_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], store_csv_file)
            time_by_day_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], time_by_day_csv_file)
            clean_data_path = os.path.join(artifacts_dir, dataset_dir, data_validation_config['clean_data_dir'])
            serialized_objects_dir = os.path.join(artifacts_dir, data_validation_config['serialized_objects_dir'])

            response = DataValidationConfig(
                clean_data_dir = clean_data_path,
                customer_csv_file = customer_csv_file_dir,
                product_class_csv_file = product_class_csv_file_dir,
                product_csv_file = product_csv_file_dir,
                region_csv_file = region_csv_file_dir,
                sales_csv_file = sales_csv_file_dir,
                store_csv_file = store_csv_file_dir,
                time_by_day_csv_file = time_by_day_csv_file_dir,
                serialized_objects_dir = serialized_objects_dir
            )

            logging.info(f"Data Validation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    

    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            data_transformation_config = self.configs_info['data_transformation_config']
            data_validation_config = self.configs_info['data_validation_config']
            data_ingestion_config = self.configs_info['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
          
            clean_data_file_path = os.path.join(artifacts_dir, dataset_dir, data_validation_config['clean_data_dir'],'clean_data.csv')
            transformed_data_dir = os.path.join(artifacts_dir, dataset_dir, data_transformation_config['transformed_data_dir'])

            response = DataTransformationConfig(
                clean_data_file_path = clean_data_file_path,
                transformed_data_dir = transformed_data_dir
            )

            logging.info(f"Data Transformation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            model_trainer_config = self.configs_info['model_trainer_config']
            data_transformation_config = self.configs_info['data_transformation_config']
            data_ingestion_config = self.configs_info['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']

          
           
            transformed_data_file_dir = os.path.join(artifacts_dir, dataset_dir, data_transformation_config['transformed_data_dir'], 'transformed_data.pkl')
            trained_model_dir = os.path.join(artifacts_dir, model_trainer_config['trained_model_dir'])
            trained_model_name = model_trainer_config['trained_model_name']

            response = ModelTrainerConfig(
                transformed_data_file_dir = transformed_data_file_dir,
                trained_model_dir = trained_model_dir,
                trained_model_name = trained_model_name
            )

            logging.info(f"Model Trainer Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e


    
    def get_recommendation_config(self) -> ModelRecommendationConfig:
        try:
            model_trainer_config = self.configs_info['model_trainer_config']
            data_validation_config = self.configs_info['data_validation_config']
            trained_model_name = model_trainer_config['trained_model_name']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            trained_model_dir = os.path.join(artifacts_dir, model_trainer_config['trained_model_dir'])
            

            list_of_products_serialized_objects = os.path.join(artifacts_dir, data_validation_config['serialized_objects_dir'], 'list_of_products.pkl')
            trained_model_path = os.path.join(trained_model_dir,trained_model_name)
          
            response = ModelRecommendationConfig(
                list_of_products_serialized_objects = list_of_products_serialized_objects,
                trained_model_path = trained_model_path
            )

            logging.info(f"Model Recommendation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e



