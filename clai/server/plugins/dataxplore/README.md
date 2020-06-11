# dataXplore

`Analytics` `NLP` `Support`

Data science has become one of the most popular real-world applications of ML. This skills is targeted specifically 
toward making the CLI easier to adopt and navigate for data scientists.

## Implementation

The current version of the skill provides two functionalities: **summarize** and **plot**. 
"Summarize" utilizes the [describe function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html) of the popular 
[Pandas library](https://pandas.pydata.org/pandas-docs/stable/index.html) to 
generate a human-readable summary of a specified CSV file; this functionality is intended to allow data scientists
to quickly examine any data file right from the command line. "Plot" builds on the plot function provided by 
[MatPlotLib](https://ieeexplore.ieee.org/document/4160265), 
and the Pillow library [[link](https://pillow.readthedocs.io/en/stable/index.html)] 
[[link](https://www.pythonware.com/products/pil/)] 
to generate a plot of a given CSV file. Such functionalities illustrate basic use cases
of how CLAI can be used as a CLI assistant for data science.

## Example Usage

`>> clai "dataxplore" summarize air_quality.csv` to view the summary of the give data file. 

`>> clai "dataxplore" plot air_quality.csv` to view a plot of the given data file. 

![figure1](https://www.dropbox.com/s/lin379uw2nc0ts9/dx_summarize_plot_test.png?raw=1) 

![figure2](https://www.dropbox.com/s/j4xxme9eaj92mh5/dx_summarize_plot_airQuality.png?raw=1)

Both dataset are courtesy of [pandas](http://pandas.pydata.org/).

## [xkcd](https://uni.xkcd.com/)
The contents of any one panel are dependent on the contents of every panel including itself. The graph of panel dependencies is complete and bidirectional, and each node has a loop. The mouseover text has two hundred and forty-two characters.

![alt text](https://imgs.xkcd.com/comics/self_description.png "The contents of any one panel are dependent on the contents of every panel including itself. The graph of panel dependencies is complete and bidirectional, and each node has a loop. The mouseover text has two hundred and forty-two characters.")
