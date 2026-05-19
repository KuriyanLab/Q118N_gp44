# Q118N_gp44
These scripts and files for data analysis of Q118N mutation in T4 Clamp loader. It also has ProteinMPNN designs that were used. Apart from this it also contains Protein Frustration Analysis of Clamp loader

1. There are Excel  and CSV files with variant counts and enrichment values for different experiments. The color "green" indicates variant is from "Active template" and "Red" indicated "Inactive Template." Counts for all the replicates are present here. Please look at files names and sheet names.

  
2. Python files are reprevstative file. They have to be modified for different eperiments according to columns, replicates, SD, etc.
   This script processes replicate enrichment data from Excel files and generates histograms comparing Active and Inactive template populations for WT and D86H datasets.

The workflow begins by loading two Excel files containing replicate enrichment measurements (Enc_1–Enc_5). Each row is classified as either “Active” or “Inactive” by reading the fill color of a specified Excel column using openpyxl. Green-colored cells are labeled as Active, while red-colored cells are labeled as Inactive.

After loading the data, the script performs several quality-control filtering steps:

   * Rows containing missing replicate values are removed
   * The standard deviation across replicate enrichment measurements is calculated for each row
   * Rows with replicate standard deviation greater than a defined threshold (MAX_ROW_STD) are excluded to remove noisy or inconsistent measurements

      
3. ".fa" files contains ProteinMPNN generated output for different design conditions.
4. Only configurationa output from Frustration analysis is present. We have not used mutational frustration in our analysis
