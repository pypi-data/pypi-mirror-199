import base64

def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')


file = r'c:\git\npbackup\npbackup\icon_npbackup.png'
print(image_to_data_url(file))