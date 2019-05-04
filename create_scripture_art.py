import os
import re
import csv
import math
import glob
import random
import colorsys
import scriptures
from Tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageFont
from PIL import ImageDraw

class ScriptureArt():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("Scripture Art")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=FALSE, height=FALSE)

        # initialize global state
        self.csv_book = './bible/key_english.csv'
        self.csv_verse = './bible/t_asv.csv'
        self.dir_bg = './bg/'
        self.dir_font = './font/'
        self.dir_out = './output/'
        self.img_margin_x_rat = 0.1
        self.img_margin_y_rat = 0.1
        self.num_step_avg_color = 100
        self.img_disp_size = (1280, 720)
        self.num_char_max = 1024
        self.scripture = ''
        self.text_scripture = ''
        self.quote_scripture = ''
        self.list_bg = []
        self.list_font = []
        self.idx_bg = -1
        self.idx_font = -1
        self.bg_wid_val = 0
        self.bg_hei_val = 0
        self.img = None
        self.tkimg = None

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text="Scripture quote:")
        self.label.grid(row=0, column=0, sticky=E)
        self.entry = Entry(self.frame)
        self.entry.grid(row=0, column=1, sticky=W + E)
        self.ldBtn = Button(self.frame, text="Create", command=self.initScriptureArt)
        self.ldBtn.grid(row=0, column=2, sticky=W + E)

        # main panel
        self.mainPanel = Canvas(self.frame, cursor='arrow')
        #self.parent.bind("n", self.next)  # press 'a' to go next
        #self.parent.bind("s", self.save)  # press 's' to save
        self.mainPanel.grid(row=1, column=1, rowspan=4, sticky=W + N)

        # control panel for going next and saving image
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row=5, column=1, columnspan=2, sticky=W + E)
        self.nextBtn = Button(self.ctrPanel, text='Next', width=10, command=self.next)
        self.nextBtn.pack(side=LEFT, padx=5, pady=3)
        self.saveBtn = Button(self.ctrPanel, text='Save', width=10, command=self.save)
        self.saveBtn.pack(side=LEFT, padx=5, pady=3)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side=RIGHT)

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(4, weight=1)

    def initScriptureArt(self):
        # load Bible books
        print("Loading Bible books...")
        dict_book = {}
        with open(self.csv_book, 'rb') as f:
            reader = csv.reader(f)
            flag_1st_row = True
            for row in reader:
                if flag_1st_row:
                    flag_1st_row = False
                else:
                    dict_book[row[1]] = int(row[0])
        #print(dict_book)

        # load Bible verses
        print("Loading Bible verses...")
        dict_verse = {}
        list_id = []
        with open(self.csv_verse, 'rb') as f:
            reader = csv.reader(f)
            flag_1st_row = True
            for row in reader:
                if flag_1st_row:
                    flag_1st_row = False
                else:
                    dict_verse[row[0]] = row[4]
                    list_id.append(row[0])
        #print(dict_verse)

        # input scripture and extract the text
        # get txt file list
        self.scripture = scriptures.extract(self.entry.get())
        assert(len(self.scripture) == 1)
        self.scripture = self.scripture[0]
        id_book = dict_book[self.scripture[0]]
        key_verse_bgn = "%d%03d%03d" % (id_book, self.scripture[1], self.scripture[2])
        key_verse_end = "%d%03d%03d" % (id_book, self.scripture[3], self.scripture[4])
        idx_verse_bgn = list_id.index(key_verse_bgn)
        idx_verse_end = list_id.index(key_verse_end)
        for i in range(idx_verse_bgn, idx_verse_end+1):
            self.text_scripture += dict_verse[list_id[i]].rstrip() + ' '

        # handle long scripture
        if (len(self.text_scripture) > self.num_char_max):
            print("The scripture is too long. Please try another one.")
            return

        print(self.text_scripture)

        # get quote of the scripture
        self.quote_scripture = '- ' + scriptures.reference_to_string(self.scripture[0], self.scripture[1], 
                          self.scripture[2], self.scripture[3], self.scripture[4])

        print(self.quote_scripture)

        # read the databases of background iamges and fonts
        self.list_bg = glob.glob(self.dir_bg + "*")
        self.list_font = glob.glob(self.dir_font + "*")

        self.genScriptureArt()

    def genScriptureArt(self):
        # input background image
        self.idx_bg = random.randint(0, len(self.list_bg))
        name_bg = self.list_bg[self.idx_bg]
        #print(name_bg)
        self.img = Image.open(name_bg)
        bg_size = self.img.size
        self.bg_wid_val = bg_size[0] * (1 - self.img_margin_x_rat)
        self.bg_hei_val = bg_size[1] * (1 - self.img_margin_y_rat)
        # compute average color of the background
        r, g, b = 0, 0, 0
        count = 0
        for x in range(0, bg_size[0], bg_size[0] / self.num_step_avg_color):
            for y in range(0, bg_size[1], bg_size[1] / self.num_step_avg_color):
                pixlr, pixlg, pixlb = self.img.getpixel((x, y))
                r += pixlr / 255.
                g += pixlg / 255.
                b += pixlb / 255.
                count += 1
        h, s, v = colorsys.rgb_to_hsv((r/count), (g/count), (b/count))

        # compute contrastive color for the text
        h = (h + 0.5) % 1.0
        s = (s + 0.5) % 1.0
        v = (v + 0.5) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        color_text = (int(r*255), int(g*255), int(b*255))

        # input font
        self.idx_font = random.randint(0, len(self.list_font))
        name_font = self.list_font[self.idx_font]
        #print(name_font)
        num_line = 2
        while True:
            try:
                font = ImageFont.truetype(name_font, size=int(self.bg_hei_val/num_line), encoding="unic")
            except IOError:
                num_line += 1
            else:
                num_line_real = math.ceil(font.getsize(self.text_scripture)[0] / self.bg_wid_val)
                num_line_real += math.ceil(font.getsize(self.quote_scripture)[0] / self.bg_wid_val)
                if num_line_real <= num_line:
                    if font.getsize('hg')[1] * num_line_real < self.bg_hei_val:
                        break
                num_line += 1

        # split a long text into multiple lines
        lines = []
        lines = self.splitText(self.text_scripture, lines, font)
        lines = self.splitText(self.quote_scripture, lines, font)

        # ensure the text is overlaid in the middle of the image
        draw = ImageDraw.Draw(self.img)
        y = int((bg_size[1] / 2.) - (font.getsize('hg')[1] * len(lines) / 2.))
        x = int(bg_size[0] * self.img_margin_x_rat / 2)
        for line in lines:
            # draw the line on the image
            draw.text((x, y), line, fill=color_text, font=font)
            # update the y position so that we can use it for next line
            y = y + font.getsize('hg')[1]

        # put the image into the center of the main panel
        img_disp = Image.new('RGB', self.img_disp_size, (240, 240, 240))
        img_rat_ori = float(bg_size[0]) / float(bg_size[1])
        img_rat_new = float(self.img_disp_size[0]) / float(self.img_disp_size[1])
        if (img_rat_new < img_rat_ori):
            hei_resize =  self.img_disp_size[0] * bg_size[1] / bg_size[0]
            img_resize = self.img.resize((self.img_disp_size[0], hei_resize), Image.ANTIALIAS)
            x = 0
            y = (self.img_disp_size[1] / 2) - (hei_resize / 2)
            img_disp.paste(img_resize, (x, y))
        else: 
            wid_resize =  self.img_disp_size[1] * bg_size[0] / bg_size[1]
            img_resize = self.img.resize((wid_resize, self.img_disp_size[1]), Image.ANTIALIAS)
            x = (self.img_disp_size[0] / 2) - (wid_resize / 2)
            y = 0
            img_disp.paste(img_resize, (x, y))
        self.tkimg = ImageTk.PhotoImage(img_disp)
        self.mainPanel.config(width=self.img_disp_size[0], height=self.img_disp_size[1])
        self.mainPanel.create_image(0, 0, image=self.tkimg, anchor=NW)

    def splitText(self, text, lines, font):
        if font.getsize(text)[0] <= self.bg_wid_val:
            lines.append(text) 
        else:
            # split the line by spaces to get words
            words = text.split(' ')  
            i = 0
            # append every word to a line while its width is shorter than image width
            while i < len(words):
                line = ''         
                while i < len(words) and font.getsize(line + words[i])[0] < self.bg_wid_val:                
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                # when the line gets longer than the max width do not append the word, 
                # add the line to the lines array
                lines.append(line)
        return lines

    def next(self, event=None):
        self.genScriptureArt()

    def save(self, event=None):
        # create the output directory if it does not exist
        if not os.path.exists(self.dir_out):
            os.mkdir(self.dir_out)
        # save the output image
        print('Saving image ' + '%04d_%04d.jpg...' % (self.idx_bg, self.idx_font))
        self.img.save((self.dir_out + '%04d_%04d.jpg' % (self.idx_bg, self.idx_font)), optimize=True)

if __name__ == '__main__':
    root = Tk()
    tool = ScriptureArt(root)
    root.resizable(width=True, height=True)
    root.mainloop()