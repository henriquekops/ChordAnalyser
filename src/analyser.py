#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import glob
import os

# external lib
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

# project
from src.detector import HandDetector
from src.ui.hud import Interface
from src.util.config import Core
from src.util.io import IO
from src.util.video import Video


class ChordAnalyser:

    """Machine learning based chord analyser"""

    class __TrainTestBag:
        def __init__(self, x_train, x_test, y_train, y_test):
            self.x_train = x_train
            self.x_test = x_test
            self.y_train = y_train
            self.y_test = y_test

    __detector = HandDetector()

    def __init__(self):
        self.__classifier = None
        self.__path = IO.gen_path(Core.IO.MODEL_DIRECTORY, Core.IO.MODEL_NAME, Core.IO.MODEL_EXTENSION)

    def __get_knn_classifier(self, trained):
        if not self.__classifier and not trained:
            self.__classifier = GridSearchCV(
                estimator=KNeighborsClassifier(),
                param_grid={
                    'n_neighbors': [3, 5],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                },
                cv=5,
                scoring='accuracy',
                n_jobs=1
            )
        elif not self.__classifier and trained:
            self.__classifier: KNeighborsClassifier = joblib.load(self.__path)

    def __get_rf_classifier(self, trained):
        if not self.__classifier and not trained:
            self.__classifier = GridSearchCV(
                estimator=RandomForestClassifier(random_state=42),
                param_grid={
                    'n_estimators': [100, 200],
                    'max_depth': [None, 20, 10]
                },
                cv=5,
                scoring='accuracy',
                n_jobs=1
            )
        elif not self.__classifier and trained:
            self.__classifier: RandomForestClassifier = joblib.load(self.__path)

    def __get_classifier(self, trained):
        if Core.Landmark.CLASSIFIER == 'KNN':
            return self.__get_knn_classifier(trained)
        elif Core.Landmark.CLASSIFIER == 'RF':
            return self.__get_rf_classifier(trained)
        else:
            raise ValueError(Core.Landmark.NO_CLASSIFIER_ERROR + Core.Landmark.CLASSIFIER)

    @staticmethod
    def __read_dataset(directory):
        _directory = os.path.join(directory, '')
        files = glob.glob(_directory + f'*.{Core.IO.DATASET_EXTENSION}')
        dataset = np.vstack([pd.read_csv(file).values for file in files])
        return pd.DataFrame(dataset)

    def __split_train_test(self, df):
        x = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y,
            test_size=0.2,
            stratify=y,
            random_state=42
        )
        return self.__TrainTestBag(x_train, x_test, y_train, y_test)

    @staticmethod
    def __show_metrics(y_test, y_predict):
        print(f'===Classification Report===\n{classification_report(y_test, y_predict)}')
        print(f'===Confusion Matrix===\n{confusion_matrix(y_test, y_predict)}')

    def __save(self):
        IO.create_directory_if_not_exists(Core.IO.MODEL_DIRECTORY)
        joblib.dump(self.__classifier.best_estimator_, self.__path)

    def __analyse(self, frame):
        predict = ''
        landmarks = self.__detector.detect(frame)
        x = 0
        y = 0

        if landmarks:
            h, w, _ = frame.shape
            landmark = landmarks[0].landmark[0]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            entry = self.__detector.get_coordinates(landmarks)

            if len(entry) != Core.Landmark.TARGET_LANDMARK_COUNT:
                return True

            entry = np.array(entry).reshape(1, -1)
            predict = self.__classifier.predict(entry)[0]

        if predict:
            Interface.write_text(frame, predict, (x+200, y-300), color=(0, 255, 0), size=2, thickness=6)

    def train(self):
        if not IO.exists(Core.IO.DATASET_DIRECTORY):
            return False

        self.__get_classifier(trained=False)

        df = self.__read_dataset(Core.IO.DATASET_DIRECTORY)
        bag = self.__split_train_test(df)

        self.__classifier.fit(bag.x_train, bag.y_train)

        y_predict = self.__classifier.predict(bag.x_test)

        self.__show_metrics(bag.y_test, y_predict)
        self.__save()
        return True

    def start(self):
        if not IO.exists(self.__path):
            return False

        self.__get_classifier(trained=True)
        Video.start_capture(self.__analyse)

        return True
