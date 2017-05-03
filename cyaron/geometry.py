from .utils import *
from .consts import *
import random

class Geometry:
    @staticmethod
    def convex_hull(n,**kwargs):
        #fx, fy are functions which map [0,1] to int or float
        fx = kwargs.get("fx", lambda x:x)
        fy = kwargs.get("fy", lambda x:x)
        sz=n*2
        result=[]
        while len(result)<n:
            points=[]
            #about 10 points will be randomized
            randomize_prob=sz/10+1
            if randomize_prob<10:
                randomize_prob=10
            for i in range(0,sz):
                angle=random.uniform(0,2*PI)
                x=0.5+math.cos(angle)*0.48
                y=0.5+math.sin(angle)*0.48
                if random.randint(0,randomize_prob)==0:
                    x=x+random.uniform(-0.005,0.005)
                    y=y+random.uniform(-0.005,0.005)
                points.append([fx(x),fy(y)])
            #compute convex hull for points and store in rst
            points=sorted(points)
            #unique
            tmp=[]
            for i in range(0,len(points)):
                if i==0 or points[i-1]!=points[i]:
                    tmp.append(points[i])
            points=tmp
            st=[] #stack
            for i in range(0,len(points)):
                while len(st)>=2:
                    a=st[len(st)-1]
                    b=points[i]
                    o=st[len(st)-2]
                    if (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])>=0:
                        break
                    st.pop()
                st.append(points[i])
            g=len(st)+1
            for i in range(0,len(points)-1)[::-1]:
                while len(st)>=g:
                    a=st[len(st)-1]
                    b=points[i]
                    o=st[len(st)-2]
                    if (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])>=0:
                        break
                    st.pop()
                st.append(points[i])
            result=st
            sz=int(sz*1.7)+3  #if failed, increase size and try again
        random.shuffle(result)
        result=result[0:n]
        return result
    #find a path from points[0] to points[1] and cross all points in [points]
    @staticmethod
    def __conquer(points):
        if len(points)<=2:
            return points
        divide_id=random.randint(2,len(points)-1)
        divide_point1=points[divide_id]
        divide_k=random.uniform(0.01,0.99)
        divide_point2=[divide_k*(points[1][0]-points[0][0])+points[0][0],
                       divide_k*(points[1][1]-points[0][1])+points[0][1]]
        #path: points[0]->points[divide]->points[1]
        #dividing line in the form Ax+By+C=0
        divide_line=[divide_point2[1]-divide_point1[1],
                     divide_point1[0]-divide_point2[0],
                     -divide_point1[0]*divide_point2[1]
                     +divide_point1[1]*divide_point2[0]]
        p0=(divide_line[0]*points[0][0]+divide_line[1]*points[0][1]+divide_line[2]>=0)
        p1=(divide_line[0]*points[1][0]+divide_line[1]*points[1][1]+divide_line[2]>=0)
        if p0==p1: #the divide point isn't good enough...
            return __conquer(points)
        s=[[],[]]
        s[p0].append(points[0])
        s[p0].append(divide_point1)
        s[not p0].append(divide_point1)
        s[not p0].append(points[1])
        for i in range(2,len(points)):
            if i==divide_id:
                continue
            pt=(divide_line[0]*points[i][0]+divide_line[1]*points[i][1]+divide_line[2]>=0)
            s[pt].append(points[i])
        pa=Geometry.__conquer(s[p0])
        pb=Geometry.__conquer(s[not p0])
        pb.pop(0)
        return pa+pb
    #generate simple polygon from given points (int[2] or float[2])
    #O(nlogn)~O(n^2)
    @staticmethod
    def simple_polygon(points):
        if not list_like(points):
            raise Exception("source point is not a list")
        random.shuffle(points)
        if len(points)<3:
            return points
        #divide by points[0], points[1]
        divide_line=[points[1][1]-points[0][1],
                     points[0][0]-points[1][0],
                     -points[0][0]*points[1][1]
                     +points[0][1]*points[1][0]]
        s=[[],[]]
        s[0].append(points[0])
        s[0].append(points[1])
        s[1].append(points[1])
        s[1].append(points[0])
        for i in range(2,len(points)):
            pt=(divide_line[0]*points[i][0]+divide_line[1]*points[i][1]+divide_line[2]>=0)
            s[pt].append(points[i])
        pa=Geometry.__conquer(s[0])
        pb=Geometry.__conquer(s[1])
        pa.pop(0)
        pb.pop(0)
        return pa+pb
