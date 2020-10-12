Feature: Upload Image

As a SupplyHero user
I want to upload an Image to the School Supply Application
So that I can get a list of school supplies


Scenario: Upload an Image (Normal Flow)
  
Given user is selecting an image
When user requests to upload the file
Then user should receive a school supply list


Scenario: Uploading a PDF file (Alternate Flow)
  
Given user selected a file that is a PDF
When user requests to upload the file
Then user should receive a school supply list


Scenario: Uploading a wrong file type (Error Flow)
  
Given user selected a file that is not an image or pdf
When user requests to upload the file
Then user is informed that "File is not an image."

