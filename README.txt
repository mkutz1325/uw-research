This is a Django project that visualizes data for the Cold Chain.

It is currently set up to show the monthly volume of vaccine deliveries to various regions and districts in Tanzania based on 2012 DVDMT data. 

Cloning the directory locally and running 'python manage.py runserver' from the directory should start a development server and bring up the site at 127.0.0.1:8000/barchart/

*Note: the Django is unfortunately named 'barchart' due to lack of foresight

First few things to improve:

-Labeling of regions. They are currently split by color, but it is not possible to tell which region is 'Region 1' or 'Region 3'.

-Labeling actual percentages and units. It gives an idea of how the proportions break down, but shouldn't leave the user guessing.

-Add an option for actual energy consumption in the drop-down list at the bottom of the page, and base it on the volume of vaccines that are delivered using a rough model that will be developed.
