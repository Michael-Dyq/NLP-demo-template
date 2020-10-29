# Front End Design

## Introduction

The front end design usually consists of three parts: HTML, CSS, and JavaScript. Since it controls how the interface displays to the users, it is very important to have a easy-to-follow, interactive design. 

## Components

### HTML

HTML stands for Hyper Text Markup Language and is the standard markup language for creating Web pages. HTML document is made of a series of HTML elements. HTML elements tell the browser how to display the content. For instance, HTML elements label pieces of content such as "this is a heading", "this is a paragraph", "this is a link", etc. You may refer to the [HTML file](index.html) and take a look how the elements are arranged in the document.

External Material: https://www.w3schools.com/html/html_intro.asp

### CSS

CSS stands for Cascading Style Sheets. CSS describes how HTML elements are to be displayed on screen, paper, or in other media. CSS can save a lot of effort by controling the layout of multiple web pages all at once. However, it is important to note that you don't always need to generate CSS files on your own. There are many well-written CSS templates online, such as w3css, UIkit, etc. In our demo, we do not create our own CSS files. Instead, we load a CSS from online resource.

External Material: https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/about-readmes

### JavaScript

JavaScript files is capable of changing the HTML elements and CSS attributes. In order words, JavaScript can change a site from static to dynamic based on the user's behavior. For instance, when we submit a sentence to the backend for annotation and receive a result, we need to create a new HTML element to store the result and display it nicely. The JavaScript's functionality can also be enhanced by JQuery, a JavaScript library. It allows us to generate code in a simpler and cleaner way. You may refer to the [JavaScript file](js/demo.js) to see how we create the functions to manipulate the views.

External Material: https://www.w3schools.com/jquery/jquery_intro.asp

## How to Implement it
Run the command in your terminal. The service is currently running on dickens:4033 and dickens:4034. You may alter the port number based on your need.

 ```python

 ```

## How to Retrieve the Output

## Post Request

This script use an example string of 'Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017.', and calls two backend services mentioned above. You need to modify the port number and urls based on where your service is running.

```python
python api_post_request.py
```
