import url_utils
import requests
from PIL import Image
from urllib.request import urlopen

'''
Given the url of an image and a directory, attempt to download that image to the directory.
directory: where to save the file; must end in / or \

If the url is incorrect, return false. Otherwise, return true. 
'''
def download_image(pic_url : str, directory : str) -> bool:
    
    response = requests.get(pic_url, stream = True)
    # Can we download this image?
    if( not response.ok):
        return False
    
    # Get all image data, which is everything after the /
    url_img_data = pic_url.rsplit('/', 1)[0]
    # get the filename, which is the above but without appended query params.
    # therefore, it looks like website.com/filename.ext?blah=foo&w=2000 and we get filename.ext
    filename = url_img_data.split('?', 1)[0]
    # image_name is the filename, minus the file extension
    image_name = filename.rsplit('.', 1)[0]

    # Get the file extension. if this is webp, we want to convert the image to jpg. 
    # If the extension is png, preserve it. 
    extension = filename.rsplit('.')[-1]
    if(extension != 'png'):
        extension = 'jpg'
        filename = image_name + '.' + extension
    im_format = 'jpeg' if (extension in {'jpg', 'jpeg'}) else 'png'

    # img = Image.open(urlopen(pic_url)).convert("RGB")
    # for jpeg:
    # img.save(image_name + ".jpg", "jpeg")
    # for png:
    # im.save(image_name + ".png", "png")
    
    img = Image.open(urlopen(pic_url)).convert("RGB")
    img.save(directory + filename, im_format)
    
    '''
    with open(directory + filename, 'wb') as handle:

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    '''
    return True

    
def grab_image(url : str, directory : str):
    # A variable we use at each step, to see if the current method was successful. If it was not, continue.    
    success = False

    # If the URL contains another url, try that first.
    url_params = url_utils.get_query_params(url, decode_percents = True)
    url_params_keyset = set(url_params)

    # some key values it might use:
    img_source_names = {'url', 'URL', 'source'}

    potential_source_names = set.intersection(url_params_keyset, img_source_names)

    # If there is overlap, continue
    for potential_source in potential_source_names:
        # If it does not contain '://' then it cannot be a valid URL. 
        if('://' not in url_params[potential_source]):
            continue
        # download from url_params[potential_source] and see if successful
        success = download_image(pic_url = url_params[potential_source], directory = directory)
        if(success):
            return True

    
    # What if the image CDN uses width, height, quality, etc? 
    
    # First, try stripping all query params.
    img_base_url = url.split('?')[0]
    # download from img_base_url and see if successful
    success = download_image(pic_url = img_base_url, directory = directory)
    if(success):
        return True
    
    # Otherwise, just try very large values. 