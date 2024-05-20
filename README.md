# JeremyHuntsman.com Server Process API

This api is to serve as the entry point to the backend of my server architecture.  

Currently, the idea is to have this handle authentication, provide enpoints to all my public facing applications,
and insulate the more critical modules and components. 

This is mostly unnecessary considering the use cases of my personal projects, but 
the intent is to get practice and experience using enterprise standards.  This also 
allows my architecture to be extremely robust, stable, and scalable. 

Currently this layer will handle all api requests; Producing events to kafka for my 
service apis to consume and handle.  A performant database solution will be in place to "cache" data for data fetching
from my front end, and maintain the asynchronous flow I have planned. 


I will update more when I have more of it built!
