# 3D Reconstruction

目前三维重建系统由两部分组成：SfM部分和多视图几何部分，其中SfM部分参考[OpenMVG](https://github.com/openMVG/openMVG),多视图几何部分参考[OpenMVS](https://github.com/cdcseacave/openMVS)

- **build

SfM: 参考/openMVG/BUILD

OpenMVS: 参考/openMVS/BUILD.md

- **Run

先运行SfM部分：

python sfm.py 重建图像数据集目录 SfM结果保存目录

然后运行mvs部分：

python mvs.py SfM结果保存目录 mvs结果保存目录

需要修改两个脚本中的可执行文件和相机参数文件路径
