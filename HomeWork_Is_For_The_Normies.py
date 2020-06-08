from bs4 import BeautifulSoup
import requests
import re
import random
from PIL import Image
import wget
import cv2
import pycountry
import tkinter

def check_table_info(current_page):

    #define lists
    issue_Names_List = []
    issue_Vaule_List = []
    issue_Names_List.clear()
    issue_Vaule_List.clear()

    #re.compile
    pattern_table = re.compile(r"<tr class=(.*?)</td>(.*?)</td>(.*?)</td>(.*?)</td>")
    pattern_Find_Name_L1 = re.compile(r"<td>(.*?)<sup>")
    pattern_Find_Value_L1 = re.compile(r">[0-9-].*?<")

    all_List_Elements = pattern_table.findall(str(current_page))
    for i in range(len(all_List_Elements)):
        txt_To_Shearch = all_List_Elements[i]

        #prossesong name
        processed_String_Name_L1 = pattern_Find_Name_L1.findall(str(txt_To_Shearch))
        processed_String_Data_L1 = pattern_Find_Value_L1.findall(str(txt_To_Shearch))
        processed_String_Data_L2 = str(processed_String_Data_L1).replace(" ", "")
        issue_Names_List.append(processed_String_Name_L1)
        issue_Vaule_List.append(processed_String_Data_L2)


            #pick two random issues
    random_Pick_1 = random.randrange(len(issue_Names_List))
    random_Pick_2 = random.randrange(len(issue_Names_List))
    random_Pick_3 = random.randrange(len(issue_Vaule_List))


    issue_1_Name = issue_Names_List[random_Pick_1]
    issue_1_Vaule = issue_Vaule_List[random_Pick_1]
    issue_2_Name = issue_Names_List[random_Pick_2]
    issue_2_Vaule = issue_Vaule_List[random_Pick_2]
    issue_3_Name = issue_Names_List[random_Pick_3]
    issue_3_Vaule = issue_Vaule_List[random_Pick_3]

    return issue_1_Name, issue_2_Name, issue_3_Name, issue_1_Vaule, issue_2_Vaule, issue_3_Vaule


def get_Country_Flag(url_of_counrtry, full_Index_HTML):

    #defin regex patterns
    pattern_find_Country_Section_L1 = re.compile(rf"<a href=\"{url_of_counrtry}\">(.*?)</li>")
    pattern_find_img_html = re.compile(r"\/common\/flags\/.*?\.png")

    #Extract img url from html
    URL_Extrated_Section = pattern_find_Country_Section_L1.findall(str(full_Index_HTML))
    Ectrated_img_Url = pattern_find_img_html.findall(str(URL_Extrated_Section))
    flag_img_url = "http://data.un.org" + str(Ectrated_img_Url[0])

    #grab and download img
    flag_img_download_name = wget.download(flag_img_url, out = 'flags')
    color1_final_name, color2_final_name, color3_final_name, color1_final_percent, color2_final_percent, color3final_percent = find_colors_and_percets(flag_img_download_name)
    return color1_final_name, color2_final_name, color3_final_name, color1_final_percent, color2_final_percent, color3final_percent, flag_img_download_name, flag_img_url

