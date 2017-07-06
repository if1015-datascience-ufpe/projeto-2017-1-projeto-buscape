# projeto-2017-1-projeto-buscape
projeto-2017-1-projeto-buscape created by GitHub Classroom

The main purpose os this project is to expose price estimation of mobile phones 
based on their common features like Internal memory size, Camera resolution, Brand and others.

The data behind the analysis was retrieve from Buscapé official site using a web crawler. 
We divided the project in 3 main modules:

- crawler:
  Responsible for retrieve the data from Buscapé official website and output it as a csv file.
  
- server:
  Given the csv file described above, this module process the file and provides a API (HTTP)
  to retrieve the main features, categories and price estimation.
  This module contains two main routes:
  
  /categories -> Returns all main mobile phones categories (memory, hd, camera resolution,...) and index them to integers
  to avoid string comparison. 
  
  /analyse -> Receives the category which should be the base for the price estimation and a vector of coeficients as result.  
  These coefficients are the result of a linear regression of the Data, grouped by the differents sub-groups for
  the given category.
  
  Currently this server is deployed on Google Cloud instances using Flask as web server framework.
  
- webgui:
  Provides a web page where you can interact with the price estimation, choosing one of the main features. 
  To see this webpage just access the /webgui/buscape.html file on your browser (Chrome as preference).
 
