from dataset import DatasetCreator
from detector import HandDetector


if __name__ == '__main__':
    cmd = input('command: ')
    if cmd == 'capture':
        DatasetCreator(1000).start()
    elif cmd == 'detect':
        HandDetector().start()
    else:
        print('invalid command')
