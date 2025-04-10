# query_GLIS_API
Python functions to query FAO GLIS API (url = "https://glis.fao.org/glisapi/v1/pgrfas?")

These are functions to call the GLIS API and fetch data regarding the DOI registration (date) and MLS status for each accession registered

Function call_glis_API takes the INSTCODE of the genebank conserving the material and returns the result of the API call as list (results_API_call)

Function make_estimate takes the results_API_call and the desired year and returns a Pandas dataframe with columns with the year that DOI was registered, boolean values for DOI registered and inclusion in MLS for the desired year.  
