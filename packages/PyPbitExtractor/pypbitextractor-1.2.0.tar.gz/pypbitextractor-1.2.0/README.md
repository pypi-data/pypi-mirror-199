## ✔ Power BI Automation Using Open AI API
### Problem Statement:
- Power BI documentation is essential for maintaining the accuracy and integrity of data models, ensuring compliance with regulations, and improving collaboration and efficiency across teams. 
- It is a time-consuming task that requires more human intervention and is highly error prone. 
- Our model aims to automate this process using OpenAI's NLP capabilities. 
		
****

### Purpose:
- The purpose of our Power BI model documentation automation is to provide a Time-saving and Accurate solution for fetching pbix details. Below are the purpose that our model is fulfilling:
    - Automating the Power BI model documenter using one of the most efficient GPT-3 architecture i.e. `text-davinci-002`.
    - Fetched the `Measures`, `Source Information`, and `Model Relationships` attributes from the Power BI report.
    - Wrote back the Measures and Modification Descriptions and displayed on hovering the respective properties in updated pbit files.
    - Presented the output into three directories, namely `EXCEL`, `JSON` and `Updated PBIT`.

****

### Input/Output Deliverables:
```
- Input: 
    - Single File
    - Multiple Files
    - A Folder

- Output:
    - Excel Directory
    - JSON Directory
    - Updated PBIT Directory
```

****

### Features:
- Implemented following features in our model:
    1.	Features in JSON Deliverables:
        - `DataModelSchema Generation`: Generated the datamodelschema file for the respective pbit file and stored it in JSON format.

    2.	Features in EXCEL Deliverables:
        - `Measure Sheet`:
            - Measure Name
            - Measure Expression
            - Measure Data Type
            - Measure Description
        - `Source Information Sheet`:
            - Table No
            - Table Name
            - Table Mode
            - Table Type
            - Table Source
            - Original Table Name
            - Table Query
            - Modification
            - Modification Description
        - `Relationships Sheet`:
            - From Table
            - From Column
            - To Table
            - To Column
            - State
            - Direction
            - Cardinality

    3.	Features in UPDATED PBIT Deliverables:
        - `Dynamic Hover Description`: Made the Measures and Modifications Description to hover on each respective properties.

****

### Prerequisites:
- In order to use this script, one need to ensure to met the following requirements:
    - A Power BI Desktop installation (version - 2.115.663.0 64-bit).
    - A valid API secret key for OpenAI's NLP capabilities.
    - Python 3.7 or later installed on your machine.
    - Access to the Power BI models that you want to document.

****
****

## ✔ Package Description
### PyPbitExtractor
    - Created a python package for the given python script and published it on https://pypi.org/

### Package Usage
```
- from PyPbitExtractor import Extractor
    - This command will install all the uninstalled required libraries used in script.
- Extractor.api()
    - This command will prompt user for Open API Secret Key.
- Extractor.main()
    - This will prompt user for input of file selection and thereafter the repective file/folder.
```

### Package Installation
```bash
pip install PyPbitExtractor
```