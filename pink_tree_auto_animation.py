from PIL import Image, ImageDraw
import numpy as np
import random

random.seed(12)
branches, buds = [], []

def grow(x, y, angle, length, depth, width):
    if depth == 0 or length < 0.012:
        buds.append((x, y, random.uniform(0.012, 0.025)))
        return
    nx, ny = x + length*np.cos(angle), y + length*np.sin(angle)
    branches.append(((x,y),(nx,ny),width))
    if depth <= 2:
        buds.append((nx,ny,random.uniform(0.010,0.018)))
    spread = 0.42 + random.uniform(-0.08,0.08)
    if depth > 2:
        lengths, turns = [length*0.78,length*0.73],[-spread,spread]
    else:
        lengths = [length*0.68,length*0.62,length*0.55]
        turns = [-spread*1.15,0.05,spread*1.15]
    for L,T in zip(lengths,turns):
        grow(nx,ny,angle+T+random.uniform(-0.08,0.08),L,depth-1,width*0.72)

grow(0,-1,np.pi/2,0.62,7,4.0)

SIZE=480
def to_pixel(p):
    x,y=p
    return (int((x+1.25)/2.5*SIZE),int((1.45-y)/2.57*SIZE))

def draw_frame(branch_count, bloom):
    image=Image.new("RGB",(SIZE,SIZE),"black")
    draw=ImageDraw.Draw(image)
    for p1,p2,width in branches[:branch_count]:
        a,b=to_pixel(p1),to_pixel(p2)
        thick=max(1,int(width*1.5))
        draw.line([a,b],fill="#7d2630",width=thick)
        draw.line([a,b],fill="#d45b68",width=max(1,int(thick*.28)))
    for x,y,size in buds[:int(len(buds)*bloom)]:
        px,py=to_pixel((x,y))
        r=max(2,int(size*SIZE*.55))
        draw.ellipse((px-r,py-r,px+r,py+r),fill="#f5a6b0",outline="#ffd4d9")
        draw.ellipse((px-1,py-1,px+1,py+1),fill="#fff0f2")
    return image

frames=[]
step=max(1,len(branches)//42)
for count in range(0,len(branches)+1,step):
    frames.append(draw_frame(min(count,len(branches)),0))
for step in range(1,11):
    frames.append(draw_frame(len(branches),step/10))
frames.append(draw_frame(len(branches),1))
frames[0].save("pink_tree_growing_step_by_step.gif",save_all=True,
               append_images=frames[1:],duration=85,loop=0,optimize=True)
print("Animation saved!")
