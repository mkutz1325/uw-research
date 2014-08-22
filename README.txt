This is a Django project that visualizes data for the Cold Chain.

It is currently set up to show the monthly volume of vaccine deliveries to various regions and districts in Tanzania based on 2012 DVDMT data. 

Cloning the directory locally and running 'python manage.py runserver' from the directory should start a development server and bring up the site at 127.0.0.1:8000/barchart/

For a quick look at what the initial version looks like at the top level, there is a screenshot in the barchart/ directory.

*Note: the Django project is unfortunately named 'barchart' due to lack of foresight

This visualization is based on an example from Mike Bostok's d3 repository, which can be found here: http://mbostock.github.io/d3/talk/20111018/treemap.html