def find_colors_and_percets(flag_img_name):
    img = Image.open(flag_img_name)
    left = 12
    top = 41
    right = 12
    bottom = 41

    # Cropped image of above dimension
    img2 = img.crop((left, top, right, bottom))
    #open
    flag_img_not = cv2.imread(flag_img_name)
    flag_img_not_rg = flag_img_not[41:151, 12:180]
    cv2.imwrite(flag_img_name, flag_img_not_rg)
    flag_img_not_rgb = cv2.imread(flag_img_name)
    #flag_img_not_rgb = cv2.cvtColor(flag_img_not, cv2.COLOR_RGB2RGBA)
    print(flag_img_not_rgb[96, 96])
    #define col and row
    row, col, inte = flag_img_not_rgb.shape
    print(row, col)
    last_pixel_color = [-1, -1, -1]
    list_of_colors = [0]
    all_pixels = []
    recorded_colors = []
    amount_of_color = []
    color_names = []
    clear_pixel = (0,0,0)
    clear_pixel_count = 0


    all_pixels_non_str = []
    cv2.imshow("iamge", flag_img_not_rgb)
    cv2.waitKey(1)
    for x in range(row):
        for y in range(col):
            pixel = flag_img_not_rgb[x,y]
            all_pixels.append(str(pixel))
            pixel



    print(len(all_pixels))

    #creats list of colors without repeating
    for i in range(len(all_pixels)):
        color_to_count = str(all_pixels[i])
        number_of_maches = (recorded_colors.count(color_to_count))
        if number_of_maches == 0:
            recorded_colors.append(all_pixels[i])

    #
    for i in range(len(recorded_colors)):
        amount_of_color.append(all_pixels.count(recorded_colors[i]))
        color_names.append(recorded_colors[i])

    #declaring high counts

    high_count_1 = 0
    high_count_2 = 0
    high_count_3 = 0
    high_count_4 = 0
    high_count_5 = 0

    #print some infomration
    print(color_names)
    print(amount_of_color)
    print(all_pixels)

    #find the highest counts of colors
    for i in range(len(recorded_colors)):
        current_color_count = amount_of_color[i]
        if current_color_count > high_count_1:
            high_count_1 = current_color_count
        current_color_count = amount_of_color[i]
        if current_color_count < high_count_1 and current_color_count > high_count_2:
            high_count_2 = current_color_count
        current_color_count = amount_of_color[i]
        if current_color_count < high_count_2 and current_color_count > high_count_3:
            high_count_3 = current_color_count
        current_color_count = amount_of_color[i]

    #diminted the high colors count color value
    color_1_amount = color_names[(amount_of_color.index(high_count_1))]
    color_2_amount = color_names[(amount_of_color.index(high_count_2))]
    color_3_amount = color_names[(amount_of_color.index(high_count_3))]


    #calculate percentage
    full_pixel_count = (int(flag_img_not_rgb.size)/3)
    loc1 = amount_of_color.index(high_count_1)
    color_1_percent = ((amount_of_color[loc1]/full_pixel_count)*100)
    color_2_percent = ((high_count_2/full_pixel_count)*100)
    color_3_percent = ((high_count_3/full_pixel_count)*100)
    print(color_1_percent)
    print(color_2_percent)
    print(color_3_percent)


    #finding the names of the colors
    color_1_location = (amount_of_color.index(high_count_1))
    color_2_location = (amount_of_color.index(high_count_2))
    color_3_location = (amount_of_color.index(high_count_3))
    color_1_name = color_names[color_1_location]
    color_2_name = color_names[color_2_location]
    color_3_name = color_names[color_3_location]

    return color_1_name, color_2_name, color_3_name, color_1_percent, color_2_percent, color_3_percent



    #define var
    col = 0
    row = 0
    max_col = flag_img.shape[0]
    max_row = flag_img.shape[1]





