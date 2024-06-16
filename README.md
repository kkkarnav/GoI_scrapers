# GoI_scrapers
Set of scrapers to grab political economy data from various GoI sites. Wrote these in the course of research work in Spring and Summer 2024.

### nrega_scraper
Grabs monthly work demand pattern data at the village level from https://nreganarep.nic.in

### nrega_scst_scraper
Grabs generated employment data by category (SC/ST/etc.) at the village level from https://nreganarep.nic.in

### env_clearance_scraper
Downloads basic project information for non-coal mining projects submitted for Environmental Clearance from https://environmentclearance.nic.in/
This script is not as useful as hoped, it fails to download the main page data and can only grab basic project details.

### ec_doc_scraper
Given the static link to each non-coal mining project's main EC page, grabs all PDF documentations for the project uploaded to https://environmentclearance.nic.in/

### ec_parivesh_scraper
Given the proposal number of each non-coal mining project, grab all information about it available at https://parivesh.nic.in/

### ec_form2_parser
Extract useful information from the documents downloaded by doc_scraper, and create a collated dataset on project Environmental Clearances.

### voucher_scraper
Given the district and village codes for each district in a state, grab basic information on all the money paid and receivied by Gram Panchayats under various government schemes, from https://egramswaraj.gov.in/

### voucher_details_scraper
Given the voucher information for each Gram Panchayat payment and receipt, grab its details from https://egramswaraj.gov.in/ and collate a dataset