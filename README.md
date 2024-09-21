# GoI_scrapers
Set of scrapers to grab political economy data from various GoI sites. Wrote these in the course of research work in Spring and Summer 2024.


### / (analysis)

 - ##### ec_dataset.Rmd
     - As part of an upcoming research paper, collate and analyse a dataset of industrial projects across India and their environmental clearance processes
 - ##### voucher_analysis.Rmd
     - As part of an upcoming research paper, collate and analyse a dataset of income and expenditure of Gram Panchayats across Orissa

### nrega/ (from https://nreganarep.nic.in)

 - ##### nrega_scraper
     - Grabs monthly work demand data at the village level
 - ### nrega_scst_scraper
     - Grabs generated employment data by category (SC/ST/etc.) at the village level

### parivesh/ (from https://environmentclearance.nic.in & https://parivesh.nic.in)

 - ##### env_clearance_scraper
     - Downloads basic project information for non-coal mining projects submitted for governmental environmental clearance
     - Note: This script is not as useful as hoped, it often fails to download the main page data and can only grab basic project details.
 - ##### ec_doc_scraper
     - Given the static link to each mining project's main EC page, grabs all PDF documentations for the project
 - ##### ec_parivesh_scraper
     - Given the proposal number of each non-coal mining project, grab all available information about it at the new governmental portal
 - ##### ec_form2_parser
     - Extract useful information from the documents downloaded by doc_scraper, and create a collated dataset on project Environmental Clearances.
 - ##### ec_kml_scraper
     - Extract information on and download Google Earth KML files for the collated Environmental Clearance projects.

### egramswaraj/ (from https://egramswaraj.gov.in)

 - ##### voucher_scraper
     - Given the district and village codes for each district in a state, grab basic information on all the money paid and receivied by Gram Panchayats under various government schemes
 - ##### voucher_details_scraper
     - Given the voucher information for each Gram Panchayat payment and receipt, grab its bank, particulars, etc. details from and collate a dataset

### copernicus/ (from https://human-settlement.emergency.copernicus.eu)

 - ##### copernicus_merge
     - Given raster grids downloaded from Copernicus, merge them into the area of study
 - ##### copernicus_visualize
     - Parse, process and visualize the merged GHS raster files
 - ##### copernicus_extract
     - Given a merged raster, extract the GHS values into an overlapping shapefile
 - ##### copernicus_ulb
     - Given a merged raster, extract the GHS values into an overlapping cities and towns shapefile
 - ##### copernicus_vector_visualize
     - Given a populated GHS shapefile, process and visualize the district/subdistrict/ULB polygons
  
### ULB/

 - ##### ulb_budgets
     - Take a series of PDF files containing municipal (urban local body) budget and expenditure data for each year and extract the topline amounts for the year into a csv
 - ##### ulb_ghsl_correlate
     - Merge the ULB budget data and the GHSL Copernicus data for Odisha to correlate whether higher municipal budgets are linked with higher growth (~no)

### SECC/

 - ##### name_classifiers
     - Classifiers to assign gender/caste/tribe values to Indian names
