# NLP-Demo-Template (Multi Services)
A frontend-backend separation model and web application template

## Goal
We aim to provide guidance on how to design and fire up a NLP demos that requests calling other services.

## Pros
This demo template is more secure, as we do not expose our servcie url in our files, preventing other people from recursively calling the services and causing shutdowns.

## Cons
It takes more time to generate results, as the annotations are made in other ports. In addition, retrieving annotation results is asynchronous, so we may need to rearrange the result from POST requests after we receive them.
