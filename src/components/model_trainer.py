import os
import sys
from dataclasses import dataclass

from catboost import CatBoostClassifier
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTraier:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array, preprocessor_path):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "AdaBoost": AdaBoostRegressor(random_state=42),
                "Decision Tree": DecisionTreeRegressor(),
                "K-Nearest Neighbors": KNeighborsRegressor(),
                "XGBoost": XGBRegressor(),
                "Linear Regression": LinearRegression(),
            }

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))
            ## To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException(
                    "No model achieved an R2 score of at least 0.60"
                )
            
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )                  
            predictions = best_model.predict(X_test)
            r2_square = r2_score(y_test, predictions)
            return r2_square
        except Exception as e:
            raise CustomException(e, sys)
