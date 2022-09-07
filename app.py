import os
import sys
import pickle
import streamlit as st
import requests
import numpy as np
from market_basket.logger.log import logging
from market_basket.exception.exception_handler import AppException
from market_basket.config.configuration import AppConfiguration
from market_basket.pipeline.training_pipeline import TrainingPipeline


class Recommendation:
    def __init__(self,app_config = AppConfiguration()):
        try:
            self.recommendation_config= app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    

    def recommendations_using_Fpgrowth(self,item):
        try:
            fpgrowth_rules = pickle.load(open(self.recommendation_config.trained_model_path,'rb'))
            recommend = []
            records = fpgrowth_rules.shape[0]
            for i in range(0,records):
                if item == fpgrowth_rules.iloc[i,0]:
                    recommend.append(fpgrowth_rules.iloc[i,1])
            
            return recommend
        
        except Exception as e:
            raise AppException(e, sys) from e


    def train_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.text("Training Completed!")
            logging.info(f"Trained successfully!")
        except Exception as e:
            raise AppException(e, sys) from e

    
    def recommendations_engine(self,item):
        try:
            recommended_products = self.recommendations_using_Fpgrowth(item)[0:5]
            print(recommended_products)
            if len(recommended_products) == 0:
                st.text("Nothing recommended_products")
            else:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.text(list(recommended_products[0])[0])

                with col2:
                    st.text(list(recommended_products[1])[0])

                with col3:
                    st.text(list(recommended_products[2])[0])
                with col4:
                    st.text(list(recommended_products[3])[0])
                with col5:
                    st.text(list(recommended_products[4])[0])

        except Exception as e:
            raise AppException(e, sys) from e


if __name__ == "__main__":
    obj = Recommendation()
    st.header('Customer Market Basket on E-Commerce')
    st.text("This is a E-Commerce Market Basket based on association rule learning.!")

    #Training
    if st.button('Train Market Basket'):
        obj.train_engine()

    list_of_products = pickle.load(open(os.path.join('templates','list_of_products.pkl') ,'rb'))
    selected_product = st.selectbox(
    "Type or select a product from the dropdown",
    list_of_products)
    print(selected_product)
    
    #recommendation
    if st.button('Show Basket'):
        obj.recommendations_engine({selected_product})
