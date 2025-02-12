import cv2
import datetime
import matplotlib.pyplot
import numpy as np
from matplotlib import pyplot as plt
def get_supported_resolutions():
    cap = cv2.VideoCapture(0)
    common_resolutions = [
        (1920, 1080),
        (1280, 720),
        (1024, 768),
        (800, 600),
        (640, 480),
    ]
    supported_resolutions = []
    for width, height in common_resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if (actual_width, actual_height) == (width, height):
            supported_resolutions.append((width, height))
    print("Supported resolutions:", supported_resolutions)
    cap.release()
    cv2.destroyAllWindows()
    #get_supported_resolutions()

def ReadAndWrite():
    #img = cv2.imread('lena.jpg',1)

    #img = cv2.line(img,(0,0),(300,300),(0,255,0),100)
    #img = cv2.arrowedLine(img,(500,500),(300,300),(0,255,0),10)
    img = np.zeros([512,512,3],np.uint8)
    img = cv2.circle(img,(200,200),100,(255,255,0),-1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img,'opencv',(100,200),font,1,(0,0,0),1,cv2.LINE_AA)
    
    pts = np.array([[100,200],[300,400],[500,300]],dtype=np.int32)
    print(pts)
    print(pts.shape)
    pts = pts.reshape((-1, 1, 2))
    print([pts])
    print(pts.shape)
    img = cv2.polylines(img,[pts],isClosed = False,color = (255,255,0),thickness=50)
    cv2.imshow('image1',img)
    k = cv2.waitKey(0)
    print("k:",k)
    if k == 27:
        cv2.destroyAllWindows()
    elif k == ord('s'):
        cv2.imwrite('lena_copy.jpg',img)
        cv2.destroyAllWindows()
    #ReadAndWrite()

def video():
    cap = cv2.VideoCapture("C:/Users/18269/Desktop/record/gjl.mp4")
    #cap = cv2.VideoCapture(0)
   
    while(cap.isOpened()):
        
        ret,frame1 = cap.read()
        ret,frame2 = cap.read()
        diff = cv2.absdiff(frame1,frame2)
        gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,5)
        _,threshold = cv2.threshold(blur,50,255,cv2.THRESH_BINARY)
        erosion = cv2.erode(threshold,None,iterations = 3)
        
        contours,_ = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame1,contours,-1,(0,255,0),2)
        
        for contour in contours:
            (x,y,w,h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 70:
                continue
            else:
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2,cv2.LINE_8)
                cv2.putText(frame1,'person',(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,1,1),1,cv2.LINE_4)
        cv2.imshow('frame1',frame1)
        
        '''
        canny = cv2.Canny(frame1,50,255)
        canny_color = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
        combined = cv2.add(frame1,canny_color)
        cv2.imshow('canny',combined)
        '''
        k = cv2.waitKey(100) & 0xff
        if k == ord('q'):
            break
    
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH  ))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    #print(width,height)
    #cap=cv2.VideoCapture(0)
    
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH  ))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
   

    #cap.set(3,1920)
    #cap.set(4,1080)
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH  ))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    #print(width,height)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('C:/Users/18269/Desktop/practice/output2.avi',fourcc,20,(544,960))
    '''
    while(cap.isOpened()):
        datet = str(datetime.datetime.now())
        ret,frame = cap.read()
        if ret == True:
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = 'fuck u'
            frame = cv2.putText(frame,datet,(1,400),font,1,(255,255,0),5,cv2.LINE_AA)
            out.write(frame)
        #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',frame)
            if cv2.waitKey(50) & 0xff == ord('q'):
                break
        else:
            break
    '''
    cap.release()
    cv2.destroyAllWindows()
    video()


