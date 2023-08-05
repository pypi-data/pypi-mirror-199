import PyPDF2
import pandas as pd
import yake
import textract


def get_keywords(file_path, max_ngram_size=3, deduplication_threshold=0.9, numOfKeywords=50):
    # open the pdf file in binary mode
    with open(file_path, 'rb') as pdf_file:
        # create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # get the number of pages
        num_pages = pdf_reader.numPages
        # initialize the text variable
        text = ""
        # loop through each page and extract the text
        for page_num in range(num_pages):
            page_obj = pdf_reader.getPage(page_num)
            text += page_obj.extractText()

        # if no text was extracted, use textract to extract text from scanned PDFs
        if not text:
            text = textract.process(
                file_path, method='tesseract', language='eng')

        # initialize the keyword extractor object
        kw_extractor = yake.KeywordExtractor(
            lan="en", n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

        # extract the keywords and store them in a DataFrame
        keywords = kw_extractor.extract_keywords(text)
        keywords_df = pd.DataFrame(keywords, columns=['keywords', 'value'])

    # return the keywords DataFrame
    return keywords_df
