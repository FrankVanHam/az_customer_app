# Artifacts
The artifacts feed stores universal packages that are used to [deploy](#deploy) the application. Universal packages are either jar's or zip's.  
  
The packages for the customer smallworld products will be build and uploaded during the [build](#build) phase.  
  
The packages for the core product and external products should be uploaded by the administrator and registered in base_artifacts.json in the root directory of the source-code repo.  
Upload the core and external products with code like this:  
<code>az artifacts universal publish --organization https://dev.azure.com/{account}/ --feed {feed} --name cst.jar --version 5.3.61 --description "SW Core installer" --path D:\core_installer.jar --project={project} --scope project</code>

Edit the [base artifacts](../base_artifacts.json) file to include all the core and external products that need to be installed for a full deploy. The properties in the json are:

- order: the order in which the product is installed.
- product_path: the relative path to the target directory
- artifact_name: the name of the artifact
- file_name: the file name of the artifact, this need not be the same as the artifact name
- product_type: either "sw-jar" or "zip"
  
Products of type "sw-jar" will be installed with the java installer, products of type "zip" will just be unzipped.  
