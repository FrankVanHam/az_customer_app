## Library
In this example you should use two Azure variable groups:
- build-var-group
- deloy-var-group

The follownvg variables are used:
### build-var-group
- AZ_FEED<br>The name of the Azure Artifacts feed you have choosen for your project.
- CUSTOMER_APP_VERSION<br>The version of the customer application the developers are building. This value determines the name of the artifacts that are uploaded after a succesfull build.
- JACOCO_REPORTER_ARTIFACT_NAME: name of the jacoco reporter artifact. Download at [jacoco-reporter](https://github.com/StevenLooman/sw5-jacoco-reporter).
- JACOCO_REPORTER_ARTIFACT_VERSION<br>The version of the artifact in the Artifacts repository.
- JACOCO_REPORTER_JAR<br>The name of the jar file itself. See [converage analysis](#jacoco-converage).
- JACOCO_ARTIFACT_NAME<br>the name of the uploaded artifact of the jacoco jar. Download at (https://www.eclemma.org/jacoco).
- JACOCO_ARTIFACT_VERSION<br>the version of the jacoco artifact in the Artifacts repository.
- JACOCO_ZIP<br>the name of the jacoco zip file. See [converage analysis](#jacoco-converage).
- MAGIK_LINT_ARTIFACT_NAME<br>The name of the magik lint artifact name. Download at [magik-lint](https://github.com/StevenLooman/magik-tools/tree/develop/magik-lint).
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
