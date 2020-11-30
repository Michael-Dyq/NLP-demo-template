# Back End Design

## Things to Modify for Your Demo

Unlike simple single-service demo, we do not generate the annotation results in this service. Instead, our front end will call other services with its back end server. This allows us to hide the annotation urls and incorporate multiple annotation services from distinct sources. The [frontend_backend.py](To be Update for Final Version) is responsible for hosting the HTML file and send post request to the services for the responses. Generally, the root path should host our html files, and each other path can be assign to a service. For instance, if you wish to fetch the annotation result for PoS tagging, you can directly send the request to '/pos' and the backend service will forward the request to the backend of the PoS tagging service. In other words, the '/pos' path serves as a middleware.

### HTML

The HTML file [index.html](To be Update for Final Version) controls the static elements of the page, and it generates a overall HTML DOM structure. Currently our HTML file contain a language option for multilingual models, but we do not utilize it since we are only running basic NER and PoS tagging in English. If your model only serve a single language, please remove the language option. We also have another option box for sentence examples. If our users just wish to run a simple demo, this feature can be very handy. Therefore, it is recommended that you include some examples that can clearly and nicely demonstrate the functionality of your demo. 

In addition, you may also modify the hyperlink to the [CSS files](To be Update for Final Version) and the hyperlink to the [JavaScript files](To be Update for Final Version) according to your needs.

### CSS

Since we are using external CSS files, we do not keep a hard copy of any CSS files in the folder for this demo as they are served online. However, if you want to build your own CSS files, you can include the file in the frondend/css folder and add the extra configuration in the [service_backend.py](To be Update for Final Version) file.

### Javascript

The [demo.js](To be Update for Final Version) controls the dynamic contents on the website, such as form submitting or language option choosing. Based on your annotation service, you can modify the list of available languages. You can also modify the examples for each language. Furthermore, there are several functions that handle changes and sumbits on the HTML form. You may refer to the [JavaScript file](To be Update for Final Version) and use the comments to understand what each function behaves.

Please note that you are very likely need to change the [runAnnotation()](To be Update for Final Version). Please modify the data variable to include every necessary elements for you annotation service. For our demo, we only need to send the text in data, but for your purpose, the data can be more complicated, such as adding language and other flags.
