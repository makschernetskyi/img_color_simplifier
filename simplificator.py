from PIL import Image
from itertools import chain
import numpy as np
from datetime import datetime
from k_means import k_means

IMG_NAME = "img_5.jpg"
IMG_PATH = "./test_photos/"
OUT_PATH = "./processed_pictures/"






if __name__ == "__main__":

    img = Image.open(IMG_PATH + IMG_NAME)
    width, height = img.size
    indexed_pixel_values = list(map(lambda p: [p[0], *p[1:][0]], enumerate(list(img.getdata()))))

    clusters_number = 16

    clusters = k_means(indexed_pixel_values, clusters_number, id_column=True)

    modified_clusters = clusters.copy()

    for i in range(clusters_number):
        for j in range(len(clusters[i])):
            for k in range(1, len(modified_clusters[i][j])):
                modified_clusters[i][j][k] = clusters[i][0][k]

    new_indexed_pixel_values = list(chain(*modified_clusters))
    new_pixel_values = [[0, 0, 0] for i in range(len(new_indexed_pixel_values))]
    for p in new_indexed_pixel_values:
        for k in range(1, len(p)):
            new_pixel_values[p[0]][k-1] = p[k]


    new_img = Image.fromarray(np.array(new_pixel_values, dtype=np.uint8).reshape((height, width, 3)), mode="RGB")

    # Save the image to a file (you can change the file format and filename)
    new_img.save(OUT_PATH + IMG_NAME[:-4] + datetime.now().strftime("%Y%m%d%H%M%S") + IMG_NAME[-4:])