def handle_mouse_events(event,x,y,flags,img):
    #events = [i for i in dir(cv2) if 'EVENT' in i]
    #print(1)
    #img = cv2.resize(img,(960,960))
    img1 = cv2.imread("ymd.jpg",1)
    img1 = cv2.resize(img1,(400,800))
    #cv2.imshow('img1',img1)
    if event == cv2.EVENT_LBUTTONDOWN:
        
        print(x,',',y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x) + ',' + str(y)
        #cv2.putText(img,strXY,(x,y),font,1,(0,0,0),1)
        
        #cv2.circle(img,(x,y),3,(255,255,0),-1,cv2.LINE_AA)
        #points.append((x,y))
        coordinate.append(x)
        coordinate.append(y)
        print(coordinate)
        
        if len(coordinate) >= 4 and len(coordinate) % 4 ==0:
            x1 = coordinate[-4]
            x2 = coordinate[-2]
            y1 = coordinate[-3]
            y2 = coordinate[-1]
            print('coordinate:',[x1,y1,x2,y2])
            be_copyed = img[y1:y2,x1:x2]
            #cv2.imshow('part',be_copyed)
            img1[300:y2-y1+300,100:x2-x1+100] = be_copyed 
            
        #if len(points) >= 2:
        #    cv2.line(img,points[-1],points[-2],(255,255,0),1,lineType = cv2.LINE_4)
        cv2.imshow('img1',img1)
    if event == cv2.EVENT_RBUTTONDOWN:
        blue = img[y,x,0]
        green = img[y,x,1]
        red = img[y,x,2]
        print(blue,green,red)
        new_img = np.zeros((512,512,3),np.uint8)
        new_img[:]=[blue,green,red]
        cv2.imshow('new',new_img)