def compile_and_print(flag_img_download, issue_1_Name, issue_1_Vaule, color1_final_name, issue_2_Name, issue_2_Vaule, color2_final_name, issue_3_Name, issue_3_Vaule, color3_final_name):
    color = [0, 0, 0]
    filter_color = re.compile("\d{1,3}")
    color = filter_color.findall(color1_final_name); color2 = filter_color.findall(color2_final_name); color3 = filter_color.findall(color3_final_name)
    print("hi")
    template = Image.open("template.png")

    current_flag = Image.open(flag_img_download)
    template.paste(current_flag)

    get_basic_name = re.compile(r"\w*?_\w.*?\.png")
    print(flag_img_download)
    flag_img_download_1 = get_basic_name.findall(flag_img_download)
    flag_img_download = flag_img_download_1[0]
    template.save("Temp/" + flag_img_download)
    template2 = cv2.imread("Temp/" + flag_img_download)
    font = cv2.FONT_HERSHEY_COMPLEX
    xy = (20, 140)
    xy2 = (20, 170)
    xy3 = (20, 200)
    scale = .4
    line_thicknes = 1
    #adding country name
    #regex name to only get letters
    alpha2_pattern = re.compile(r"\w*?_")
    countr_alpha2 = alpha2_pattern.findall(flag_img_download)
    country_alpha2 = countr_alpha2[0].replace("_", "")
    full_country_name = pycountry.countries.get(alpha_2 = country_alpha2)
    print(full_country_name)

    g = int(color[1])
    b = int(color[2])
    r = int(color[0])
    g2 = int(color2[1])
    b2 = int(color2[2])
    r2 = int(color2[0])
    g3 = int(color3[1])
    b3 = int(color3[2])
    r3 = int(color3[0])
    temp = cv2.putText(template2, f"The issue is {issue_1_Name} in 2005, 2010 and 2019 respectively, was at {issue_1_Vaule}", xy, font, scale, (r, g, b), line_thicknes, cv2.LINE_AA)
    temp = cv2.putText(template2,
                       f"The issue is {issue_2_Name},  in 2005, 2010 and 2019 respectively, was at {issue_2_Vaule}", xy2,
                       font, scale, (r2, g2, b2), line_thicknes, cv2.LINE_AA)
    temp = cv2.putText(template2,
                       f"The issue is {full_country_name}", (11, 1),
                       font, scale, (r2, g2, b2), line_thicknes, cv2.LINE_AA)
    temp = cv2.putText(template2,
                       f"The issue is {issue_3_Name} in 2005, 2010 and 2019 respectively, was at {issue_3_Vaule}", xy3,
                       font, scale, (r3, g3, b3), line_thicknes, cv2.LINE_AA)
    cv2.imshow('output', temp)
    cv2.imwrite("output/Desposito." + flag_img_download, temp)
    print(color)


def UI():
    do_all_homework_window = tkinter.Tk()
    do_all_homework_window.geometry('270x300')
    do_all_homework_window.title("HomeWorkMCDoer")
    do_all_homework_window.configure(bg = "black")




def Begin_program():
    url="http://data.un.org/en/index.html"
    html_content = requests.get(url)
    getpage = BeautifulSoup(html_content.text, 'html.parser')
    pattern_Iso = re.compile(r"iso....html")
    lnks = getpage.find_all('a')
    complete_link_list = pattern_Iso.findall(str(lnks))
    complete_link_list_length = range(len(complete_link_list))


    for x in complete_link_list_length:
        country_Page_To_Grab = complete_link_list[x]
        country_Page_Url = "http://data.un.org/en/" + country_Page_To_Grab
        country_Page_To_Grabed = requests.get(country_Page_Url).text
        country_Country_Page = BeautifulSoup(country_Page_To_Grabed, 'html.parser')

        issue_1_Name, issue_2_Name, issue_3_Name, issue_1_Vaule, issue_2_Vaule, issue_3_Vaule = check_table_info(country_Country_Page)
        color1_final_name, color2_final_name, color3_final_name, color1_final_percent, color2_final_percent, color3_final_percent, flag_img_download, flag_img_url = get_Country_Flag(country_Page_To_Grab, getpage)
        print(issue_1_Name, issue_1_Vaule, issue_2_Name, issue_2_Vaule, issue_3_Name, issue_3_Vaule)
        print(color1_final_name, color1_final_percent, color2_final_name, color2_final_percent, color3_final_name, color3_final_percent)
        compile_and_print(flag_img_download, issue_1_Name, issue_1_Vaule, color1_final_name, issue_2_Name, issue_2_Vaule, color2_final_name, issue_3_Name, issue_3_Vaule, color3_final_name,)
        print(country_Page_To_Grab)



        print("susess")

do_all_homework_window = tkinter.Tk()
do_all_homework_window.geometry('270x300')
do_all_homework_window.title("HomeWorkMCDoer")
do_all_homework_window.configure(bg="black")

# define params
button = tkinter.Button(do_all_homework_window, text='DO HOMEWORK', command=Begin_program, bg="red", width='30',
                        height='5')
label1 = tkinter.Label(do_all_homework_window, text="Oliver's  HOMEWORK Thingy-M-Gig", bg='white', fg='black', height=2,
                       width=33)

# append to window
label1.pack(expand=True)
button.pack(expand=True)

do_all_homework_window.mainloop()