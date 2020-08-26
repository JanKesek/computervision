import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
class CropApp:
	def __init__(self,screensh):
		self.xy={}
		self.root = tk.Tk()
		self.root.attributes('-fullscreen', True)
		self.root.bind("<Button 1>",self.getorigin)
		background_image=ImageTk.PhotoImage(screensh)
		background_label = tk.Label(self.root, image=background_image)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.root.mainloop()
	def getorigin(self,eventorigin):
		if 'x1' not in self.xy:
			self.xy['x1']=eventorigin.x
			self.xy['y1']=eventorigin.y
		else:
			self.xy['x2']=eventorigin.x
			self.xy['y2']=eventorigin.y
			print(self.xy)
			self.root.destroy()
if __name__ == "__main__":
	imgFull=ImageGrab.grab(all_screens=True)
	app=CropApp(imgFull)
	x1,y1,x2,y2=app.xy.values()
	if x2<x1 or y2<y1:
		x1,x2=x2,x1
		y1,y2=y2,y1
	img=imgFull.crop((x1,y1,x2,y2))
	img.save("test.png")