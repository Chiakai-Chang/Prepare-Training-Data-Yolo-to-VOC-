# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 16:54:31 2022

@author: chiakai
"""

import os, shutil
from PIL import Image

'''
超參數設定: 輸入
'''

# 資料所在資料夾
input_folder = os.getcwd()

# 依序號存取 class 名稱的 txt
classes_file = os.path.join(input_folder, 'classes.txt')
classes = open(classes_file).read().splitlines()
print(classes)

# 標註資料的 txt 所在資料夾
source_txt_path = {
    'train': os.path.join(input_folder, 'train_labels'),
    'val': os.path.join(input_folder, 'val_labels'),
    'test': '',
    }

# img 所在資料夾
source_img_path = {
    'train': os.path.join(input_folder, 'train'),
    'val': os.path.join(input_folder, 'val'),
    'test': os.path.join(input_folder, 'test'),
    }


'''
超參數設定: 輸出
'''
# 輸出 VOC 格式的資料夾
output_folder = os.path.join(os.getcwd(), 'VOC2007')
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)
    
# Annotations (要輸出的 xml 的位置)
folder_Annotations = os.path.join(output_folder, 'Annotations')
if not os.path.isdir(folder_Annotations):
    os.mkdir(folder_Annotations)

# ImageSets
folder_ImageSets = os.path.join(output_folder, 'ImageSets')
if not os.path.isdir(folder_ImageSets):
    os.mkdir(folder_ImageSets)

folder_ImageSets = os.path.join(folder_ImageSets, 'Main')
if not os.path.isdir(folder_ImageSets):
    os.mkdir(folder_ImageSets)

# JPEGImages
folder_JPEGImages = os.path.join(output_folder, 'JPEGImages')
if not os.path.isdir(folder_JPEGImages):
    os.mkdir(folder_JPEGImages)
if not os.path.isdir(os.path.join(folder_JPEGImages, 'train')):
    os.mkdir(os.path.join(folder_JPEGImages, 'train'))
if not os.path.isdir(os.path.join(folder_JPEGImages, 'val')):
    os.mkdir(os.path.join(folder_JPEGImages, 'val'))
if not os.path.isdir(os.path.join(folder_JPEGImages, 'test')):
    os.mkdir(os.path.join(folder_JPEGImages, 'test'))

'''
開始轉換格式
'''

for data_type in ['train', 'val', 'test']:
    
    main_txt = os.path.join(folder_ImageSets, f'{data_type}.txt')
    main_file = open(main_txt, 'w')
    
    if data_type == 'test':
        for file in os.listdir(source_img_path[data_type]):
            
            main_file.write(f'{str(file).replace(".jpg","")}\n')
            
            # 圖片複製到 JPEGImages 資料夾
            shutil.copy(
                os.path.join(source_img_path[data_type], file), 
                os.path.join(folder_JPEGImages, file)
                )
        main_file.close()
        continue
    
    for file in os.listdir(source_txt_path[data_type]):
        
        main_file.write(f'{str(file).replace(".txt","")}\n')
        
        # 圖片複製到 JPEGImages 資料夾
        img_path = os.path.join(source_img_path[data_type], file.replace('.txt','.jpg'))
        shutil.copy(img_path, os.path.join(folder_JPEGImages, file.replace('.txt','.jpg')))
        
        # 讀取圖片
        img_file = Image.open(img_path)
        
        # 讀取標註資料
        txt_file = open(os.path.join(source_txt_path[data_type], file)).read().splitlines()
        #print(txt_file)
        
        # 生成 xml
        xml_file = open(os.path.join(folder_Annotations, file.replace('.txt','.xml')), 'w')
        width, height = img_file.size
        xml_file.write('<annotation>\n')
        xml_file.write(f'\t<folder>{data_type}</folder>\n')
        xml_file.write('\t<filename>' + str(file) + '</filename>\n')
        xml_file.write('\t<size>\n')
        xml_file.write('\t\t<width>' + str(width) + ' </width>\n')
        xml_file.write('\t\t<height>' + str(height) + '</height>\n')
        xml_file.write('\t\t<depth>' + str(3) + '</depth>\n')
        xml_file.write('\t</size>\n')
    
        for line in txt_file:
            print(line)
            line_split = line.split(' ')
            x_center = float(line_split[1])
            y_center = float(line_split[2])
            w = float(line_split[3])
            h = float(line_split[4])
            xmax = int((2*x_center*width + w*width)/2)
            xmin = int((2*x_center*width - w*width)/2)
            ymax = int((2*y_center*height + h*height)/2)
            ymin = int((2*y_center*height - h*height)/2)
    
            xml_file.write('\t<object>\n')
            xml_file.write('\t\t<name>'+ str(classes[int(line_split[0])]) +'</name>\n')
            xml_file.write('\t\t<pose>Unspecified</pose>\n')
            xml_file.write('\t\t<truncated>0</truncated>\n')
            xml_file.write('\t\t<difficult>0</difficult>\n')
            xml_file.write('\t\t<bndbox>\n')
            xml_file.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
            xml_file.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
            xml_file.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
            xml_file.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
            xml_file.write('\t\t</bndbox>\n')
            xml_file.write('\t</object>\n')
        xml_file.write('</annotation>')
        xml_file.close()
    main_file.close()
    
print('finish')