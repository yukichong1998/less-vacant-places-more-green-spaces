## Project - Deliverable \# 1 Feedback 
 
The goal of our project is to map the locations of green spaces and create a visual representation of the relationship between availability of green spaces and a composite public health indicator across zip codes in Chicago. Based on the recent movement towards converting unused land into parks and green spaces, we also intend to make this project a tool for policymakers to identify vacant lots that can potentially be converted into green spaces. Hence, we will also map the locations of vacant lots.

I pretty much already gave you feedback on the approval of the project. I think it's a great idea overall. Here's some feedback on thinking about the structure: 

1. One person should be in charge of handling the visualization component. Based on your project I would recommend these potential packages:

https://betterprogramming.pub/7-must-try-data-visualization-libraries-in-python-fd0fe76e08a0 

Actually 1-6 have been used by many different groups over the years. I would look them over and choose the one that works best for what you are trying to produce. Maybe Geoplotlib is what you are looking for in this case. 

2. One person should be in charge of cleaning and wrangling the data once you receive it. 

3. One person should be in charge of scraping/gathering the data. 

4. One person should be in charge of handling what needs to be displayed based on the metrics the user has filtered on. The key here is to seperate out the visual aspect and the code for performing the analysis on what to actually show. I think Geopotlib will be best for handling the situation. 

The actual code structure and how the components are connected is what I will be grading you on so I want you to first determine what you think is the best method and I'll provide some additional help in Week 7. 


*Grade*: 10/10 