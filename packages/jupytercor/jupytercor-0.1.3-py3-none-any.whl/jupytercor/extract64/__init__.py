import base64
from PIL import Image
from io import BytesIO


def extract_image_64(base64_string, nom_fichier):
    # Remove the prefix and get only the base64 data
    base64_data = base64_string.split(",")[-1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Create an image object from the bytes
    image = Image.open(BytesIO(image_bytes))
    # Save the image to a file
    image.save("images/"+nom_fichier)

def extract_attachemnt_image(base64_data, nom_fichier, total_images):
    
    print("dans la fonction")
    # Decode the base64 data to bytes
    #imagedata = base64.decodestring(base64_data)
    image_bytes = base64.b64decode(base64_data)
    # Create an image object from the bytes
    # with open("images/"+nom_fichier, "wb") as f:
    #     f.write(imagedata)
    image = Image.open(BytesIO(image_bytes))
    # Save the image to a file
    image.save("images/"+str(total_images)+"-"+nom_fichier)

