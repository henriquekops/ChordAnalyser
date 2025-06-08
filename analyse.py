import os
import glob
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import numpy as np

from detect import HandDetector
from video import start_capture
from interface import Interface


class TrainTestBag:
    def __init__(self, x_train, x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test


class ChordAnalyser:

    __DIRECTORY = 'model'
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
            self.__classifier: RandomForestClassifier = joblib.load(f'{self.__DIRECTORY}/{self.__name}.pkl')

    @staticmethod
    def __read_dataset(directory):
        _directory = os.path.join(directory, '')
        files = glob.glob(_directory + '*.csv')
        dataset = np.vstack([pd.read_csv(file).values for file in files])
        return pd.DataFrame(dataset)

    @staticmethod
    def __split_train_test(df):
        x = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)
        return TrainTestBag(x_train, x_test, y_train, y_test)

    def __show_metrics(self, y_test, y_predict):
        print(f'===Best Estimator===\n{self.__classifier.best_estimator_}')
        print(f'===Classification Report===\n{classification_report(y_test, y_predict)}')
        print(f'===Confusion Matrix===\n{confusion_matrix(y_test, y_predict)}')

    def __create_directory_if_not_exists(self):
        if not os.path.exists(self.__DIRECTORY):
            os.makedirs(self.__DIRECTORY)

    def __save(self):
        self.__create_directory_if_not_exists()
        path = f'{self.__DIRECTORY}/{self.__name}.pkl'
        joblib.dump(self.__classifier.best_estimator_, path)
        print(f'Model saved at {path}')

    def train(self, path):
        self.__create_classifier(trained=False)
        df = self.__read_dataset(path)
        bag = self.__split_train_test(df)
        self.__classifier.fit(bag.x_train, bag.y_train)
        y_predict = self.__classifier.predict(bag.x_test)
        self.__show_metrics(bag.y_test, y_predict)
        self.__save()

    def __analyse(self, frame):
        landmarks = self.__detector.detect(frame)
        self.__detector.draw(frame, landmarks)

        predict = ''

        if landmarks:
            entry = self.__detector.get_coordinates(landmarks)

            if len(entry) != 42:
                return True

            entry = np.array(entry).reshape(1, -1)
            predict = self.__classifier.predict(entry)[0]

        if predict:
            Interface.write_text(frame, f'Chord: {predict}', (0, 50))

    def start(self):
        self.__create_classifier(trained=True)
        start_capture(self.__analyse)
