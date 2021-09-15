# Test file to run MultiscaleTemplateMatching.py on different canvas images.
from MultiscaleTemplateMatching import read_image, return_dim, preprocess_image, plt_imshow, detect_object, draw_match

for i in range(1,9):
    template = read_image('pepsi_template.png') #Receive filename
    template = preprocess_image(template) #Receive image object
    canvas = read_image('pepsi_image0{}.jpg'.format(i)) #Receive filename

    result = detect_object(canvas, template) #Receive object names
    draw_match(result, canvas, template)