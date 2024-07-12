# vatservice-gui

User interface for the [vatservice](https://github.com/dseichter/vatservice) written in Python and wx. Use single or batch validation with support for CSV, XLSX and JSON.

## Badges

![pep8](https://github.com/dseichter/vatservice-gui/actions/workflows/pep8.yml/badge.svg)
![trivy](https://github.com/dseichter/vatservice-gui/actions/workflows/trivy.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dseichter_vatservice-gui&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dseichter_vatservice-gui)

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=dseichter_vatservice-gui)

## Start development

Create and activate an environment by running the following command:

```python -m venv .venv```

```.venv/Scripts/activate```

Install the required dependencies

```pip install -r src/requirements.txt```

If you want to do some UI changes, download and install the latest wxFormBuilder from the [wxFormBuilder Homepage](https://github.com/wxFormBuilder/wxFormBuilder).

You can start the vatservice-gui by running the following command:

```python src/vatservice.py```

## Some screenshots

### Single validation

![single validation](images/single.png)

### Batch validation

![batch validation](images/batch.png)

### Configuration

![configuration](images/config.png)