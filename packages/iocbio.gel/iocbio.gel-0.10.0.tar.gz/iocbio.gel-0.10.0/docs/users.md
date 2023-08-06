# Users Guide

## Starting the application

Start the application: 
Linux/Mac users run the command: `iocbio-gel/bin/iocbio-gel`
Windows users go to the extracted folder and run: `gel.bat`

## Settings

This is for first time users only: 

Go to Settings and select Image source and Database connection. Your selection depends on whether you want to store your files and results locally, i.e. on your own computer, or whether your files and results are stored in a shared space. 

### Image source

If your results are only on your own computer, select Image source “local” and Database connection “SQLite” from the drop-down lists.
Your workplace may also have a larger database for central storage of data from all lab members. For example, in our laboratory, all images are stored in our OMERO central repository (https://www.openmicroscopy.org/omero/). 
If your images and results are stored centrally, select Image source “omero”. Insert 

*	The host name/address, which should be available from your local systems administrator. 
*	The port – we suggest to use the default port (4064).
*	Your username 
*	Your password. 
Database connection
Under Database connection, select “PostgreSQL” from the drop-down lists. Insert

*	The host name/address, which should be available from your local systems administrator. 
*	The port – we suggest to use the default port (5432).
*	The SSL mode – we suggest to use the default (prefer encryption)
*	The name of your database, which should be available from your local systems administrator. 
*	The schema – we suggest to use the default (gel)
*	Your username 
*	Your password

Note: At the moment, this software supports only the use of Omero as the central image repository, and the use of PostgreSQL and SQLite to fetch the data. If there is interest, it is possible to support other image repositories and database connections through the SQLAlchemy library (contact the developers).

### Privacy

If needed, the settings for database connection can be removed under Privacy.

### Logs

Logs are kept in a separate folder and can be accessed here in the file called “app”. Please attach the log when reporting issues. See the section “Reporting issues”.

When the settings are set, go to 

## Types

Under Types, you define the types of measurements.

Note: The software has two modes to avoid accidental changes, viewing and editing, see the upper right corner. As a default, the software opens in viewing mode. In order to make any changes, click in the upper right corner. It will change to editing mode and you will be able to add types of measurements.

In the present example, we did a Western blot to assess the expression of AMPK. Before antibody incubation the membrane was dyed with Ponceau to visualize and assess the overall protein content in each lane. Therefore, we put the types “Ponceau” and “AMPK”.

With the types of measurements defined, go to 

## Projects

When doing multiple analyses, you might want to split your data according to which project they belong to. 
Click “Add a new project”. By double-clicking on the “Name” and “Comment” fields, you can name the project and add a comment. 

With the project defined, go to

## Gels

Make sure that you are still in the editing mode (see upper right corner).

Define a new gel by clicking on “+ New”.

Name the gel: Highlight the “Name” field and start typing.

Set the reference time. In our case, we used the date of imaging as the reference time, but this is open to interpretation and each user can decide which reference time to use. Highlight the “Reference time” field and double-click to see the drop-down calendar, where you can select the right date. You can also specify the time of the day. If this field is left blank, then the software will automatically put the current time.

Insert a comment, if needed, by highlighting the “Comment” field and typing.

Here, you also select which project this gel belongs to. Double-click on the “Project” field and select the project.

The number of lanes is determined automatically at a later stage.

You are now ready to start analyzing your images.

## Image analysis

“Gels” shows you a list of all the gels you have. To start the image analysis of a particular gel, press its ID in the list of gels or the name of the gel in the left column.
Define the lanes of the gel. Press “+ New” until you have the number of lanes that you want to analyze.

In our lab, we often have two ladders – one in the left-most and one in the right-most lane. As we do not include the ladder in the image analysis, we only analyze for example 13 out of 15 lanes. 

There are multiple columns:

*	The ID of the measurement
*	The number of the lane
*	The ID of the sample
*	The amount of protein that was loaded into each well on the gel
*	Tick if one of two of the samples are used as references for comparing between gels
*	Comments

If you want to shift the number of lanes, it is easier to do this already after adding the first lane. The number of the lane will increase with each new addition. 

When the details of the different lanes are added, you can add the images from this gel. Click on “Add new image”. If you did multiple images of the same membrane, for example Ponceau and anti-body staining, both pictures are added here.

You are now ready to analyze the signal intensity of the lanes in the pictures.

### Defining the region of interest (ROI)

Double-click on the image, you want to analyze. We usually start with the Ponceau image. This will open the picture in the “Adjust” tab. 

Before that, is the “Raw” tab, where you see the raw image as well as the inverted picture. 

In the “Adjust” tab, click on “Add ROI” to select the region of interest (ROI) that you have for your analysis. The ROI will be marked with a red square. The ROI can be move by clicking within the ROI and dragging it to where you want it to be. 

The ROI has two handles. In the upper left corner, there is a circular handle to change the rotation of the ROI. In the lower right corner, there is a diamond-shaped handle to change the size of the ROI. The rotation can also be set on the slider in the upper right corner. When you have defined your ROI, click “Apply”. 

### Background subtraction

After defining the ROI, you will automatically be taken to the “Background” tab, where you can subtract the background. First, you need to define whether the background colour is dark or light. Then, you select the kind of background subtraction that suits your image. There are three kinds of background:   

*	Flat
*	Ball
*	Ellipsoid

Select the kind of background subtraction that is the most suitable for your image. If the background has little variation, select the flat background. If the background is lighter in one part of the image than another, select “Ball” or “Ellipsoid”. For the latter two options, you need to define the radius of the ball or the radii of the ellipse. Select a relatively large radius (500 or more). If the radius is too small, part of the signal will also be subtracted. Click “Apply” to see the background that was subtracted as well as the final result. If you are not happy with the result, try to change to another kind of background subtraction, or change the diameter.

### Marking and positioning the lanes for analysis

With the background subtracted, go to “Lanes” and click “Add new lane”. Click until you have marked all the lanes that you want to analyze with an analysis lane. In each analysis lane, the center is marked with a green, dotted line, and the sides are marked with green dashed lines. The intensity profile of each analysis lane will show up in the right-side panel.

You can zoom in and out by clicking on the gel picture and using the scrolling wheel of your mouse.

You will need to adjust the position and shape of the analysis lanes.

To move an analysis lane, position the mouse over the central dotted line – it will turn to a solid, red line. Click to drag and drop.

To change the width of the analysis lane, position the mouse over the little red square on the left side of the lane – this little square will turn yellow. Click and drag to adjust the width of the lane. 
You can choose to adjust the width of just one analysis lane at a time, or to keep the same width of all analysis lanes. For this, there is a toggle button in the upper right corner, where you can choose “Lane widths: Individual” to change the width of one analysis lane, or “Lane widths: Synced” to keep the same width of all analysis lanes.

If the lane on your image is curved, you can incline or curve the analysis lane to follow the lane on the image.

To incline the analysis lane: The central line has a top and a bottom handle. They are marked as little red squares, and they can be moved left or right to incline the analysis lane according to the lane on your picture. 

To curve the analysis lane:  Double-click on the central line to add extra handles. They will show up as little red squares along the central line, where you double-click. To grab a handle, position the mouse over it, and it will turn yellow. Click to grab and drag the handles on the analysis lane to follow the shape of the lane on the image. You can add multiple handles, but you must move the handle you made before you can add an additional handle.

All actions can be reversed by pressing “Ctrl + z”. 

To remove a handle:  Place the mouse over the handle and check that the little red square changes colour to yellow. Then you can right-click on the handle and choose “Remove handle” from the drop-down menu. The analysis lane will straighten between the remaining handles.

When all the analysis lanes are adjusted according to the picture, you can move on to look at the intensity profile for each lane. 

### Setting the baseline of the intensity profile

The intensity profile of each lane is shown in the right-side panel. Here, it is possible to adjust the position of the baseline. We usually adjust the baseline to follow the dips of the intensity profile.

You can zoom in and out by clicking on the intensity plot and using the scrolling wheel of your mouse. If you want to return to the original view, you can press the A button in the lower left corner of the plot.

To add a handle: Double-click on the baseline, and the handle will appear as a little black square. 

To grab a handle: Click on the window to make sure it is active. Place the mouse over the handle and check that the little black square becomes bold. Then you can click and drag to position it.

To remove a handle:  Place the mouse over the handle and check that the little black square changes to bold. Then you can right-click on the handle and choose “Remove handle” from the drop-down menu.

When you are happy with the position of the baseline in all the intensity profiles, you can move on to the “Measurements” tab.

### Obtaining signal intensity measurements

On the “Measurements” tab, you first add a new measurement. You can either click “Add new measurement” in the upper right corner or click “+ New” in the lower right corner. Next, select the type of measurement that you are doing by double-clicking in the “Type” field and selecting from the drop-down list. In the example shown, we selected Ponceau.

Now, you simply click with the mouse on all the lanes that you want to use for you analysis. The dashed green lines marking the edges of each lane will be highlighted by a solid orange line below, and the intensity value will be shown in the “Measurement Lanes” field below the image. In this field, each measurement is shown with 

*	Its own ID
*	The lane number
*	The value of the intensity
*	Success – tick, if the measurement is successful
*	Comments – if you have any

It is quite common that you do not want to measure the intensity of all the bands in each lane, but rather one or – in the case of protein staining – some of the bands, i.e. you want to specify the height of your analysis lanes. To select the band(s), whose intensity you want to measure, go to the intensity profile for each lane. There are sliders at each end of the profile shown as dashed, yellow dashed lines. Click on the intensity profile to activate the window and position the mouse over the slider – it will turn into a solid, yellow line. Click with the left mouse button and hold it down while adjusting the position of the slider. Notice that the value in Measurement Lanes changes as you adjust the sliders. 

You can choose to adjust the height of just one analysis lane at a time, or to keep the same height of all analysis lanes. For this, there is a toggle button in the upper right corner, where you can choose “Lane height: Individual” to change the height of one analysis lane, or “Lane heights: Synced” to keep the same height of all analysis lanes.

In the example shown, we uploaded two images from the same membrane: In one image, overall protein was stained using Ponceau, and in the other image, the protein of interest was labelled with antibodies. 

After analyzing the overall protein stain intensity in each lane, go back to “Gels” (in the upper left corner) and double-click on the ID of the gel, you are analyzing. 

Double-click on the next image, that you want to analyze. In this example, it is the image with the protein of interest, t-AMPK. 

Adjust to *ROI of the image (see “Defining the region of interest (ROI)”) and analyze this image as before, subtracting the background, marking the lanes for analysis, setting the baseline of the intensity profile and obtaining signal intensity measurements.  

### Esporting the results

To see the results of you analyses, you must export the data. If your results are only on your own computer, and you selected Image source “local” and Database connection “SQLite” under Settings, then your data will be exported as an xlsx file.

Click on “Export” in the lower left corner. You will be prompted to name the file and select a location for your exported data. 
The excel-file has several sheets with the information from the gel analysis software:

*	Gels
*	Measurement types
*	Gel lanes
*	Images
*	Measurement (raw)
*	Reference measurement
*	Measurements (normalized)

For most people, the last sheet with the normalized data will be the most interesting. It shows the intensity measurement values normalized to the reference sample that was defined, when specifying the number of lanes to analyze (see “Image analysis”). If you have more than one reference lane, the values from each lane will be normalized to an average of the values from the reference lanes. 

The normalization is only within one type and within in one gel. Thus, the overall protein stain intensity (in this example by Ponceau, P) is normalized to the protein stain intensity of the reference sample (Pref), i.e. P/Pref. The signal intensity of the protein of interest (S) is normalized to the signal intensity of the reference sample (Sref), i.e. S/Sref.

To analyze the protein of interest, it is common practice to relate its intensity to the overall protein stain intensity of each lane. Thus, you compare S/P between lanes within one image.

However, it is common to have so many samples that you want to compare between images as well. To compare between images, you must calculate S/Sref/P/Pref. 

If you have only a few images to compare, this can easily be done in Excel. However, for larger datasets, we recommend using a database, so these ratios can be calculated in the SQL command to fetch the data.

## Reporting issues

Issues are reported in GitLab. Go to the home page (https://iocbio.gitlab.io/gel/) and follow the link “Issues”. This will take you to GitLab, where you have to register as a user.
In GitLab, under Laboratory of Systems Biology > gel > Issues, press the blue button “New issue”.
Write the title of the issue.
Keep Type as the default, “Issue”.
Write a description of the issue.
Assignee, milestone, and labels do not have to be selected.
Press the blue button “Create issue”.

