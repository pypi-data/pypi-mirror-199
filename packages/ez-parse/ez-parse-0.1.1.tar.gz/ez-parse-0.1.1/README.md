# Resume-Parser
A Python library that scrapes essential information from PDFs of LinkedIn profiles.

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

![](https://img.shields.io/github/issues/ShivanshSrivastava1/Resume-Parser)

![](https://github.com/ShivanshSrivastava1/Resume-Parser/actions/workflows/build.yml/badge.svg)

[![codecov](https://codecov.io/github/ShivanshSrivastava1/Resume-Parser/branch/main/graph/badge.svg?token=V4IKQ490DY)](https://codecov.io/github/ShivanshSrivastava1/Resume-Parser)

[Project Board](https://github.com/users/ShivanshSrivastava1/projects/2/views/1)

## Overview
This is a parser that extracts important information from a LinkedIn profile PDF. It converts the PDF to a list of strings, and then uses LinkedIn's headers to create a dictionary that maps said headers to string values that contain the most relevant parts of a candidate's profile.

## Installation
Install the library's dependencies and build the library using `make develop`.

## Accessing LinkedIn PDFs
Visit the LinkedIn profile that you would like to parse. Under the individual's basic profile information, there is a button labeled "More". Click on this button, and then click on "Save to PDF".

## Usage
In your code, begin by importing the package:

`from Resume-Parser import parser`

You can extract the text data from the PDF like so:

`data = parser.extract_pdf(<path_to_linkedin_pdf>)`

This parsed data can also be stored in a dictionary:

`res = parser.get_many(data)`
