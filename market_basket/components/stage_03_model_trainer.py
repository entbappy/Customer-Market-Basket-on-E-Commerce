import os
import sys
import pickle
from market_basket.logger.log import logging
from market_basket.exception.exception_handler import AppException
from market_basket.config.configuration import AppConfiguration
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules


class ModelTrainer:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e

    
    def train(self):
        try:
            #loading basket data
            dummy = pickle.load(open(self.model_trainer_config.transformed_data_file_dir,'rb'))
            # Frequent Items with support 0.001% using Fpgrowth Algorithm
            freq_items=fpgrowth(dummy,min_support=.0001,use_colnames=True)
            # Association Rules using Fpgrowth Algorithm
            fpgrowth_rules=association_rules(freq_items,metric="lift",min_threshold=1)

            #Saving model object for recommendations
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            file_name = os.path.join(self.model_trainer_config.trained_model_dir,self.model_trainer_config.trained_model_name)
            pickle.dump(fpgrowth_rules,open(file_name,'wb'))
            logging.info(f"Saving final model to {file_name}")


            # Saving the training model metrics
            fpgrowth_rules.to_csv(os.path.join(self.model_trainer_config.trained_model_dir,'metrics.csv'), index = False)
            logging.info(f"Saving metrics to {self.model_trainer_config.trained_model_dir}")
            
        except Exception as e:
            raise AppException(e, sys) from e

    
    def initiate_model_trainer(self):
        try:
            logging.info(f"{'='*20}Model Trainer log started.{'='*20} ")
            self.train()
            logging.info(f"{'='*20}Model Trainer log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
