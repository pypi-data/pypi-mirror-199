from ultralytics import YOLO


def train(epoch):
    model = YOLO("yolov8s.pt")
    model.train(data="coco128.yaml", epochs=epoch)
    model.val()
    print("coco128 train and val finished !")


if __name__ == '__main__':
    train(5)