def handle_mouse_events_API():
    #img = np.zeros((512,512,3),np.uint8)
    img = cv2.imread("123456.jpg",1)
    img = cv2.resize(img,(540,960))
    cv2.imshow('img0',img)   
    cv2.setMouseCallback('img0',handle_mouse_events,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    points = []
    coordinate = []
    handle_mouse_events_API()

def bitwise():
    #img1 = np.zeros((512,512,3),np.uint8)
    #img1 = cv2.rectangle(img1,(0,0),(250,250),(255,255,255),-1,cv2.LINE_4)
    img2 = cv2.imread("C:/Users/18269/OneDrive/Desktop/50318d121cbda516cfebdc57c29b0db.jpg",1)
    img2 = cv2.resize(img2,(512,512))
    img2 = cv2.bitwise_not(img2)
    cv2.imshow('img2',img2)
    cv2.imwrite("signment.jpg",img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    bitwise()
def nothing(x):
    pass

def bind_trackbar():
    #img = np.zeros((512,512,3),np.uint8)
    img = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",1)
    #print(img)
    b,g,r = cv2.split(img)
    cv2.namedWindow('img')
    cv2.createTrackbar('CP','img',10,400,nothing)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.createTrackbar('B','img',10,400,nothing)
    #cv2.createTrackbar('G','img',0,255,nothing)
    #cv2.createTrackbar('R','img',0,255,nothing)
    switch = r'color \ gray'
    cv2.createTrackbar(switch,'img',0,1,nothing)
    while(1):
        cv2.imshow('img',img)
        pos = cv2.getTrackbarPos('CP','img')
        cv2.putText(img,str(pos),(50,150),font,1,(0,0,0),1,cv2.LINE_4)
        #cv2.imshow('img',img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        b = cv2.getTrackbarPos('B','img')
        #g = cv2.getTrackbarPos('G','img')
        #r = cv2.getTrackbarPos('R','img')
        s = cv2.getTrackbarPos(switch,'img')
        if s == 0:
            img[:] = 0
        else:
            #blue_img = cv2.merge((b, np.zeros_like(b), np.zeros_like(b)))
            img[:] = [b,0,0]
            
    cv2.destroyAllWindows()

    #bind_trackbar()


def HSV():

    def nothing(x):
        pass
    cv2.namedWindow('Tracking')
    cv2.createTrackbar('LH','Tracking',0,255,nothing)
    cv2.createTrackbar('LS','Tracking',0,255,nothing)
    cv2.createTrackbar('LV','Tracking',0,255,nothing)
    cv2.createTrackbar('UH','Tracking',255,255,nothing)
    cv2.createTrackbar('US','Tracking',255,255,nothing)
    cv2.createTrackbar('UV','Tracking',255,255,nothing)
    cap = cv2.VideoCapture("C:/Users/18269/Desktop/record/gjl.mp4")
    while(1):
        #img = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",1)
       
        _,frame = cap.read()
        #cv2.imshow('img',img)
        
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv',hsv)
        l_h = cv2.getTrackbarPos('LH','Tracking')
        l_s = cv2.getTrackbarPos('LS','Tracking')
        l_v = cv2.getTrackbarPos('LV','Tracking')
        u_h = cv2.getTrackbarPos('UH','Tracking')
        u_s = cv2.getTrackbarPos('US','Tracking')
        u_v = cv2.getTrackbarPos('UV','Tracking')

        l_b = np.array([l_h,l_s,l_v])
        u_b = np.array([u_h,u_s,u_v])

        mask = cv2.inRange(hsv,l_b,u_b)
        cv2.imshow('mask',mask)
        res = cv2.bitwise_and(frame,frame,mask=mask)
        cv2.imshow('res',res)

        
        key = cv2.waitKey(1000)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    #HSV()

def img_threshold():  
    img = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg")
    img1 = img.copy()
    img1 = cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
    _,th1 = cv2.threshold(img1,40,255,0)
    #th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,1)
    contours,hierarchy = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    print(contours)
    print(hierarchy)
    th3 = cv2.drawContours(img,contours,9,(0,255,0),3)
    cv2.imshow('img',img)
    cv2.imshow('th1',th1)
    cv2.imshow('th3',th3)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img_threshold()

def plt_with_cv2():
    img1 = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",1)
    img2 = cv2.imread("C:/Users/18269/Desktop/record/yan.jpg",1)
    #cv2.imshow('img',img)
    titles = ['guo','yan']
    
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2HSV)
    images = [img1,img2]
    for i in range(2):
        plt.subplot(2,1,i+1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
   
    
    plt.show()
    k = cv2.waitKey(0) & 0xFF
    if k == ord('q'):
        cv2.destroyAllWindows()

    #plt_with_cv2()

def morphological_transformations(): #形态转变
    img1 = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",0)
    img = cv2.imread("C:/Users/18269/Desktop/record/yan.jpg",0)
    _,mask = cv2.threshold(img1,100,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((10,10),np.uint8)
    dilation = cv2.dilate(mask,kernel ,iterations = 2)
    erosion = cv2.erode(mask,kernel,iterations = 2)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    closing = cv2.morphologyEx(mask,cv2.MORPH_GRADIENT,kernel)
    img2 = cv2.bitwise_and(img1,img1,mask=mask)
    img3 = cv2.bitwise_and(img1,img1,mask=dilation)
    img4 = cv2.bitwise_and(img1,img1,mask = erosion)
    img5 = cv2.bitwise_and(img1,img1,mask = opening)
    img6 = cv2.bitwise_and(img1,img1,mask = closing)
    plt.subplot(3,3,1),plt.imshow(img,'gray')
    plt.subplot(3,3,2),plt.imshow(img1,'gray')
    plt.subplot(3,3,4),plt.imshow(mask,'gray')
    plt.subplot(3,3,5),plt.imshow(dilation,'gray')
    plt.subplot(3,3,6),plt.imshow(erosion,'gray')
    plt.subplot(3,3,7),plt.imshow(img2,'gray')
    plt.subplot(3,3,8),plt.imshow(img5,'gray')
    plt.subplot(3,3,9),plt.imshow(img6,'gray')
    #plt.subplot(3,3,7),plt.imshow(,'gray')
   
    #plt.subplot(3,3,9),plt.imshow(,'gray')
    plt.show()
    #cv2.imshow('img',img)
    cv2.waitKey(0)
    

    morphological_transformations()

def calculate_blur(image):
    # 读取图像
    if image is None:
        raise ValueError("无法读取图像，请检查图像路径。")

    # 计算拉普拉斯变换
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    
    # 计算拉普拉斯变换结果的方差
    variance = laplacian.var()
    
    return variance

def smooth_and_blurring():
    img = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",0)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)
    blur = cv2.blur(img,kernel.shape)
    gassuian = cv2.GaussianBlur(img,kernel.shape,0)
    midfilter = cv2.medianBlur(img,5)
    bilateralfilter = cv2.bilateralFilter(img,9,75,75)
    titles = ['smile','2D convolution','blur','gaussian','midfilter','bilateralfilter']
    images = [img,dst,blur,gassuian,midfilter,bilateralfilter]
    for i in range(6):

        plt.subplot(2,3,i+1)
        val = calculate_blur(images[i])
        plt.imshow(images[i])
        plt.title(titles[i]+str(val))
    plt.show()
    smooth_and_blurring()

def gradient_and_EdgeDetection():
    img = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",1)
    #img = cv2.imread('lena.jpg',1)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    lap = cv2.Laplacian(img,cv2.CV_64F,ksize = 3)
    lap = np.uint8(np.absolute(lap))

    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1)

    sobelx = np.uint8(np.absolute(sobelx))
    sobely = np.uint8(np.absolute(sobely))
   
    sobelcombined = cv2.bitwise_or(sobelx,sobely)
    cv2.namedWindow('img')
    cv2.createTrackbar('threshold1','img',0,100,nothing)
    cv2.createTrackbar('threshold2','img',200,255,nothing)
    plt.ion()
    while(1):
        threshold1 = cv2.getTrackbarPos('threshold1','img')
        threshold2 = cv2.getTrackbarPos('threshold2','img')
        canny = cv2.Canny(img,threshold1,threshold2)

        titles = ['smile','laplacian','sobelx','sobely','sobelcombined','canny']
        images = [img,lap,sobelx,sobely,sobelcombined,canny]
        for i in range(6):
            plt.subplot(2,3,i+1)
            plt.imshow(images[i])
            plt.title(titles[i])
       
        plt.show()
        plt.pause(0.1)
        plt.clf()
        
    gradient_and_EdgeDetection()


def pyramid():
    img = cv2.imread("C:/Users/18269/Desktop/record/gjl1.png",1)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    layer = img.copy()
    gp = [layer]

    for i in range(6):
        layer = cv2.pyrDown(layer)
        gp.append(layer)

    layer = gp[5]
    lp = [layer]
    for i in range(5,0,-1):
        gaussian_extended = cv2.pyrUp(gp[i])
        gaussian_extended = cv2.resize(gaussian_extended,dsize = (gp[i-1].shape[1],gp[i-1].shape[0]))
        laplacian = cv2.subtract(gp[i-1],gaussian_extended)
        lp.append(laplacian)
        cv2.imshow(str(i),laplacian)
    cv2.waitKey(0)
    
    lr = cv2.pyrDown(img)

    hr = cv2.pyrUp(img)
    titles = ['img','lr','hr']
    images = [img,lr,hr]
    '''
    for i in range(3):
        plt.subplot(2,2,i+1)
        plt.imshow(images[i])
        plt.title(titles[i])
        #plt.xticks([0,images[i].shape[1]])
        #plt.yticks([0,images[i].shape[0]])
        plt.xticks([0,600])
        plt.yticks([0,600])
    plt.show()
    '''
    #pyramid()

def blending_img():
    img1 = cv2.imread("C:/Users/18269/Desktop/record/biye.jpg",1)
    img2 = cv2.imread("C:/Users/18269/Desktop/record/smile.jpg",1)
    img2 = cv2.resize(img2,(img1.shape[1],img1.shape[0]))
    img1 = cv2.cvtColor(img1,cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2BGR)

    img1_copy = img1.copy()
    gp_1= [img1_copy]
    for i in range(6):
        img1_copy = cv2.pyrDown(img1_copy)
        gp_1.append(img1_copy)
    lp_1 = [gp_1[-1]]
    for i in range(5,0,-1):
        gaussian_extended = cv2.pyrUp(gp_1[i])
        gaussian_extended = cv2.resize(gp_1[i],dsize = (gp_1[i-1].shape[1],gp_1[i-1].shape[0]))
        laplacion_1 = cv2.subtract(gaussian_extended,gp_1[i-1])
        lp_1.append(laplacion_1)

    img2_copy = img2.copy()
    gp_2= [img2_copy]
    for i in range(6):
        img2_copy = cv2.pyrDown(img2_copy)
        gp_2.append(img2_copy)
    lp_2 = [gp_2[-1]]
    for i in range(5,0,-1):
        gaussian_extended = cv2.pyrUp(gp_2[i])
        gaussian_extended = cv2.resize(gp_2[i],dsize = (gp_2[i-1].shape[1],gp_2[i-1].shape[0]))
        laplacion_2 = cv2.subtract(gaussian_extended,gp_2[i-1])
        lp_2.append(laplacion_2)
    img_pyramid = []
    n = 0
    
    for lp_img1,lp_img2 in zip(lp_1,lp_2):
        n += 1
        cols,rows,ch = lp_img1.shape
        laplacian = np.hstack((lp_img1[:,0:int(rows/2)],lp_img2[:,int(rows/2):]))
        laplacian = np.vstack((lp_img1[0:int(cols/2),:],lp_img2[int(cols/2):,:]))
        if n == 1:
            plt.subplot(2,3,1),plt.imshow(lp_img1)
            plt.subplot(2,3,2),plt.imshow(lp_img2)
            plt.subplot(2,3,3),plt.imshow(laplacian)
            plt.subplot(2,3,4),plt.imshow(lp_1[0])
            plt.subplot(2,3,5),plt.imshow(lp_2[0])
        
        #plt.show()
        img_pyramid.append(laplacian)
        
    
    reconstract = img_pyramid[0]
    #cv2.imshow('1',reconstract)
    for i in range(1,6):
        reconstract = cv2.pyrUp(reconstract)
        
        #cv2.imshow('1',reconstract)
        k = cv2.waitKey(0) & 0xff
        if k == ord('c'):
            pass
        reconstract = cv2.resize(reconstract,(img_pyramid[i].shape[1],img_pyramid[i].shape[0]))
        reconstract = cv2.add(img_pyramid[i],reconstract)
        #plt.subplot(2,3,i),plt.imshow(img_pyramid[i-1])
    #plt.show()
    cv2.imshow('reconstract',reconstract)
    cv2.imwrite('reconstract.jpg',reconstract)
    #cv2.imshow('img2',img2)
    #cv2.imshow('two',two_img)
    k = cv2.waitKey(0) & 0xff
    if k == ord('q'):
        cv2.destroyAllWindows()

    blending_img()


def shape_detection():
    img = cv2.imread("C:/Users/18269/Desktop/record/shapes.jpg",1)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(img_gray,200,255,cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
        
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01 * cv2.arcLength(contour,True),True)
        cv2.drawContours(img,[contour],-1,(255,0,0),10,cv2.LINE_4)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) == 1:
            cv2.putText(img,'1',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),1,cv2.LINE_4)
        if len(approx) == 2:
            cv2.putText(img,'2',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),1,cv2.LINE_4)
        if len(approx) == 3:
           
            cv2.putText(img,'triangle',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),1,cv2.LINE_4)
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(approx)
            if float(w) / h < 0.95 or float(w) / h > 1.05:
                
                cv2.putText(img,'rectangle',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),1,cv2.LINE_4)
            else:
                cv2.putText(img,'square',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),1,cv2.LINE_4)
        if len(approx) > 4:
            cv2.putText(img,'circle',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),1,cv2.LINE_4)
    cv2.imshow('image',img)
    cv2.waitKey(0) & 0xff
    cv2.destroyAllWindows()
    shape_detection()

