#  Dataset for precolombian reconstruction

> Compiled by: Pablo Jaramillo & Joaquín Cruz 

> Under guidance of professor Iván Sipirán

> At: Universidad de Chile, Department of Computer Sciences, Santiago, Chile.

## Nature

This dataset is a compilation and selection from previously existing datasets in order to train neural networks for repairing precolombian earthenware artifacts such as, and mainly, bowls.

The data present in these datasets was obtained from the publically available data of ShapeNet, ModelNet40, and Native American Pottery. Also included are a handful of scans of artifacts from The Josefina de Cox Museum.

All objects in this dataset are named with a prefix in accordance of their source and serialized in a 4 digit numerical ID, the prefix is followed by an underscore. Augmentations of the present files contain an additional underscore followed by their augmentation ID. The ID is the same as the one in the source if it had a 4 digit numerical ID, if the original source had the objects hashed then they correspond to an increasing alphabetical order of the original source.

|Dataset|Prefix|incremental ID|
|:------|:----:|-------|
|ModelNet40| MD | yes |
|Native American Pottery| NA | No |
|Josefina de Cox Museum| SC | No |
|ShapeNet | SN  | Yes |

## Work

This dataset was used in the memoir work for qualifying for the Bacherlor's degree of Computer Engineer by Pablo Jaramillo "3D Reconstruction with Diffusion Neural Networks" and Joaquín Cruz's MsC degree thesis.

## Content

This section explains the contents of the present dataset and how to use it.

### Collection

All original mesh files are present in the ``precol`` directory in their respective subdirectories ``MD40_bowl``, ``native``, ``SN_bowl``, and ``scanned``.

### Point Data

Usable point cloud training and evaluation data once created is located in the ``precol`` directory and once processed, separated in 3 subdirectories: ``broken``, ``complete``, and ``repair``. 

The ``complete`` subdirectory contains copies of the data in ``collection``. Copies of the present files may be found, if so they are copies and have no differences.

The ``broken`` subdirectory contains the input part of the files' namesake counterpart of ``complete``. Items here represent an obtained broken artifact meant to be repaired by being fed as input to a DL model.

The ``repair`` subdirectory contains the ground truth to the repair task over the respective counterparts in ```broken``.

Ideally you should separate the The mesh scans of the the Josefina de Cox Museum in a different subdirectory like ``validate`` to contain their undersampled point clouds obtained from the process up to the collection generation. These shapes are to be used as input for models as a validation task, as they have no ground truth.

### Scripts

Useful configurable python scripts for managing this data can be found in the ``scripts`` directory. The scripts found here can sample meshes into point clouds, copy files on mass, create a repair task over the data, and create a train-test split.

## How to use

If you plan on making your own repair task utilizing the framework of this dataset then you may follow these steps as a guide. Note: **the working directory is designed to be the root level of the repository**, there are not many safeguards to guarantee good execution in other cases.

1. Obtain point clouds from meshes.
    - 
    To sample points from mesh files you may use [the dataset preprocessing script](scripts/preproc_dataset.py), as follows:

    ```
    python preproc_dataset.py --dataset <path_to_dataset> --points <integer>
    ```

    This script is an altered version from the one present in  the MICCAI 2023 paper [Point Cloud Diffusion Models for Automatic Implant Generation](https://pfriedri.github.io/pcdiff-implant-io/) by Paul Friedrich, Julia Wolleb, Florentin Bieder, Florian M. Thieringer and Philippe C. Cattin. The repository of the original work can be found in [this link](https://github.com/pfriedri/pcdiff-implant).

    Other arguments may be used for miscellaneous utility to determine which files to process, how to process them, and other characteristics of the data.

    The resulting data from this script will be stored in the same directory as the source in .npy format. 


2. Create a train-test split

    This is achieved through the [provided splitting script](scripts/collect_complete.py). This script will copy objects from the dataset directories into a collection directory as well as creating csv files for the split. These csv files aren't final and meant as reference for the next stage for the data augmentation.  

    ```
    python collect_complete.py 
    ```


3. Separate point clouds into input and ground truth
    - 
    The mechanism to achieve this in this dataset is designed to emulate the defects originating from scanning an object where the fragility of the object prevents a correct scanning of the bottom of the object. This means effectively that [the script provided](scripts/degrade_cloud_bottom.py) performes simple regular cuts at an adjustable height and angle.

    ```
    python degrade_cloud_bottom.py --dataset <path_to_dataset> --breakage <float> --variance <float> 
                            --maxx <float> --maxy <float> --maxz <float> --n_breaks <integer>
    ```

    This script processes point clouds such that for each it will create ``n_breaks`` data points.

    A data point is creating a plane of separation for the points where all points above are treated as input and all those below as ground truth. The plane is located around the height of ``breakage`` inside an unit cube, randomly placed within a (1 +- ``variance``) factor of this height.

    Before the plane is created the object is transformed by a seedable randomized rotation configurable on the X, Y, and Z axis, with ``maxx``, ``maxy``, and ``maxz`` being the maximum degrees allowed for the rotation. After this rotation is performed the object is separated and has the rotation undone.

    The final 2 point clouds are saved under the same name in the dataset's ``broken`` and ``repair`` subdirectories, additionally a copy of the original point cloud is stored in ``complete``.

    The script allows to create a mesh counterpart for all parts involved by a marching cubes algorithm.

