from load_google_doc import read_faq
import pandas as pd


result = read_faq("1qZjwHkvP0lXHiE4zdbWyUXSVfmVGzougDD6N37bat3E")
df = pd.DataFrame(result)

# print(df.head())

faq_documents = {
    'llm-zoomcamp': '1m2KexowAXTmexfC5rVTCSnaShvdUQ8Ag2IEiwBDHxN0',
}


documents = []

for course, file_id in faq_documents.items():
    print(course)
    course_documents = read_faq(file_id)
    documents.append({'course': course, 'documents': course_documents})

print(len(documents)) # 1
