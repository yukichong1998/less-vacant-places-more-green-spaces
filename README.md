Project Installation:
1. Clone the repo to your local hard drive (or server):
```
git clone https://github.com/uchicago-CAPP30122-win-2022/proj-less-parking-more-parks
```

2. Go to the cloned repository:
```
cd ./proj-less-parking-more-parks
```

3. Install the virtual environment:
```
bash install.sh
```

4. Activate the virtual environment:
```
source env/bin/activate
```

5. Run the program:
```
bash run_program.sh
```

6. Go to the returned address in a web browser:
Example: “Dash is running on http://127.0.0.1:8053/”

7. To exit Dash: "ctrl + c"

8. To exit virtual environment "deactivate"

9. (Optional) Generate the input data files:
```
cd dashboard_app/data_prep
python3 data_extraction.py
```

Project Interaction:
1. Choose a parameter from the drop down to display on the choropleth map. If "Health Risk Score" is selected, the user may choose at least two health indicators to be included in the computation of the composite health risk score.
2. Choose a neighborhood from the drop down to display on the scatterplot map.
3. Choose a 2nd neighborbood from the drop down to create bar charts comparing the 2 selected neighborhoods.

