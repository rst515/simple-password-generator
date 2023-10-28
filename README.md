# simple-password-generator

API endpoint to generate a simple password.
Returns a simple password string: Three words (one CAPS, randomised), separated by a random punctuation character
`!#$%&*+-<=>?@_` and ending with a number 0-99.

This API endpoint is written in Python and built with the AWS Serverless Application Model (SAM)
using AWS CodeBuild, AWS API Gateway and AWS Lambda.
It was created using Test Driven Development (TDD).

To use this project
1. Clone the repository.
2. Install the project dependencies using `pip install -r requirements.txt`
3. To run the tests use `python -m pytest tests`
4. To view the api documentation, open `api-docs.html` in a browser

The AWS CodeBuild and AWS CloudFormation YAML files for serverless deployment are included for reference.