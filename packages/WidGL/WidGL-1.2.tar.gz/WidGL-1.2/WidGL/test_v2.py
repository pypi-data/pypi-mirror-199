from pygl_nf import GL

from WidGL import Styles_loader,wrapper
# python      version 3.10.4
# pygl_nf     version 21.8


win = GL.Display_init_(flags=GL.D_Resize,size=[700,400])
 
style = Styles_loader.LoadFile('WidGL\style.txt',win)

w = wrapper.Wrapper(style,win)


while win.CEUF(FPS=1000):
    w.Render()
    
    

    
    
    