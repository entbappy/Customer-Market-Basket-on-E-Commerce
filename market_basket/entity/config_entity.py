from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["dataset_download_url",
                                                   "raw_data_dir",
                                                   "ingested_dir"])


DataValidationConfig = namedtuple("DataValidationConfig", ["clean_data_dir",
                                                         "customer_csv_file",
                                                         "product_class_csv_file",
                                                         "product_csv_file",
                                                         "region_csv_file",
                                                         "sales_csv_file",
                                                         "store_csv_file",
                                                         "time_by_day_csv_file",
                                                         "serialized_objects_dir"])  

DataTransformationConfig = namedtuple("DataTransformationConfig", ["clean_data_file_path",
                                                                   "transformed_data_dir"])     



ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["transformed_data_file_dir",
                                                      "trained_model_dir",
                                                      "trained_model_name"])  


ModelRecommendationConfig = namedtuple("ModelRecommendationConfig", ["list_of_products_serialized_objects",
                                                      "trained_model_path"])
