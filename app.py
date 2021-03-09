import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import os

from datetime import datetime


#디렉토리와 이미지를 주면, 해당 디렉토리의 이 이미지를 저장하는 함수.
def save_uploaded_file(directory, img):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = datetime.now().isoformat(sep = '-').replace('.', '-').replace(':', '-')
    img.save(directory + '/' + filename +  '.jpg') #이미지를 수정했으니까 이미지를 저장할 때 img.save()를 써야한다.
    return st.success("Saved file : {} in {}".format(filename + '.jpg', directory))

def load_image(image_file):
    img = Image.open(image_file)
    return img


def main(): 

    #1.파일 업로드하기.
    
    image_file_list = st.file_uploader("이미지 파일 업로드", type = ['png', 'jpeg', 'jpg'], accept_multiple_files=True)

    print(image_file_list)

    if image_file_list is not None:

    # 2. 여기까지 리스트에 들어가 있는 것들은 전부 파일이다. 각 파일을 이미지로 바꿔줘야 화면에 찍든 뭘하든 할 수 있다. 파일 상태하고 이미지 상태는 완전히 다르다.
    # 파일 하나를 가져와서 변수 하나에 저장할 순 없다. 데이터 여러개 저장할 땐? 리스트.

        image_list = []
    
    # 2-1. 모든 파일이 image_list에 이미지로 저장됨.
        for image_file in image_file_list:
            img = load_image(image_file)
            image_list.append(img)
    
    # 3. 이미지를 화면에 확인해본다.
        # for img in image_list:
        #     st.image(img)
            

        option_list = ['Show Image', 'Rotate Image', 'Create Thumbnail', 'Crop Image', 'Merge Images', 
                    'Flip Image', 'Change_Color', 'Filters - Sharpen', 'Filters - Edge enhance',
                    'Contrast Image'] 
        option = st.selectbox('옵션을 선택하세요.', option_list)



        #하드코딩을 없애는 작업.


        if option == 'Show Image':
            raw_image_list=[]
            for img in image_list:
                st.image(img)
                raw_image_list.append(img)
            if st.button('파일 저장', key = 'show_image'):
                directory = st.text_input('파일 경로 입력', key = 'show_image')
                for img in raw_image_list:
                    save_uploaded_file(directory, img)
                




        elif option == 'Rotate Image':

            #유저에게 각도를 입력받는다.
            degree = st.number_input('각도입력', 0, 360)

            #이미지를 다 돌린다.
            transformed_img_list = []
            for img in image_list:
                rotated_img = img.rotate(degree)                
                st.image(rotated_img)                   #화면에도 보여주고
                transformed_img_list.append(rotated_img)

            #디렉토리 이름 받는다.
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                # 3. 파일 저장.
                for img in transformed_img_list:
                    save_uploaded_file(directory, img)
            




        elif option == 'Create Thumbnail':
                width = st.slider("썸네일 가로 사이즈 입력", 1, 100)
                height = st.slider("썸네일 세로 사이즈 입력", 1, 100)

                size = (width, height)
                transformed_img_list = []
                for img in image_list:
                    img.thumbnail(size)         #img.thumbnail(size) 은 이미지 자체를 바꿔버린다. 변수에 저장하면 안된다.
                    st.image(img)
                    transformed_img_list.append(img)
                directory = st.text_input('파일 경로 입력')
                #이미지 다 불러와서 가장 작은 거 찾고 그걸 기준으로 가로세로 제한을 정해야하는데 귀찮으니까 그냥 넘긴다.
                if st.button('파일 저장'):
                    for img in transformed_img_list:
                        save_uploaded_file(directory, img)
        



        elif option == 'Crop Image':
            if image_list is not None:
                crop_start_x = st.slider('썸네일 자르기 가로 시작점 입력', 0,300)
                crop_start_y = st.slider('썸네일 자르기 세로 시작점', 0,300)
                crop_to_x = st.slider('썸네일 가로 꼭지점 입력', 0,300)
                crop_to_y = st.slider('썸네일 세로 꼭지점 입력', 0,300)
                for img in image_list:
                    st.image(img)
                    img = load_image(img)
                    #왼쪽 위 부분부터 시작해서, 너비와 깊이만큼 잘라라.
                    #왼쪽 윗 부분이 좌표 (50,100)
                    #너비 x축 으로 200, 깊이 y축으로 200. (200,200)

                    #왼쪽 위에서 오른쪽 으로 200, 아래쪽으로 200한 영역.
                    box = (crop_start_x, crop_start_y, crop_to_x, crop_to_y)
                    cropped_image = img.crop(box)
                    img.save('data/crop.png')
                    st.image(cropped_image)




        elif option == 'Merge Images':
            st.write('휴무')
            pass






        elif option == 'Flip Image':
            status = st.radio('플립 선택', ['FLIP_TOP_BOTTOM', 'FLIP_LEFT_RIGHT'])
            if status == 'FLIP_TOP_BOTTOM':
                transformed_img_list = []
                for img in image_list:
                    flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)
            elif status == 'FLIP_LEFT_RIGHT':
                transformed_img_list = []
                for img in image_list:
                    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)

            directory = st.text_input('파일 경로 입력', key = 'show_image')       #스트림릿이라서 이 줄을 아래 이프문 안에 넣어서 숨길 수가 없다. 
            if st.button('파일 저장', key = 'show_image'):
                for img in transformed_img_list:
                    save_uploaded_file(directory, img)


    

        
                






        elif option == 'Black & White':
            bw = img.convert("L")          #1은 black and white 모드, L은 그레이스케일(흑백과 구분하기), RGB로 쓰면 컬러. 
            st.image(bw)

        elif option == 'Filters - Sharpen':
            sharp_img = img.filter(ImageFilter.SHARPEN)     #ImageFilter.치면 뭐가 많이 나옴ㄴ
            st.image(sharp_img)      #선명하게 나옴.
        
        elif option == 'Filters - Edge enhance':
            edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
            st.image(edge_img)           #윤곽선이 진해진다.

        elif option == 'Contrast Image':
            contrast_img = ImageEnhance.Contrast(img).enhance(2)
            st.image(contrast_img)       #대비가 세진다.
        else:
            pass


    # 1.이미지를 업로드해서 이걸 ㅓ하 ㄹ 수 있어야한다. 이미지 1장.


    # 2. 하드코딩된 코드를, 유저한테 입력받아서 처리할 수 있도로 ㄱ바꾼다.


if __name__ == '__main__':         #__name__은 변수다. 파이썬 내장변수
    main()