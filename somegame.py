import random,name2

class Location:
	def __init__(self,namegen):
		self.name=namegen.generate("city")

class Game:
	def __init__(self):
		self.namegen=name2.generator()
		self.locations=[]

import gtk
import sys
import gobject

#Mainmenu
#-Game
#--New
#--Save
#--Load
#--SaveQuit
#--Quit
#-View
#--About
#--Stats
#--Logs
#-Help
#--Tutorial

#stats
#experience
#inventory
#actiontext
#progress

class textedit:
	#def newfile_activate_cb(self, widget, data=None):
	#	self.tabs.delete()
	def motnot(self,widget,data=None):
		self.exp.set_property('fraction',min(1.0,self.exp.get_property('fraction')+0.025))
	def New_activate_cb(self,widget,data=None):
		self.exp.set_property('fraction',0.5)
	def window_destroy_cb(self, widget, data=None):
		gtk.main_quit()
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("gamewindow.glade")
		self.window = builder.get_object("window")
		self.actiontext = builder.get_object("actiontext")
		self.exp = builder.get_object("experience")
		#self.tabs = builder.get_object("drawarea")
		builder.connect_signals(self)

if __name__ == "__main__":
	editor = textedit()
	editor.window.show()
	#editor.window.height=640
	#editor.window.width=480
	gtk.main()
