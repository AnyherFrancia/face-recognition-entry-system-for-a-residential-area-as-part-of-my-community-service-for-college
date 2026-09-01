# face-recognition-entry-system-for-a-residential-area-as-part-of-my-community-service-for-college
The project is still being made as I'm waiting for testing from the residents.

This software was made as a way for me to practice more serious coding skills that could teach me a better understanding of the connection between databases and software, using postgresql and python. CustomTkinter was used for the ui as I wasn't preoccupied with the visuals more so with the backend.

The project is capable of creating new users and deleting, editing and recovering them by their id, I chose to encode the users photos to base64 before saving them to postgresql as a text so they wouldn't become a space liability eventually, the face encodings, however, are save as a multi-dimensional vector that uses a HNSW algorithm supported by cosine operations to calculate the similarity between them with an error margin to ensure good results. 

The database is only one table, I have created more complex databases in fourth and fifth normal form for other college projects but I felt that since the software didn't need to make any real distinction between owners, a first normal form was enough.  
