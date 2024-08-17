import spacy

import subprocess
import sys

from langchain_core.documents import Document

def download_spacy_pt_model():
    model_name = "pt_core_news_sm"
    subprocess.run([f"{sys.executable}", "-m", "spacy", "download", model_name])

def sliding_window_split(documents, stride, window_size):
    sentencizer = spacy.blank('pt')
    sentencizer.add_pipe('sentencizer')

    window_documents = []

    for document in documents:
        text = document.page_content
        paragraphs = text.split('\n\n')
        paragraphs = [ p.replace('\n', ' ').strip() for p in paragraphs if p.strip() ]
        for paragraph in paragraphs:
            p_sentencized = sentencizer(paragraph)
            sentences = [ sent.text.strip() for sent in p_sentencized.sents ]
            for i in range(0, len(sentences), stride):
                window_text = ' '.join(sentences[i : min(len(sentences), i+window_size)]).strip()
                window_documents.append(Document(page_content=window_text))

    return window_documents