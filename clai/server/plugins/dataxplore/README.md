# DataXplore

`Data-Analytics` `NLP` `Support` `Plots`

Data Exploration is one of the well versed topics in the course of Data Analyst/ Scientist and Researcher. For a given data based modeling, one needs to know a) What are the attribute one is looking b) how the attribute can be used for top level analysis. DataXplore Plugin in Project (CLAI) Command Line AI implements few primary tasks on the command line including visualization on a certain terminal. A goto plugin like dataxplore comes handy for myriad of data analysis task for the above effort. 

## Implementation

Command usage:- clai dataxplore function csvfilelocation
e.g. 
1) `>> clai dataxplore summarize air_quality.csv`, when this command is executed one can view the summary of the give data file. 
2) `>> clai dataxplore plot air_quality.csv`, when this command is executed one can view the plot of the given data file. 
#### Execution on test dataset.
![figure1](https://github.com/madhavanpallan/clai/blob/master/clai/server/plugins/dataxplore/figures/dx_summarize_plot_test.png) 
#### Execution on air quality dataset.
![figure2](https://github.com/madhavanpallan/clai/blob/master/clai/server/plugins/dataxplore/figures/dx_summarize_plot_airQuality.png)

*** Both dataset are courtesy from the [pandas](http://pandas.pydata.org/) website.
## [xkcd](https://uni.xkcd.com/)
The contents of any one panel are dependent on the contents of every panel including itself. The graph of panel dependencies is complete and bidirectional, and each node has a loop. The mouseover text has two hundred and forty-two characters.

![alt text](https://imgs.xkcd.com/comics/self_description.png "The contents of any one panel are dependent on the contents of every panel including itself. The graph of panel dependencies is complete and bidirectional, and each node has a loop. The mouseover text has two hundred and forty-two characters.")
