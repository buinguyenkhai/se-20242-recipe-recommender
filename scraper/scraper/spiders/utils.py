from re import sub

def clean_text(text_lst):
    return [sub(r'\s{2,}', ' ', sub(r'<.*?>', '', text)).strip() for text in text_lst]