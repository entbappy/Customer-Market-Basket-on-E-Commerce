import os
import sys
import ast 
import pandas as pd
import numpy as np
import pickle
import networkx as nx
from market_basket.logger.log import logging
from market_basket.exception.exception_handler import AppException
from market_basket.config.configuration import AppConfiguration


class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    

    def preprocess_data(self):
        try:
            # loading all the data
            customer = pd.read_csv(self.data_validation_config.customer_csv_file)
            product = pd.read_csv(self.data_validation_config.product_csv_file)
            product_class = pd.read_csv(self.data_validation_config.product_class_csv_file)
            region = pd.read_csv(self.data_validation_config.region_csv_file)
            sales = pd.read_csv(self.data_validation_config.sales_csv_file)
            store = pd.read_csv(self.data_validation_config.store_csv_file)
            time_by_day = pd.read_csv(self.data_validation_config.time_by_day_csv_file)
            
            
            logging.info(f" Shape of customer data file: {customer.shape}")
            logging.info(f" Shape of product data file: {product.shape}")
            logging.info(f" Shape of product_class data file: {product_class.shape}")
            logging.info(f" Shape of region data file: {region.shape}")
            logging.info(f" Shape of sales data file: {sales.shape}")
            logging.info(f" Shape of store data file: {store.shape}")
            logging.info(f" Shape of time_by_day data file: {time_by_day.shape}")

            # Merging Customer Dataset in sales Dataframe
            df=sales.merge(customer,on='customer_id')
            # Merging Products Dataset in df Dataframe
            df=df.merge(product,on='product_id')
            # Merging Department Dataset in df Dataframe
            df=df.merge(product_class,on='product_class_id')
            # Merging Stores Dataset in df Dataframe
            df=df.merge(store,on='store_id')
            # Merging Region Dataset in df Dataframe
            df=df.merge(region,on='region_id')
            # Merging Time by Day Dataset in df Dataframe
            df=df.merge(time_by_day,on='time_id')
            logging.info(f" Shape of the after merging: {df.shape}")

            # Converting Dataframe to Final Foodmart Offline Dataset
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            df.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'Foodmart_dataset.csv'))

            # Loading Foodmart Offline Dataset
            df=pd.read_csv(os.path.join(self.data_validation_config.clean_data_dir,'Foodmart_dataset.csv'))
            logging.info(f" Shape of final: {df.shape}")

            # Top 10 First Choices in Products
            df['products'] = 'Products'
            products = df.truncate(before = 605, after = 615)
            products = nx.from_pandas_edgelist(products, source = 'products', target = 'product_name', edge_attr = True)

            # Top 10 First Choices in Department
            df['departments'] = 'Departments'
            departments = df.truncate(before = 150, after = 195)
            departments = nx.from_pandas_edgelist(departments, source = 'departments', target = 'department', edge_attr = True)
            logging.info(f" Shape : {df.shape}")

            # Drop Duplicates
            df.drop_duplicates()

            # Transaction ID - create transaction id which denotes a basket
            df['transaction_id'] = df['customer_id'].astype(str) + df['time_id'].astype(str)

            # Filtering the Columns
            cols = [77,3,1,24,7,2]
            product_name=df[df.columns[cols]]
            logging.info(f" Shape of the clean data after preprocessing: {product_name.shape}")

            list_of_products = np.array(product_name['product_name'])

            # Saving the cleaned data for transformation
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            product_name.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'clean_data.csv'), index = False)
            logging.info(f"Saved cleaned data to {self.data_validation_config.clean_data_dir}")

            #saving list_of_products objects for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(list_of_products, open(os.path.join(self.data_validation_config.serialized_objects_dir, "list_of_products.pkl"),'wb'))
            logging.info(f"Saved list_of_products serialization object to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    
    
    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.preprocess_data()
            logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e

    
