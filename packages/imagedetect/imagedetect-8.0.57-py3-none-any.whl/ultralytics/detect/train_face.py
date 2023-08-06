from ultralytics import YOLO


def train():
    model = YOLO("yolov8s-face.yaml")
    model.train(data="face.yaml", epochs=10)
    model.val()
    print("face train and val finished !")


if __name__ == '__main__':
    train()