def histograms():
    img = cv2.imread("lena.jpg",1)
    
   
    #b,g,r = cv2.split(img)

    #plt.hist(b.ravel(),256,[0,256])
    #plt.hist(g.ravel(),256,[0,256])
    #plt.hist(r.ravel(),256,[0,256])
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    plt.plot(hist)
    
    plt.show()
    img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('img1',img1)
    k = cv2.waitKey(0) & 0xff
    if k == ord('q'):
        cv2.destroyAllWindows()

histograms()

def template_matching():
    img = cv2.imread("C:/Users/18269/Desktop/record/yan.jpg",1)
    
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    img_template = cv2.imread("C:/Users/18269/Desktop/record/yan_template.jpg",0)
    w,h = img_template.shape[::-1]
    
    #img_template = cv2.cvtColor(img_template,cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_grey,img_template,cv2.TM_CCOEFF_NORMED)
    
    threshold = 0.8
    loc = np.where(res > threshold)
    print(loc)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img,pt,(pt[0]+w,pt[1]+h),(255,0,0),1,cv2.LINE_4)
    plt.subplot(1,3,1),plt.imshow(img_grey)
    plt.subplot(1,3,2),plt.imshow(img_template)
    plt.subplot(1,3,3),plt.imshow(img)
    plt.show()
    k = cv2.waitKey(0) & 0xff
    if k == ord('q'):
        cv2.destroyAllWindows()
    template_matching()

def hough_line_transform():
    img = cv2.imread("C:/Users/18269/Desktop/record/yan.jpg",1)
    img = cv2.resize(img,(int(img.shape[1]/3),int(img.shape[0]/3)))
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray,50,250,apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,70)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,30,minLineLength = 50,maxLineGap = 5)
    canny = cv2.Canny(img,50,100)
    cv2.imshow('canny',canny)
    if lines is None:
        print('none')
    for line in lines:
        print(line)
        '''
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = int(a * rho)
        y0 = int(b * rho)
       
        x1 = int(x0 + 500 * (-b))
        y1 = int(y0 + 500 * (a))
        x2 = int(x0 - 500 * (-b))
        y2 = int(y0 - 500 * (a))
        '''
        x1,y1,x2,y2 = line[0]
        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
    cv2.imshow('img',img)
    cv2.imshow('img1',img_gray)
    k = cv2.waitKey(0) & 0xff
    if k ==ord('q'):
        cv2.destroyAllWindows()
    hough_line_transform()




