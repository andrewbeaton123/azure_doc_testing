from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
# Replace with your endpoint and key


# Set the document model to be used for analysis
model = "prebuilt-read"  # You can choose a different model if needed
def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def extract_numerics(document_url):
  """
  Analyzes a document at the specified URL and extracts numeric values.

  Args:
      document_url (str): The URL of the document to be analyzed.

  Returns:
      list: A list of extracted numeric values.
  """
  client = DocumentAnalysisClient(endpoint=endpoint, 
                                  credential=AzureKeyCredential(key))

  # Analyze the document
  poller = client.begin_analyze_document_from_url(model, document_url)
  result = poller.result()
  print ("Document contains content: ", result.content)
  for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )
        
  for page in result.pages:
        print("----Analyzing Read from page #{}----".format(page.page_number))
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

  for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_bounding_box(line.polygon),
                )
            )

  for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

  print("----------------------------------------")

# Example usage
document_url = r"https://dagrs.berkeley.edu/sites/default/files/2020-01/sample.pdf"
#r"https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2024/strategic-report-2023.pdf"  # Replace with your document URL
#extracted_numerics, all_stuff = 
extract_numerics(document_url)
"""


if extracted_numerics:
  print("Extracted numeric values:")
  for value in extracted_numerics:
    print(value)
else:
  print(all_stuff)
  print("No numeric values found in the document.")"""