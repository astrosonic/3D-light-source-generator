import cv2 as cv
import numpy as np
import sys

def normalizer(lenght,mu,sigma,max_val=20):
    "Using standard distribution to increase the value in HSV"
    temp=np.arange(0,lenght)
    temp=np.exp( - (temp - mu)**2 / (2 * sigma**2) )/(sigma * np.sqrt(2 * np.pi))
    slope=max_val/(max(temp)-min(temp))
    intercept=max_val-(max(temp)*max_val/(max(temp)-min(temp)))
    temp=temp*slope+intercept
    return temp    

def func(a,b):
    "Add if initial value is less than val"   
    if(a>100 or a<1):
        return a
    else:
        return a+b
    
def find_angle(x,y):
    return x*y/180.0

def main(args):
    image=args[0]
    assert image!=None
    image=cv.imread(image)
    new=cv.cvtColor(image,cv.COLOR_BGR2HSV)
    value=int(args[1])
    axis=int(args[2])
    angle1=int(args[3])
    assert 0<=axis<=1
    assert 0<=angle1<=180
    if(axis):
        for i in range(new[:,:,2].shape[0]):
            angle=find_angle(len(new[i,:,2]),angle1)
            temp=normalizer(len(new[i,:,2]),angle,sigma=len(new[i,:,2])/5,max_val=value)
            vec=np.vectorize(func)
            copy=new[i,:,2].copy()
            _,mask=cv.threshold(copy,0,255,cv.THRESH_BINARY)
            copy=cv.bitwise_and(copy,copy,mask=mask)
            x=vec(copy,temp)
            new[i,:,2]=x
    else:
        mask=new[new[:,:,2]<50]
        for i in range(new[:,:,2].shape[1]):
            angle=find_angle(len(new[:,i,2]),angle1)
            temp=normalizer(len(new[:,i,2]),angle,sigma=len(new[:,i,2])/5,max_val=value)
            vec=np.vectorize(func)
            copy=new[:,i,2].copy()
            _,mask=cv.threshold(copy,0,255,cv.THRESH_BINARY)
            copy=cv.bitwise_and(copy,copy,mask=mask)
            x=vec(new[:,i,2],temp)
            new[:,i,2]=x
    new=cv.cvtColor(new,cv.COLOR_HSV2BGR)
    cv.imshow("image",new)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
if __name__=="__main__":
    main(sys.argv[1:])