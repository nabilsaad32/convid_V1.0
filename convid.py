#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2021 nabil_saad <nabilsaad32@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os,gi,threading
import subprocess 
from ffmpy import FFmpeg

libs= ['Gtk','Gdk']
for lib in(libs):
	gi.require_version(lib, '3.0')
from gi.repository import Gtk,Gdk
 

screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path("./css/style.css")
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def convert():

	inp_name =getfile_button.get_filename()
	form= combo.get_active_text()
	out_name = str(os.path.basename(inp_name)).split('.')[0]+'.'+str(form)

	if inp_name == None:
		idj.set_text("[X]Enter the input file! ")
		exit()
	if form == None:
		idj.set_text("[X]You didn't choose a Format! ")
		exit()
	if os.path.exists(out_name)==True:
		idj.set_text("[X]File "+os.path.basename(inp_name)+" already exist")
		exit()
		
	f = ['mp3','mp4','webm','txt','png','jpg','jpeg']
	i = 0
	while i < len(f)-1:
		if inp_name.split('.')[1]==f[i]:
			idj.set_text("Unknown file format")
			os.system('sleep 1')
			break
		else:
			i+=1
	else:
		idj.set_text("Converting...")
		

	command = 'ffmpeg -i '+ '"'+inp_name +'"  "' + out_name +'" 2> ERROR.txt'
	process = subprocess.Popen(command,shell=True)

	while True:
		os.system('sleep 2')
		size = os.path.getsize(out_name)
		size = "{0:.2f}".format(size/1000000)+"MB"
		
		inp_size = os.path.getsize(inp_name)
		inp_size = "{0:.2f}".format(inp_size/1000000)+"MB"  
		
		oldsize = idj.get_text()
		prog = ("[*]Converting: from "+inp_name.split('.')[1]+" to "+form+"\n[*]Original file size: "+inp_size+"\n[*]New File size: "+size)
		if oldsize != str(prog):
			idj.set_text (prog)
			
		else:
			idj.set_text (prog+"\n[*]Finish")
			break
	process.wait()

	#
	
def change_entry(widget):
	os.system('sleep 2')
	inp_name = str(getfile_button.get_filename())
	inp_name = os.path.basename(inp_name).split('.')[0]
	entry.set_text(inp_name)


win = Gtk.Window()
win.set_title('converter')
box = Gtk.VBox()
hbox= Gtk.HBox()

nothing = Gtk.Label()
asktochoos = Gtk.Label()
asktochoos.set_text("Input file: ")
getfile_button =Gtk.FileChooserButton('choosfile')

asktype = Gtk.Label()
asktype.set_text("Format: ")
combo = Gtk.ComboBoxText()
askfilename = Gtk.Label()
askfilename.set_text("Output file: ")
entry = Gtk.Entry()
idj = Gtk.Label()
idj.set_line_wrap(True) 
OK = Gtk.Button('OK')

for widget in(asktochoos,getfile_button,asktype,combo,askfilename,entry,OK,idj):
	box.pack_start(widget,False,False,0)
	widget.set_margin_left(5)
	widget.set_margin_right(5)
	widget.set_margin_top(5)
for form in('mp3','mp4','webm','wav','midi','mkv','ogg','avi'):
	combo.append('1',form)



for widget in [asktochoos,asktype,askfilename,OK]:
	widget.set_valign(Gtk.Align.CENTER)
	widget.set_name('label')
	widget.set_margin_left(5)
	widget.set_margin_right(5)
	widget.set_margin_top(5)
	
idj.set_name('label2')

for widget in [getfile_button,combo]:
	widget.set_name('choos')
	widget.set_size_request(1,10)
entry.set_name('entry')
OK.set_name('button')

idj.set_text('  \nConvert Media files format using ffmpeg\n  ')
win.set_name('window')
hbox.pack_start(nothing,False,False,0)
hbox.pack_start(box,False,False,0)
hbox.pack_start(nothing,False,False,0)
box.set_valign(Gtk.Align.CENTER)
box.set_margin_left(10)
box.set_margin_right(10)


win.add(hbox)
win.resize(300,380)
win.set_icon_from_file('./icon.png')
win.connect('destroy', lambda w: Gtk.main_quit())
getfile_button.set_width_chars(22)
win.show_all()

def run(widget):
	threading.Thread(target=convert).start()
OK.connect('clicked',run)
getfile_button.connect('file-set',change_entry)
if __name__=='__main__':
	Gtk.main()
