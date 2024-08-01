# GoI_scrapers
Set of scrapers to grab political economy data from various GoI sites. Wrote these in the course of research work in Spring and Summer 2024.

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
