import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import os
from PIL import Image

os.mkdir(os.path.join('.', 'uploads'))
os.mkdir(os.path.join('.', 'downloads'))

def convert_to_jpg(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)
        
        # Convert to RGB mode if image is not in RGB mode
        # if img.mode != 'RGB':
        #     img = img.convert('RGB')
        
        # Save the image as JPG
        jpg_path = os.path.splitext(image_path)[0] + ".jpg"
        img.save(jpg_path, "JPEG")
        print(f"Converted {image_path} to {jpg_path}")
        
    except Exception as e:
        print(f"Error converting {image_path}: {e}")

def delete_image(image_path):
    try:
        os.remove(image_path)
        print(f"Deleted {image_path}")
    except Exception as e:
        print(f"Error deleting {image_path}: {e}")

# Path to the directory containing images
directory = os.path.join('.','uploads')


for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".webp") or filename.endswith(".jfif") or filename.endswith(".avif"):
        # Convert the image to JPG
        convert_to_jpg(os.path.join(directory, filename))

for filename in os.listdir(directory):
    if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".webp") or filename.endswith(".jfif") or filename.endswith(".avif"):
        # Convert the image to JPG
        delete_image(os.path.join(directory, filename))

def image_path():
    image_paths = []
    for image in os.listdir('uploads'):
        image_paths.append(image)
    return image_paths

def image_compressor(pca):
    image_paths = image_path()
    print(image_paths)
    for image in image_paths:
        img = cv2.imread(os.path.join(".",f"uploads/{image}"))
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # plt.imshow(img_rgb)
        # plt.show()
        r,g,b = cv2.split(img_rgb)
        r,g,b = r/255,g/255,b/255
        # plt.imshow(r)
        pca_components = pca

        pca_r = PCA(n_components=pca_components)
        reduced_r = pca_r.fit_transform(r)

        pca_g = PCA(n_components=pca_components)
        reduced_g = pca_g.fit_transform(g)

        pca_b = PCA(n_components=pca_components)
        reduced_b = pca_b.fit_transform(b)
        # combined = np.array([reduced_r,reduced_g,reduced_b])
        reconstructed_r = pca_r.inverse_transform(reduced_r)
        reconstructed_g = pca_g.inverse_transform(reduced_g)
        reconstructed_b = pca_b.inverse_transform(reduced_b)
        # plt.imshow(reconstructed_r)
        img_reconstructed = cv2.merge((reconstructed_r,reconstructed_g,reconstructed_b))
        image_name = image[0:len(image)-4]
        img_path = os.path.join('.',f'downloads/{image_name}')
        plt.imshow(img_reconstructed)
        plt.axis('off')
        fig = plt.gcf()
        # Adjust the figure size to match the content of the image
        fig.set_size_inches(img_reconstructed.shape[1] / 100.0, img_reconstructed.shape[0] / 100.0)
        plt.savefig(f"{img_path}_compressed.jpg", bbox_inches='tight', pad_inches=0)
        # plt.show()
        # img_con = cv2.convertScaleAbs(img_reconstructed)
        # img_bgr = cv2.cvtColor(img_con,cv2.COLOR_RGB2BGR)
        # cv2.imwrite(f"{img_path}_compressed.jpg", 255*img_reconstructed)
        directory = os.path.join('.','uploads')
        delete_image(os.path.join(directory,image))
def main():
    image_compressor(100)

if __name__ == "__main__":
    main()
