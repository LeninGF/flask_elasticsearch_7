## English:
This is a flask project that allows to test some functionalities of the **Elasticsearch** in **Python**.
### The project:
To run the project, please install elasticsearch (ES) for python in a conda environment, activate it and execute:

    conda install -c conda-forge elasticsearch
    conda activate bigdataenv
    python app.py
    
The project has 7 html pages:
* indexing_demo: Here, you input the index name and the document type. This page extracts
the contents from swapi.co and stores it.
* insert_demo: This html allows to input some data in an index and document type. If the 
index does not exist, it is created.
* read_demo: This html allows to retrieve the information stored of a specific **id** in an **index**
* update_demo: allows to change the information of a specific **id** in an **index**
* delete_index and delete_document: permit to delete an existing index and an existing document, respectively

## Español:
Este proyecto de flask permite probar algunas funcionalidades de **Elasticsearch** en **Python**.
### El proyecto:
Para correr el proyecto, por favor instalar elasticsearch (ES) para python en un entorno de conda, activarlo y ejecutar:

    conda install -c conda-forge elasticsearch
    conda activate bigdataenv
    python app.py
    
El proyecto tiene 7 páginas html:
* indexing_demo: Ingresa el nombre del index y el tipo de documento. Esta página extrae contenidos desde 
swapi.co y los almacena.
* insert_demo: permite ingresar datos en un index y tipo de documento. Si el index no existe, es entonces creado.
* read_demo: permite recuperar la información almacenada en un **id** de un **index**
* update_demo: permite modificar la información de un**id** específico en un **index**
* delete_index and delete_document: permite eliminar un index existente y un documento existente, respectivamente.


