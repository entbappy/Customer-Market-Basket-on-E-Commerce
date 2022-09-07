from market_basket.components.stage_00_data_ingestion import DataIngestion
from market_basket.components.stage_01_data_validation import DataValidation


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
     

    def start_training_pipeline(self):
        """
        Starts the training pipeline
        :return: none
        """
        self.data_ingestion.initiate_data_ingestion()
        self.data_validation.initiate_data_validation()
