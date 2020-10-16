import re
from bs4 import BeautifulSoup


def parse_puppy_details(puppy_div):

    puppy_content_obj = puppy_div.find('div', attrs={"class": "sqs-block-content"}).find(
        'figure').find(
        'figcaption', attrs={"class": "image-card-wrapper"}).find(
        'div', attrs={"class": re.compile("image-card\s+sqs-dynamic-text-container", re.I)})

    puppy_name = puppy_content_obj.find('div', attrs={"class": "image-title-wrapper"}).find(
        "div", attrs={"class": re.compile("image-title\s+sqs-dynamic-text", re.I)}).find("p").text.strip()
    puppy_details = puppy_content_obj.find('div', attrs={"class": "image-subtitle-wrapper"}).find(
        "div", attrs={"class": re.compile("image-subtitle\s+sqs-dynamic-text", re.I)}).find_all("p")
    puppy_desc = puppy_details[0].text.strip()
    puppy_price_details = puppy_details[1].text.strip()
    puppy_delivery_options = puppy_details[2].text.strip()
    return puppy_name, puppy_desc, puppy_price_details, puppy_delivery_options


puppies_list = """
<div class="sqs-block image-block sqs-block-image sqs-text-ready" data-block-type="5" id="block-yui_3_17_2_1_1590094644926_270732"><div class="sqs-block-content" id="yui_3_17_2_1_1590283866070_148">








  

    

      <figure class="sqs-block-image-figure image-block-outer-wrapper image-block-v2 design-layout-card combination-animation-none individual-animation-none individual-text-animation-none image-position-left sqs-text-ready" data-scrolled="" data-test="image-block-v2-outer-wrapper" id="yui_3_17_2_1_1590283866070_147">

        <div class="intrinsic" id="yui_3_17_2_1_1590283866070_146">
          
            <div class="
                
                image-inset
                
                  content-fit
                
              " data-animation-role="image" data-description="" id="yui_3_17_2_1_1590283866070_145">
            <noscript><img src="https://images.squarespace-cdn.com/content/v1/5917bfae1b10e3f7ad1ef295/1590282663158-EJ45USWZMSY0OSB7EW7D/ke17ZwdGBToddI8pDm48kKrCyRiSzxpfXTLJbPZD_mNZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVHStLkcUP6Tyz069gBgDNR7OzHeIn0cX96LHoHfWxAWtVtO8nJtk629tZGIWiyY3XQ/Screen+Shot+2020-05-23+at+9.10.46+PM.png" alt="Aileen - Aileen is a stunning mini Newfiedoodle girl wearing a fancy black and white fur coat. Aileen is ready to be by your side. Aileen was born March 18th and based on her 70 pound Newfoundland Mom and 12 pound mini Poodle Dad, we expect her to be 26-47 pounds fully grown. Aileen is available for pick-up in the Greenville, SC area.Total Price = $1700 + $102 (6% SC sales tax) = $1802 totalDelivery to anywhere in the Continental U.S. = $2099 total" /></noscript>
            <img data-src="https://images.squarespace-cdn.com/content/v1/5917bfae1b10e3f7ad1ef295/1590282663158-EJ45USWZMSY0OSB7EW7D/ke17ZwdGBToddI8pDm48kKrCyRiSzxpfXTLJbPZD_mNZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVHStLkcUP6Tyz069gBgDNR7OzHeIn0cX96LHoHfWxAWtVtO8nJtk629tZGIWiyY3XQ/Screen+Shot+2020-05-23+at+9.10.46+PM.png" data-image="https://images.squarespace-cdn.com/content/v1/5917bfae1b10e3f7ad1ef295/1590282663158-EJ45USWZMSY0OSB7EW7D/ke17ZwdGBToddI8pDm48kKrCyRiSzxpfXTLJbPZD_mNZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVHStLkcUP6Tyz069gBgDNR7OzHeIn0cX96LHoHfWxAWtVtO8nJtk629tZGIWiyY3XQ/Screen+Shot+2020-05-23+at+9.10.46+PM.png" data-image-dimensions="410x450" data-image-focal-point="0.5,0.5" data-parent-ratio="0.9" alt="Screen Shot 2020-05-23 at 9.10.46 PM.png" style="left: 0.388889px; top: 0px; width: 387.222px; height: 425px; position: absolute;" class="loaded" data-image-resolution="1000w" src="https://images.squarespace-cdn.com/content/v1/5917bfae1b10e3f7ad1ef295/1590282663158-EJ45USWZMSY0OSB7EW7D/ke17ZwdGBToddI8pDm48kKrCyRiSzxpfXTLJbPZD_mNZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVHStLkcUP6Tyz069gBgDNR7OzHeIn0cX96LHoHfWxAWtVtO8nJtk629tZGIWiyY3XQ/Screen+Shot+2020-05-23+at+9.10.46+PM.png?format=1000w">
            <div class="image-overlay"></div>
          
            </div>
          

        </div>

        
          
          <figcaption class="image-card-wrapper" data-width-ratio="">
            <div class="image-card sqs-dynamic-text-container">

              
                <div class="image-title-wrapper"><div class="image-title sqs-dynamic-text" data-width-percentage="26.1" style="font-size: 26.1%;"><p class="">Aileen</p></div></div>
              

              
                <div class="image-subtitle-wrapper"><div class="image-subtitle sqs-dynamic-text" data-width-percentage="26.1" style="font-size: 26.1%;"><p class="">Aileen is a stunning mini Newfiedoodle girl wearing a fancy black and white fur coat. Aileen is ready to be by your side. Aileen was born March 18th and based on her 70 pound Newfoundland Mom and 12 pound mini Poodle Dad, we expect her to be 26-47 pounds fully grown. Aileen is available for pick-up in the Greenville, SC area.</p><p class="">Total Price = $1700 + $102 (6% SC sales tax) = $1802 total</p><p class="">Delivery to anywhere in the Continental U.S. = $2099 total</p></div></div>
              

              

            </div>
          </figcaption>
        

      </figure>

    

  


</div></div>
"""

if __name__ == '__main__':
    soup = BeautifulSoup(puppies_list, 'html.parser')
    all_puppies_posts = soup.find_all('div', attrs={"class":
                                                    re.compile("sqs-block\s+image-block\s+"
                                                               "sqs-block-image\s+sqs-text-ready", re.I)})
    for puppy in all_puppies_posts:
        n, d, p, do = parse_puppy_details(puppy)
        print(n, d, p, do)



