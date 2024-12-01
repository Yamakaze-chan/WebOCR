import easyocr
from manga_ocr import MangaOcr
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
# from googletrans import Translator

def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int):
        lines = ['']
        _, top, _, bottom = font.getbbox(text)
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            # print(font.getlength(line), line_length)
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        max_text_w = 0
        for line in lines:
            left, _, right, _ = font.getbbox(line)
            if right - left > max_text_w:
                max_text_w = right - left
        return '\n'.join(lines), max_text_w ,len(lines)*(bottom - top)

#Checkoverlap and get the largest bbox
def bb_intersection_over_union(boxA: list, boxB: list):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[2], boxB[2])
    xB = min(boxA[1], boxB[1])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA ) * max(0, yB - yA )
    boxAArea = (boxA[0] - boxA[1] ) * (boxA[2] - boxA[3] )
    boxBArea = (boxB[0] - boxB[1] ) * (boxB[2] - boxB[3] )
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou, [min(boxA[0], boxB[0]), max(boxA[1], boxB[1]), min(boxA[2], boxB[2]), max(boxA[3], boxB[3])]

#Detect and get bbox of text
def get_bbox(img: Image, detect_text_model: easyocr):
    #detect and get bbox
    print(type(img))
    bboxes = detect_text_model.detect(img, bbox_min_score = 0.01)[0][0]
    bboxes.sort(key=lambda x: x[2])
    bboxes.sort(key=lambda x: x[0])
    # draw = ImageDraw.Draw(img)

    #combine bbox
    for i in range(0,len(bboxes)):
        for j in range(0,len(bboxes)):
            overlap = bb_intersection_over_union(bboxes[i], bboxes[j])
            if overlap[0] == 1.0 or overlap[0] == 0.0: continue
            else:
                bboxes[i] = bboxes[j]=overlap[1]
    bboxes = list(set(tuple(element) for element in bboxes)) #remove duplicate
    # for k in bboxes:
    #     draw.rectangle(((k[0], k[2]), (k[1], k[3])), outline ="black")
    # img.show() 
    # print(bboxes, end='\n')
    return bboxes

def get_text(img: Image, read_text_model: MangaOcr, coor: list):
    return read_text_model(img.crop((coor[0],coor[2], coor[1],coor[3])))

def translate_text(text: str, lang='en'):
    return GoogleTranslator(source='auto', target=lang).translate(text) 

# def translate_text1(model: Translator, text:str, dest='en'):
#     return model.translate(text, dest=dest).text

def read_image(img: Image, detect_text_model: easyocr, read_text_model: MangaOcr):
    draw = ImageDraw.Draw(img)
    for bbox in get_bbox(img, detect_text_model): #Detect text in image
        text = get_text(img, read_text_model, bbox) #extract text from image
        # translated_text = translate_text1(gg_trans, text) #Translate text
        translated_text = translate_text(text)
        # translated_text = ""
        if translated_text:
            print(text+"---->"+translated_text)
            draw.rectangle(((bbox[0], bbox[2]), (bbox[1], bbox[3])), fill="white") #remove old text

            # Downsize font
            size = 30
            font = ImageFont.truetype(r"arial.ttf", size)
            add_text = get_wrapped_text(translated_text, font, bbox[1]-bbox[0])
            while(((add_text[1] > bbox[1]-bbox[0]) or (add_text[2] > bbox[3]-bbox[2])) and size >=10):
                size = size - 1
                font = ImageFont.truetype(r"arial.ttf", size)
                add_text = get_wrapped_text(translated_text, font, bbox[1]-bbox[0])
            
            # Add text to image
            draw.text((bbox[0], bbox[2]), add_text[0], font = font, fill="#000") 
        # print(add_text)
    # img.show()
    return img

def init_model():
    m_ocr = MangaOcr(pretrained_model_name_or_path="model", force_cpu=False)
    e_ocr = easyocr.Reader(['ja'], gpu=False, download_enabled=False, model_storage_directory="model")
    # e_ocr = easyocr.Reader(['ja'])
    # m_ocr = MangaOcr()
    return e_ocr, m_ocr