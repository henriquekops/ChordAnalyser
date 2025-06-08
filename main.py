from dataset import DatasetCreator
from detect import HandDetector
from analyse import ChordAnalyser


if __name__ == '__main__':
    cmd = input('command: ')
    if cmd == 'capture':
        DatasetCreator(100).start()
    elif cmd == 'detect':
        HandDetector().start()
    elif cmd == 'train':
        ChordAnalyser('chordAnalyser').train('dataset')
    elif cmd == 'predict':
        ChordAnalyser('chordAnalyser').start()
    else:
        print('invalid command')
