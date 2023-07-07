import imghdr

def is_jpeg(data):
    return imghdr.what(file=None, h=data) == "jpeg"


if __name__ == '__main__':

    print(imghdr.what(file='../skin.jpg'))





