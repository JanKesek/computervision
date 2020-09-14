from pyrobot import Robot
robot=Robot()
monitors=robot.get_display_monitors()
print(monitors)
print(len(monitors))
im=robot.take_screenshot(monitors[-1])
im.save('screenshotwhatever.png','png')
imcrop=im.crop((0,0,1000,1000))
imcrop.save("screenshotcropexample.png",'png')