
# AI progect for ATOM

  

This repository implements an API to automate the verification of requirements in a certified circuit.

  

To start the project, you need:

* Download the repository
* Install the necessary libraries ( list is in the file requirements.txt )

* change the api key instead of the asterics`openal.api_key = "***"` insert your key from Open AI in the file `utils.py`

* Run the file `app.py`

  

## Short description of the project files:

├── .idea <- folder for PyCharm

├── .venv <- folder virtual environment

├── regulations <- sample regulations folder

├── uploads <- folder to store incoming files for processing

├── `app.py`<- main file

│ │`function`

│ ├── upload_file <- Asynchronous handler that processes incoming files

│ └── check_text <- Asynchronous handler that processes incoming text

├── `requirements.txt` <- list of required libraries

└── `utils.py` <- basic functions file

---│ `function`

---├── extract_text_from_docx<-Function for extracting text from .docx files

---├── extract_text_from_pdf<-Function for extracting text from .pdf files

---├── extract_text_from_xlsx<-Function for extracting text from .xlsx files

---└── check_compliance_with_regulations<-Function for checking compliance with regulations using GPT-4o



--------
