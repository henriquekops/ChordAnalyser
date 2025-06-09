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

# project
from src.util.contants import (
    DATASET_DIRECTORY,
    DATASET_EXTENSION,
    MODEL_DIRECTORY,
    MODEL_EXTENSION,
    TARGET_LANDMARK_COUNT
)
from src.detect import HandDetector
from src.util.interface import Interface
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

    def __init__(self, name):
        self.__name = name
        self.__classifier = None

    def __create_classifier(self, trained):
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
            path = IO.gen_path(MODEL_DIRECTORY, self.__name, MODEL_EXTENSION)
            self.__classifier: RandomForestClassifier = joblib.load(path)

    @staticmethod
    def __read_dataset(directory):
        _directory = os.path.join(directory, '')
        files = glob.glob(_directory + f'*.{DATASET_EXTENSION}')
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
        IO.create_directory_if_not_exists(MODEL_DIRECTORY)
        path = IO.gen_path(MODEL_DIRECTORY, self.__name, MODEL_EXTENSION)
        joblib.dump(self.__classifier.best_estimator_, path)
        print(f'Model saved at {path}')

    def __analyse(self, frame):
        predict = ''
        landmarks = self.__detector.detect(frame)
        self.__detector.draw(frame, landmarks)

        if landmarks:
            entry = self.__detector.get_coordinates(landmarks)

            if len(entry) != TARGET_LANDMARK_COUNT:
                return True
            entry = np.array(entry).reshape(1, -1)
            predict = self.__classifier.predict(entry)[0]

        if predict:
            Interface.write_text(frame, f'Chord: {predict}', (0, 50))

    def train(self):
        self.__create_classifier(trained=False)
        df = self.__read_dataset(DATASET_DIRECTORY)
        bag = self.__split_train_test(df)
        self.__classifier.fit(bag.x_train, bag.y_train)
        y_predict = self.__classifier.predict(bag.x_test)
        self.__show_metrics(bag.y_test, y_predict)
        self.__save()

    def start(self):
        self.__create_classifier(trained=True)
        Video.start_capture(self.__analyse)
