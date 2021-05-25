import cv2
import xml.etree.ElementTree as ET
import os

cropped_images_directory = "./cropped_images/"
if os.path.islink(cropped_images_directory):
    os.mkdir(cropped_images_directory)
    bead_directory = os.path.join(cropped_images_directory, 'bead')
    dust_directory = os.path.join(cropped_images_directory, 'dust')
    os.mkdir(bead_directory)
    os.mkdir(dust_directory)
else:
    pass

Annotations_Path = "./Training Images_ Annotations/"
Annotations_terms = os.listdir(Annotations_Path)
# print(Annotations_terms)

Images_Path = "./Training Images/"
Images_terms = os.listdir(Images_Path)
# print(Images_terms)

Save_CroppedImages_Path = "./cropped_images/"
total_bead = 0
total_dust = 0
for dir_id in range(len(Images_terms)):
    image_dir_path = os.path.join(Images_Path, Images_terms[dir_id])
    annotation_dir_path = os.path.join(Annotations_Path, Annotations_terms[dir_id])

    image_files = os.listdir(image_dir_path)
    xml_files = os.listdir(annotation_dir_path)

    for file_id in range(len(image_files)):
        xml = ET.parse(os.path.join(annotation_dir_path, xml_files[file_id]))
        image = os.path.join(image_dir_path, image_files[file_id])
        root = xml.getroot()
        objs = root.findall('object')

        print("Processing image " + image_dir_path + '/' + image_files[file_id] + "...")
        bead_num = 0
        dust_num = 0
        image_name = image_files[file_id].split('.jpg')
        for obj_id in range(len(objs)):
            name = objs[obj_id].find('name').text
            bndbox = objs[obj_id].find('bndbox')
            xmin = int(bndbox[0].text)
            ymin = int(bndbox[1].text)
            xmax = int(bndbox[2].text)
            ymax = int(bndbox[3].text)

            if name == 'bead':
                bead_num += 1
                total_bead += 1
                img = cv2.imread(image)
                crop_img = img[ymin:ymax, xmin:xmax]
                cv2.imwrite(Save_CroppedImages_Path + 'bead/' + image_name[0] + '_' + str(bead_num) + '.jpg', crop_img)
            elif name == 'dust':
                dust_num += 1
                total_dust += 1
                img = cv2.imread(image)
                crop_img = img[ymin:ymax, xmin:xmax]
                cv2.imwrite(Save_CroppedImages_Path + 'dust/' + image_name[0] + '_' + str(dust_num) + '.jpg', crop_img)

print("--------------------------------------------------------------")
print("Finish!")
print("Total number of bead: ", total_bead)
print("Total number of dust: ", total_dust)