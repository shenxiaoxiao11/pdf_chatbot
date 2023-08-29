from langchain.docstore.document import Document
import fitz
import re
print(fitz.__doc__)
def load_pdf(filename):
    pdf_reader = fitz.open(filename)

    text = ''
    for num in range(pdf_reader.page_count):
        page = pdf_reader.load_page(num)
        text += page.get_text(text)
    return text

# 自定义句子分段的方式，保证句子不被截断
def split_paragraph(text, pdf_name, max_length=300):
    text = text.replace('\n', '') 
    text = text.replace('\n\n', '') 
    text = re.sub(r'\s+', ' ', text)
    """
    将文章分段
    """
    # 首先按照句子分割文章
    sentences = re.split('(；|。|！|\!|\.|？|\?)',text) 
    
    new_sents = []
    for i in range(int(len(sentences)/2)):
        sent = sentences[2*i] + sentences[2*i+1]
        new_sents.append(sent)
    if len(sentences) % 2 == 1:
        new_sents.append(sentences[len(sentences)-1])
#     print(new_sents)
    
    # 按照要求分段
    paragraphs = []
    current_length = 0
    current_paragraph = ""
    for sentence in new_sents:
        sentence_length = len(sentence)
        if current_length + sentence_length <= max_length:
            current_paragraph += sentence
            current_length += sentence_length
        else:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence
            current_length = sentence_length
    paragraphs.append(current_paragraph.strip())
    documents = []
    metadata = {"source": pdf_name}
    for paragraph in paragraphs:
        new_doc = Document(page_content=paragraph, metadata=metadata)
        documents.append(new_doc)
    return documents
