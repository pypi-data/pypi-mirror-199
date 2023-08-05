Orange3 Earth Observation Add-on
======================

This is an add-on for [Orange3](https://orangedatamining.com/). Add-on can extend Orange either 
in scripting or GUI part, or in both. Register it with Orange and add a new workflow with some 
of these widget to example tutorials.

Installation
------------

To install the add-on from source run

    pip install .

Usage
-----

After the installation, widgets from this add-on are registered with Orange. To run Orange from the terminal,
use

    orange-canvas

or

    python -m Orange.canvas

New widgets appears in the toolbox bar under the section Earth Observation.

![screenshot](screenshots/category_EO.png)

Widgets Description
-----

**ODM** (_Orange Data Mining_) is an open source machine learning and data visualization tool.
It allows to build data analysis workflows visually, with a large, diverse toolbox.

It also allows to write its own widget in order to extend Orange functionalities either in scripting or GUI, 
for this, you can write an add-on, add-ons implement additional widgets for more specific use cases. 
Refer to Orange [documentation](https://github.com/biolab/orange3/blob/stable/README.md) for details on how 
to install and use ODM, also an example [Add-on](https://github.com/biolab/orange3-example-addon) for Orange. 


We develop a list of widgets to be used in ODM, each widget has a functionality to be mainly applied on 
EO (Earth Observation) Data.

## EODataCatalog Widget

Offers access to 3 services; `ODataServiceNodeCSC`, `ODataServiceNodeDhus` and `ODataServiceNodeDias` via OData Protocol.

OData services require authentication which is performed using drb keyring connection, refer to 
[documentation](https://gitlab.com/drb-python/impl/odata) for more details on how to use.


EODataCatalog Widget has a list of multi-option boxes to filter for products by **Mission**, **Platform**, **Type**, 
**Sensor**, and a slider to define the **Cloud Cover** maximum value, the filter is passed through `ODataQueryPredicate`. 

A `DrbNode` is retrieved, and can be passed through the output to be used by other ODM widgets, the product corresponding 
can also be downloaded to local file.


![](screenshots/Catalog.png)

## EONutsShape Widget

EONutsShape Widget is used to crop Sentinel 2 TCI (True Color Image), remove parts not part of NUTS shape. 
It takes a `DrbNode` as input, needs a file in .shp format containing polygons shapes corresponding to NUTS Region. 
The output is a `DrbImageBaseNode` of the TC Image in selected NUTS Region. 


![](screenshots/Nuts.png)

## EOMosaicImage Widget

EOMosaicImage Widget is used to assemble image parts when possible, creating a mosaic image, corresponding to a predefined NUTS Region. 
It takes a list of `DrbImageBaseNode` as input, all inputs need to be in same CRS and NUTS region. 
The output is a `DrbImageBaseNode` of the assembled TC Image. 

![](screenshots/Mosaic.png)

## EOReprojectImage Widget

EOReprojectImage Widget is used to reproject an image from one CRS to another. 
It takes a `DrbImageBaseNode` as input and outputs the same.

![](screenshots/Projection.png)

## EOCloudMask Widget

EOCloudMask Widget is used to mask Sentinel 2 TCI (True Color Image), remove pixels representing clouds, 
shadows, water, snow or ice.
It takes a `DrbNode` as input, needs the SCL band containing the mask information which can be found 
in the same S2 product. The output is a `DrbImageBaseNode` of the TC Image with selected mask applied on.  

![](screenshots/Cloud.png)

## EOHistogram Widget

EOHistogram Widget is used for histogram visualisation, basic and adaptive histogram equalization.
It takes a `DrbImageBaseNode` as input, the output is a `DrbImageBaseNode` after histogram equalization are done. 
It might need to specify the **Clip Limit** which is used by the algorithm to apply adaptive equalization.
EOHistogram Widget can also take a list of `DrbImageBaseNode` as input, in order to perform a histogram matching 
after specifying the reference image. 

![](screenshots/Histogram.png)

## EOCropImage Widget

EOCropImage Widget is used to crop an image in a selected rectangle ROI, defined visually on the widget's GUI
with a red rectangle, sliders can be used to variate **Crop Size**, **Vertical Range X** and the
**Horizontal Range Y** that modify visually the red rectangle's size and position.
It takes a `DrbImageBaseNode` as input, the output is a `DrbImageBaseNode` of the cropped image. 

![](screenshots/Crop.png)

## EOLoadImage Widget

EOLoadImage Widget is used to load images from the directory structure.
The output is a `DrbImageBaseNode` of the selected image. 

![](screenshots/Load.png)

## EOViewImage Widget

EOViewImage Widget is used to visualize images inside Orange Data Mining.
A slider is used to variate **Image Size** that modify visually the size of the image.
It takes a list of `DrbImageBaseNode` as input, the output is a `DrbImageBaseNode` of the selected image. 

![](screenshots/View.png)
