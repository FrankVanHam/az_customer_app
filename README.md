# Example customer app for CI/CD

# Artifacts
The artifacts feed stores universal packages that are used to [deploy](#deploy) the application. Universal packages are either jar's or zip's.  
  
The packages for the customer smallworld products will be build and uploaded during the [build](#build) phase.  
  
The packages for the core product and external products should be uploaded by the administrator and registered in base_artifacts.json in the root directory of the source-code repo.  
Upload the core and external products with code like this:  
<code>az artifacts universal publish --organization https://dev.azure.com/{account}/ --feed {feed} --name cst.jar --version 5.3.61 --description "SW Core installer" --path D:\core_installer.jar --project={project} --scope project</code>

Edit the [base artifacts](base_artifacts.json) file to include all the core and external products that need to be installed for a full deploy. The properties in the json are:

- order: the order in which the product is installed.
- product_path: the relative path to the target directory
- artifact_name: the name of the artifact
- file_name: the file name of the artifact, this need not be the same as the artifact name
- product_type: either "sw-jar" or "zip"
  
Products of type "sw-jar" will be installed with the java installer, products of type "zip" will just be unzipped.  

## Library
In this example you should use two Azure variable groups:
- build-var-group
- deloy-var-group

The follownvg variables are used:
### build-var-group
- AZ_FEED<br>The name of the Azure Artifacts feed you have choosen for your project.
- CUSTOMER_APP_VERSION<br>The version of the customer application the developers are building. This value determines the name of the artifacts that are uploaded after a succesfull build.
- JACOCO_REPORTER_ARTIFACT_NAME: name of the jacoco reporter artifact. Download at (https://github.com/StevenLooman/sw5-jacoco-reporter).
- JACOCO_REPORTER_ARTIFACT_VERSION<br>The version of the artifact in the Artifacts repository.
- JACOCO_REPORTER_JAR<br>The name of the jar file itself. See [converage analysis](#jacoco-converage).
- JACOCO_ARTIFACT_NAME<br>the name of the uploaded artifact of the jacoco jar. Download at (https://www.eclemma.org/jacoco).
- JACOCO_ARTIFACT_VERSION<br>the version of the jacoco artifact in the Artifacts repository.
- JACOCO_ZIP<br>the name of the jacoco zip file. See [converage analysis](#jacoco-converage).
- MAGIK_LINT_ARTIFACT_NAME<br>The name of the magik lint artifact name. Download at (https://github.com/StevenLooman/magik-tools/tree/develop/magik-lint).
- MAGIK_LINT_ARTIFACT_VERSION<br>the version of the magik lint artifact in the Artifacts repository.
- MAGIK_LINT_EXIT_CODE_FAILS<br>The exit codes that determines if the linter will fail the build. Allowed values are 2,4,8 for Critical,Major,Minor. Use comma's to separate multiple values.
- MAGIK_LINT_JAR<br>The name of the jar file of the magik linter. See [linter](#linter).
- MUNIT_TEST_ASPECTS<br>The test aspects to test after building the code. Use comma's to separate multiple values. See [MUnit](#munit).
- SW_CORE_DIR<br>The name of the Core directory as a relative path name. This name should match the directory name as specified in the [base artifacts](base_artifacts.json) file.
- SW_VERSION<br>The Smallworld version of the core products that are uploaded to the Artifacts.

## deploy-var-group
- AZ_FEED<br>The name of the Azure Artifacts feed you have choosen for your project.
- CUSTOMER_APP_VERSION<br>The version of the customer application the developers are building. This value determines the name of the artifacts that are downloaded to deploy the application. Note: it determines the **name**, not the **version**.
- DEPLOY_DIR<br>The deployment directory on the target machine.

## Build

## Deploy

## Linter

## MUnit

## Jacoco converage
