# Basic Well Log Interpretaion - Jupyter Notebook
Original code : https://github.com/petroGG/Basic-Well-Log-Interpretation/tree/master<br>
Further developed by **Afgha Izzam Tursina**, **Pahala Dominicus Sinurat, S.T, M.Sc., Ph.D.,** and **Formation Evaluation Research Team** (2022/2023)

In this Modified Version of Basic Well Log Interpretation (BWLI). There are 11 sections in jupyter notebook file (.ipynb), namely:
1. Change the LAS Format into one dataframe, column name adjustment, filter relevant data to keep.

2. Function for Data Distribution Plot
In this section, functions to show data distribution are created, namely boxplot, density plot, and histogram. These three functions are called if we need plotting to see the distribution of data.

3. Outlier Handling
In this section, dataframes containing combined dataframes are analyzed and outliers are handled. Outlier handling is carried out with isolation forest followed by interpolation. Please be careful with this part! This is because the missing value in the LAS file is written as -999.25. So, -999.25 needs to be handled by defining it as a mean, medium, zero, NaN value, or other value. At the end of the section, we will save the data that has been handled as clean data in TXT format.

4. Data Selection, Normalization, Well Selection, and Input Core Parameters for Selected Well
In this section, data that has undergone outlier handling is then selected. The data will be normalized. Next, for log analysis, one of the wells needs to be determined. Once determined, if it exists, core data for porosity and permeability can be determined or if it doesn't exist you can use dummy data with numpy.

5. Display Log Data
In this section, the well log data will display all depths and selected depths.

6. Clay Volume Calculation
Look at jupyter notebook.

7. Porosity Calculation
Look at jupyter notebook.

8. Water Saturation Calculation
Look at jupyter notebook (SWarchie, SWwaxman, SWindonesia, & SWsimandoux).

9. Permeability Calculation
Look at jupyter notebook.

10. Display the Interpretation Plot
Look at jupyter notebook.

11. Other
In this section, a crossplot is displayed

Specifically in this case, the well data used is LL-4. After the two well data are combined and outlier handling is carried out, the clean data used is data_clean_NaN, although other types of clean data can actually be used.

Clean data is data resulting from processing from section 1 to section 3 in the Jupyter notebook. For now, there are four types of clean data as follows:
1. data_clean_NaN = -999.25 is defined as a NaN value and no outlier handling is carried out
2. data_clean initialize mean = -999.25 defined as NaN value, NaN value replaced with mean, and outlier handling performed
3. data_clean initialize median = -999.25 defined as NaN value, NaN value replaced with median, and outlier handling performed
4. data_clean initialize zero = -999.25 is defined as NaN value, NaN value is replaced with 0, and outlier handling is performed

## Clone this repository into your local machine:
1. Download & install git
2. Open terminal or CMD if ur using windows
3. go to your desired Directories
4. type & run this :`git clone https://github.com/waksun0x00/BWLI-modified.git`
5. install python dependencies
6. run BWLI-modified.ipynb

Thanks
