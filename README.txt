This is a Django project that visualizes data for the Cold Chain.

It is currently set up to show the monthly volume of vaccine deliveries to various regions and districts in Tanzania based on 2012 DVDMT data. 

Cloning the directory locally and running 'python manage.py runserver' from the directory should start a development server and bring up the site at 127.0.0.1:8000/barchart/

For a quick look at what the initial version looks like at the top level, there is a screenshot in the barchart/ directory.

*Note: the Django project is unfortunately named 'barchart' due to lack of foresight

This visualization is based on an example from Mike Bostok's d3 repository, which can be found here: http://mbostock.github.io/d3/talk/20111018/treemap.html

Important files in structure:

barchart/static/barchart/pqs.csv:

This holds information about PQS models from PATH's total cost of ownership calculations.
It's structure is: Type, Cost/Liter, Capacity, Energy Cost, MaintCost
Energy cost and maintenance costs are annual.

barchart/static/barchart/DistrictInfo.csv:

Information from Tanzania's 2012 DVD-MT file, including population, births, total vaccine volume,
and capacity requirements.

barchart/parser.py: 

Reads input from above csv files to generate json objects that can be used by the d3
visualizations. Uses an algorithm I wrote to assign PQS models to districts; simply a greedy
algorithm that minimizes the number of refrigerators used in the district. The algorithm is 
not optimal in the sense that it does not minimize the cost of refrigeration.

barchart/templates/treemap.html

The d3 visualization code is contained here. It is largely based on the zoomable treemap
visualization from Mike Bostok. It provides multiple options for visualization using a 
dropdown list that repopulates the treemap when changed.


Things to improve for future work:

Allow for a user of the visualization to change the refrigerators used by the districts to 
see how it impacts outcomes. This would be executed by making each district selectable and 
showing data on which PQS models are used there, and then making it possible to change any 
of those models and repopulate the treemap.

Make sure to truncate the values in cost/birth.

Use a legend for better aesthetics.
