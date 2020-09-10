from pyrobot import Robot
robot=Robot()
monitors=robot.get_display_monitors()
print(monitors)

im=robot.take_screenshot(monitors[-1])
im.save('screenshotwhatever.png','png')