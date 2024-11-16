import arcpy
from arcpy import env
import numpy as np

# 设置工作环境
arcpy.env.overwriteOutput = True

# 输入栅格路径
input_raster = r"Path\To\Your\Raster.tif"  # 输入栅格路径
output_raster = r"Path\To\Output\Reclassified_Raster.tif"  # 输出栅格路径

# 1. 读取栅格数据
raster = arcpy.Raster(input_raster)

# 2. 转换栅格为 NumPy 数组进行处理
array = arcpy.RasterToNumPyArray(raster)

# 3. 创建一个空的数组来存储分类后的结果
classified_array = np.zeros_like(array)

# 4. 根据数值范围进行分类
classified_array[array == -1] = 1  # 水体冰川积雪
classified_array[(array >= 0) & (array <= 0.1)] = 2  # 极低覆盖度
classified_array[(array > 0.1) & (array <= 0.3)] = 3  # 低覆盖度
classified_array[(array > 0.3) & (array <= 0.5)] = 4  # 中覆盖度
classified_array[(array > 0.5) & (array <= 0.7)] = 5  # 中高覆盖度
classified_array[(array > 0.7) & (array <= 1)] = 6  # 高覆盖度

# 5. 将分类数组转换回栅格
classified_raster = arcpy.NumPyArrayToRaster(classified_array, raster.extent.lowerLeft, raster.meanCellWidth, raster.meanCellHeight)

# 6. 保存重分类后的栅格
classified_raster.save(output_raster)

# 7. 向栅格的属性表添加字段并更新字段值
# 首先，确保栅格图层包含属性表
arcpy.management.AddField(output_raster, "Coverage_Type", "TEXT")

# 使用 UpdateCursor 更新每个像素的分类信息
with arcpy.da.UpdateCursor(output_raster, ["Value", "Coverage_Type"]) as cursor:
    for row in cursor:
        value = row[0]
        if value == 1:
            row[1] = "水体冰川积雪"
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

print(f"分类完成，新的栅格文件保存在： {output_raster}")
