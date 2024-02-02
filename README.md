# Running Instructions

First, you must create a `.env` file and add your OpenAI API key. You can use the `template.env` as a reference.

You can run the application by first downloading Docker and using the command `docker compose up --build`. There are two components to the app, the front-end which you can find at `http://localhost:3000/`, and the backend. Navigate to the URL, and upload a `.txt` file, such as `test_file.txt`. In a few seconds, or longer if you've uploaded a larger file, you will see the summary of your document. 


# Potential Improvements

Due to this application just being a POC, many components of it are simplistic. For example, the chunking technique to reduce a large document into smaller, important chunks is done if the document length exceeds an arbitrary word count. An improvement would be to use token counts, and quantitivate metrics to determine when this necessary. Further, the chunking mechanism is quite simple. The API logic is also not concurrent, so if multiple users upload documents it will take a while to complete. 