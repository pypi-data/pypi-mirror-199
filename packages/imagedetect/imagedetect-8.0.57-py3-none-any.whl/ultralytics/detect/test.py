from ultralytics.detect.predict_coco128 import predict_img

if __name__ == '__main__':
    predict_img('best.pt', 'person.png')
