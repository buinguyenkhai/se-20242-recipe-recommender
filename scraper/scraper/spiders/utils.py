import re
from re import sub, search

time_reg = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}"

def clean_text(text_lst):
    return [sub(r'\s{2,}', ' ', sub(r'<.*?>', '', text)).strip() for text in text_lst]

def seperate_ingredient(text_lst):
    res = []
    for ing in text_lst:
        ing_tup = re.split(': | - ', ing)
        if len(ing_tup) == 1:
            match = search(r'\d', ing)
            ing_tup = (ing[:match.start()], ing[match.start():]) if match else (ing, None)
            if ing_tup[0] == "":
                ing_tup = (ing_tup[1], None)
            
        res.append(tuple(s.strip() if s is not None else None for s in ing_tup))
        
    return res
    
    
if __name__ == "__main__":
    print(seperate_ingredient(["3 củ khoai lang -", "1 bát bột xù -", "2 thìa bột mì -", "1/2 bát bột chiên giòn -", "2 quả trứng gà -", "1 chút muối -", "Dầu ăn -", "2 thìa sữa tươi -", "2 thìa kem tươi -"]))
        