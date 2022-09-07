import os
import sys
import pickle
import pandas as pd
from market_basket.logger.log import logging
from market_basket.exception.exception_handler import AppException
from market_basket.config.configuration import AppConfiguration



class DataTransformation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    

    # Converted the units into 1 encoded value
    @staticmethod
    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1  

    

    def get_data_transformer(self):
        try:
            product_name = pd.read_csv(self.data_transformation_config.clean_data_file_path)
            # Counting each product The number of transactions a product appeared in
            productCountDf = product_name.groupby("product_id",as_index = False)['transaction_id'].count()
            # Arranging Top Products
            productCountDf = productCountDf.sort_values("transaction_id",ascending = False)
            # Top 100 most frequently purchased products
            topProdFrame = productCountDf.iloc[0:100,:]
            productId= topProdFrame.loc[:,["product_id"]]
            # Orders containting the the most frequently purchased products
            MarketBasketdf = product_name[0:0]
            for i in range(0,99):
                pId = productId.iloc[i]['product_id'] 
                stDf = product_name[product_name.product_id == pId ]
                MarketBasketdf = MarketBasketdf.append(stDf,ignore_index = False)
            
            # Putting the items into 1 transaction
            basket = MarketBasketdf.groupby(['transaction_id','product_name'])['unit_sales'].sum().unstack().reset_index().fillna(0).set_index('transaction_id')
            basket_sets = basket.applymap(DataTransformation.encode_units)
            dummy=basket_sets.head(10000)
            logging.info(f" Final basket Shape : {dummy.shape}")
            logging.info(f" Final basket size : {dummy.size}")

            #saving basket table data
            os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
            pickle.dump(dummy,open(os.path.join(self.data_transformation_config.transformed_data_dir,"transformed_data.pkl"),'wb'))
            logging.info(f"Saved basket table data to {self.data_transformation_config.transformed_data_dir}")

        except Exception as e:
            raise AppException(e, sys) from e


    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20} ")
            self.get_data_transformer()
            logging.info(f"{'='*20}Data Transformation log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
