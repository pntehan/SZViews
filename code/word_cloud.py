from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread


def drawCloud(word, img, output, rep=True):
    '''word词云内容，img图片路径， output输出路径'''
    Img = imread(img)
    wc = WordCloud(background_color='seashell',
                   max_words=200,
                   max_font_size=100,
                   mask=Img,
                   font_path='../wordCloud/simhei.ttf',
                   repeat=rep,
                   random_state=42)
    wc.generate(word)
    image_colors = ImageColorGenerator(Img)
    plt.imshow(wc)
    plt.axis('off')
    plt.figure()
    plt.axis('off')
    wc.to_file(output)
