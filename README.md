# Example customer Smallworld app for CI/CD
This repository contains an example Smallworld customer application that can be build and deployed with Azure pipelines. The assumption is that the core application is structured like this:  
![Directory structure](/img/directory-structure.jpg)

|file/dir|content|
|--------|-------|
|az_customer_app|Your customer smallworld application. The git repository |
|az_customer_app\customer_engine_prd|The smallworld engine application providing support for the GUI|
|az_customer_app\customer_prd|The smallworld GUI application|
|az_customer_app\pipeline|The pipeline yaml and scripts|
|az_customer_app\run|The batch files to run the applications|
|az_customer_app\smallworld_registry|The smallworld registry that registers the location of the products relative to the Smallworld product|
|az_customer_app\.gitignore|.gitignore|
|az_customer_app\artifacts.json|configuration of the customer smallworld products|
|az_customer_app\base_artifacts.json|configuration of the Smallworld products and external products|
|az_customer_app\README.md|this file|
|SW|The Smallworld core products|
|SW-external|Any external products|
|Emacs.bat|Emacs|
|run.bat|The main batch file to start the application|
|set_base_dir.bat|The redirection batch file that will point to the latest deployment|

The application is a simple application based on the Cambridge application that adds a menu item that prints a message on the prompt. The application is obviously not the point of this repository, the building and deploying is...

# Set it up from scratch
My assumption is that you know how Azure DevOps works, so this tutorial is about what to do, not how to do it.

## Create project
1. In Azure DevOps create a new project SW-APP
2. Import this Git repository (or a clone) into the project.

## Create Variable groups
In the Library tab under the Pipelines tab add 2 Variable groups. The variables will name the names and versions of the artifacts that will uploaded later.
Name them build-var-group and deploy_var_group. The names must match the names in the [azure-build.yml](./pipeline/azure-build.yml) and [azure-deploy.yml](./pipeline/azure-deploy.yml) files in the "variables:" section.

For build_var-group enter the following values. See [library](/md/library.md) for details.   
|variable|value|
|--------|-----|
|AZ_FEED|sw_feed|
|CUSTOMER_APP_VERSION|1|
|JACOCO_ARTIFACT_NAME|jacoco.zip|
|JACOCO_ARTIFACT_VERSION|0.8.14|
|JACOCO_REPORTER_ARTIFACT_NAME|sw5-jacoco-reporter.jar|
|JACOCO_REPORTER_ARTIFACT_VERSION|2.2.1|
|JACOCO_REPORTER_JAR|sw5-jacoco-reporter.jar|
|JACOCO_ZIP|jacoco.zip|
|MAGIK_LINT_ARTIFACT_NAME|magik-lint.jar|
|MAGIK_LINT_ARTIFACT_VERSION|0.11.0|
|MAGIK_LINT_EXIT_CODE_FAILS|2|
|MAGIK_LINT_JAR|magik-lint-0.11.0.jar|
|MUNIT_TEST_ASPECTS|az_build_pipeline|
|SW_CORE_DIR|SW|
|SW_VERSION|5.3.61|

For deploy_var-group enter the following values. See [library](/md/library.md) for details.   
|variable|value|
|--------|-----|
|AZ_FEED|sw_feed|
|CUSTOMER_APP_VERSION|1|
|DEPLOY_DIR|C:\SW-App|
|SW_VERSION|5.3.61|

## Upload artifacts
In the Artifacts tab create a new Feed. 
* Name it "sw_feed", just as was specified in the var-groups in the yaml files.
* No upstream sources
* Scope is the project
* Set the retention policy as you require

Now we need to upload the artifacts.
### upload Smallworld core
Download the Smallworld core components for CST 5.3.6.1 (CST-5.3.6.1.ISO) and Translator 5.3.6.1 (TRANS-5.3.6.1.ISO). Extract the jar file from the ISOs. Upload the jar files with the names specified in the configuration [base_artifacts.json](./base_artifacts.json) and the version 5.3.61 as specifified in the var-group.   
```
az artifacts universal publish --organization https://dev.azure.com/frnkvnhm/ --feed sw_feed --name cst.jar --version 5.3.61 --description "SW Core installer" --path D:\dev\uploads\core_installer.jar --project="SW-APP" --scope project
{- Publishing ..
  "Description": "SW Core installer",
  "ManifestId": "6AA908902101D6766DF21A657C15E8B01153D6124C2F7AA63A44070B5B14B22A01",
  "SuperRootId": "FC44FD8AA5084C1AC509388DB91B8015198CE753E3574BC3A359A617D02C5D6302",
  "Version": "5.3.61"
}
```
and
```
az artifacts universal publish --organization https://dev.azure.com/frnkvnhm/ --feed sw_feed --name trans.jar --version 5.3.61 --description "SW Translator installer" --path D:\dev\uploads\translators_installer.jar --project="SW-APP" --scope project
{- Publishing ..
  "Description": "SW Translator installer",
  "ManifestId": "497AAF054EE74D479C50FC1CFDBD67E6D8D80A5C5DE1C178E028DCBC6E70F39701",
  "SuperRootId": "267EF85096F9302BE2F25DCA81339396E59D1DF9FCD2F5B1EA53B77C079032CA02",
  "Version": "5.3.61"
}
```

### MUnit
Dowload mUnit from https://github.com/OpenSmallworld/munit as munit.zip. Also rename the internal directory in the zip to 'munit' because you really dont want to have the version name in the product.   
Upload the zip to the Artifact with the artifact name specified in the configuration [base_artifacts.json](./base_artifacts.json) and the version 5.3.61 as specifified in the var-group. 
```
az artifacts universal publish --organization https://dev.azure.com/frnkvnhm/ --feed sw_feed --name munit.zip --version 5.3.61 --description "MUnit" --path D:\dev\uploads\munit.zip --project="SW-APP" --scope project
```

### Jacoco
Download the code coverage tool at (https://www.eclemma.org/jacoco) as jacoco.zip.   
Upload the zip to the Artifact with the name and version as specifified in the var-group.   
```
az artifacts universal publish --organization https://dev.azure.com/frnkvnhm/ --feed sw_feed --name jacoco.zip --version 0.8.14 --description "Jacoco" --path D:\dev\uploads\jacoco.zip --project="SW-APP" --scope project
```

### Jacoco reported
Download the Jacoco reporter tool at [jacoco-reporter](https://github.com/StevenLooman/sw5-jacoco-reporter) as jacoco-reporter.jar.   
Upload the jar to the Artifact with the name and version as specifified in the var-group.   
```
az artifacts universal publish --organization https://dev.azure.com/frnkvnhm/ --feed sw_feed --name "jacoco-reporter.jar" --version 2.2.1 --description "Jacoco reporter" --path "D:\dev\uploads\jacoco-reporter.jar" --project="SW-APP" --scope project
```


### Magik-linter
Download the linter at [magik-lint](https://github.com/StevenLooman/magik-tools/tree/develop/magik-lint) as magik-lint.jar.
Upload the jar to the Artifact with the name and version as specifified in the var-group.   
```
az artifacts universal publish --organization https://dev.azure.com/frnkvnhm/ --feed sw_feed --name "magik-lint.jar" --version 0.11.0 --description "Magik linter" --path "D:\dev\uploads\magik-lint.jar" --project="SW-APP" --scope project
```

[Artifacts](md/artifacts.md)  
[Library](md/library.md)

## Build

## Deploy

## Linter

## MUnit

## Jacoco converage
