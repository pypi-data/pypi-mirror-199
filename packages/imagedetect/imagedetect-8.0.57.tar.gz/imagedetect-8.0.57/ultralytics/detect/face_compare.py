import face_recognition


def face_compare(img1, img2):
    # 加载图片
    image1 = face_recognition.load_image_file(img1)
    image2 = face_recognition.load_image_file(img2)

    # 识别面部特征
    face1 = face_recognition.face_encodings(image1)[0]
    face2 = face_recognition.face_encodings(image2)[0]

    # 比较面部特征相似度
    results = face_recognition.compare_faces([face1], face2, 0.5)

    # 显示结果
    if results[0]:
        print("这两张图片是同一个人")

        distance = face_recognition.face_distance([face1], face2)
        distance = round(distance[0] * 100)

        accuracy = 100 - round(distance)

        print(f"Accuracy Level: {accuracy}%")

    else:
        print("这两张图片不是同一个人")
        distance = face_recognition.face_distance([face1], face2)
        distance = round(distance[0] * 100)

        accuracy = 100 - round(distance)

        print(f"Accuracy Level: {accuracy}%")


if __name__ == '__main__':
    # for i in range(14):
    #     face_compare('image/14.jpeg', 'image/'+str(i+1)+'.jpeg')
    face_compare('image/5.jpeg', 'image/11.jpeg')
