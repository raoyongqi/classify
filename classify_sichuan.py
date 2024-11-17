import os
import arcpy
from arcpy import sa  # 导入空间分析模块

# 设置工作环境
arcpy.env.overwriteOutput = True

# 输入栅格数据和掩膜文件
input_raster_folder = r"C:\Users\r\Desktop\classify\xinjiang\xinjiang"  # 输入栅格数据路径
mask_shapefile = r"C:\Users\r\Desktop\classify\province\xinjiang\xinjiang.shp"  # 掩膜矢量文件路径

# 输出文件夹路径
output_raster_folder = r"C:\Users\r\Desktop\classify\xinjiang\extracted"  # 输出文件夹路径

# 检查输出文件夹是否存在，不存在则创建
if not os.path.exists(output_raster_folder):
    os.makedirs(output_raster_folder)
# 输出文件夹路径
wgs84_raster_folder = r"C:\Users\r\Desktop\classify\xinjiang\wsg84"  # 输出文件夹路径

# 检查输出文件夹是否存在，不存在则创建
if not os.path.exists(wgs84_raster_folder):
    os.makedirs(wgs84_raster_folder)

# 重分类字典
reclass_dict = {
    -1: 1,  # 水体冰川积雪
    (0, 0.1): 2,  # 极低覆盖度
    (0.1, 0.3): 3,  # 低覆盖度
    (0.3, 0.5): 4,  # 中覆盖度
    (0.5, 0.7): 5,  # 中高覆盖度
    (0.7, 1): 6   # 高覆盖度
}

# WGS84坐标系
wgs84 = arcpy.SpatialReference(4326)  # WGS84坐标系（EPSG:4326）

# 遍历文件夹中的所有 TIFF 文件
for filename in os.listdir(input_raster_folder):
    # 只处理 .tif 文件
    if filename.lower().endswith(".tif"):
        input_raster_path = os.path.join(input_raster_folder, filename)
        
        # 构建输出文件路径
        output_raster_path = os.path.join(output_raster_folder, f"extracted_{filename}")
        
        # 执行 Extract by Mask 操作
        try:
            # 裁剪栅格数据
            extracted_raster = sa.ExtractByMask(input_raster_path, mask_shapefile)
            
            # 保存裁剪后的栅格
            extracted_raster.save(output_raster_path)
            print(f"Extract by Mask operation completed for {filename}. Output saved as {output_raster_path}")
            
            # 进行重分类操作
            reclass_raster = arcpy.sa.Reclassify(extracted_raster, "VALUE", arcpy.sa.RemapRange([
                (-1, -1, 1),  # 水体冰川积雪
                (0, 0.2, 2),  # 极低覆盖度
                (0.2, 0.5, 3),  # 低覆盖度
                (0.5, 0.7, 4),  # 中覆盖度
                (0.7, 0.8, 5),  # 中高覆盖度
                (0.8, 1, 6)  # 高覆盖度
            ]))

            # 保存重分类后的栅格
            reclass_raster.save(output_raster_path)
            print(f"Reclassification completed for {filename}. Output saved as {output_raster_path}")

            # 向栅格的属性表添加字段并更新字段值
            # 首先，确保栅格图层包含属性表
            arcpy.management.AddField(output_raster_path, "Cover_Type", "TEXT")

            # 使用 UpdateCursor 更新每个像素的分类信息
            with arcpy.da.UpdateCursor(output_raster_path, ["Value", "Cover_Type"]) as cursor:
                for row in cursor:
                    value = row[0]
                    if value == 1:
                        row[1] = "水体和冰雪"
                    elif value == 2:
                        row[1] = "极低覆盖度"
                    elif value == 3:
                        row[1] = "低覆盖度"
                    elif value == 4:
                        row[1] = "中覆盖度"
                    elif value == 5:
                        row[1] = "中高覆盖度"
                    elif value == 6:
                        row[1] = "高覆盖度"
                    cursor.updateRow(row)

            print(f"Classification and attribute update completed for {filename}.")
            wgs84_raster_path = os.path.join(wgs84_raster_folder, f"wsg84_{filename}")
        
            # 设置坐标系为 WGS84 (EPSG:4326)
            
# Reproject the raster
            arcpy.management.ProjectRaster(output_raster_path, wgs84_raster_path, wgs84)
            print(f"Reprojection to WGS84 completed for {filename}. Output saved as {wgs84_raster_path}.")


        except Exception as e:
            print(f"Error processing {filename}: {e}")
