# PDFHarvester

PDFHarvester is a Python package for extracting tables, images, and keywords from PDF documents.

## Installation

You can install PDFHarvester using pip:

```sh
pip install PDFHarvester
```

# Usage

To extract tables, images, and keywords from a PDF document using PDFHarvester, you can use the following functions:

```
import pdfharvest as ph

tables = ph.extract_table('path/to/pdf')
images = ph.extract_images('path/to/pdf')
keywords = ph.extract_keywords('path/to/pdf')
```

`extract_table` returns a list of pandas dataframes, one for each table in the PDF. `extract_images` returns a list of images as numpy arrays, and `extract_keywords` returns a list of keywords as strings.

#Contributing
Bug reports and pull requests are welcome on GitHub at <https://github.com/yourusername/PDFHarvester>. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

#License
The package is available as open source under the terms of the [MIT License](https://github.com/yourusername/PDFHarvester/blob/main/LICENSE.md), © 2023 Hashim Puthiyakath.

Please let me know if you have any further questions or concerns.
