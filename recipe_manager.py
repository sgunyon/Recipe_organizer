#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox
import os
import sys
import json


class Mainwindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.add_icon()
        self.cwd = os.getcwd()
        self.recipe_path = (os.path.join(self.cwd, 'Recipes'))
        self.geometry('375x320')
        self.create_list_fields()
        self.text = Text(self)
        container = self.create_container()
        self.create_pages(container)
        self.show_frame('Page_one')

    def add_icon(self):
        if sys.platform == 'win32':
            self.iconbitmap(os.path.join('icons', 'icon.ico'))
        elif sys.platform == 'darwin':
            self.iconbitmap(os.path.join('icons', 'icon.icns'))
        elif sys.platform == 'linux':
            self.iconbitmap(os.path.join('icons', 'icon.xbm'))

    def create_list_fields(self):
        self.recipe_dict = {
            'name': StringVar(),
            'time': IntVar(),
            'ingredients': StringVar(),
            'category' : StringVar(),
            'directions': StringVar()
        }

        self.option_list = ['All', 'Breakfast', 'Lunch', 'Dinner']

        self.vcmd = (self.register(self.on_validate), '%S')

    def on_validate(self, S):
        self.text.delete('1.0', 'end')
        self.text.insert('end','on_validate:\n')
        self.text.insert('end',"S='%s'\n" % S)

        if S.isdigit() or S == '.':
            return True
        else:
            self.bell()
            return False

    def create_container(self):
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        return container

    def create_pages(self, container):
        for F in (Page_one, Page_two):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_geo_page_one(self):
        self.geometry('375x320')

    def set_geo_page_two(self):
        self.geometry('820x470')


class Page_one(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.create_entry_fields()
        self.create_entry_labels()
        self.create_buttons()

    def create_entry_fields(self):
        self.entry = Entry(self, width=25, bd=3)
        self.entry.grid(row=1, column=1, pady=5)
        self.entry_th = Entry(self, width=3, bd=3, validate='key', validatecommand=self.controller.vcmd)
        self.entry_th.insert(0, '0')
        self.entry_th.grid(row=2, column=1, pady=5, padx=40, sticky=NW)
        self.entry_tm = Entry(self, width=3, bd=3, validate='key', validatecommand=self.controller.vcmd)
        self.entry_tm.insert(0, '0')
        self.entry_tm.grid(row=2, column=1, pady=5, padx=5, sticky=SE)
        self.entry_i = Entry(self, width=25, bd=3)
        self.entry_i.grid(row=3, column=1, pady=5)
        self.entry_ol = StringVar()
        self.entry_ol.set(self.controller.option_list[0])
        self.entry_c = OptionMenu(self, self.entry_ol, *self.controller.option_list, command=self.opt_menu_update)
        self.entry_c.config(bd=3)
        self.entry_c.grid(row=4, column=1, pady=5, sticky=N)
        self.entry_d = Text(self, height=10, width=19, bd=3)
        self.entry_d.grid(row=5, column=1, pady=5)

    def create_entry_labels(self):
        self.lbl = Label(self, text='Name', fg='black')
        self.lbl.grid(row=1, column=0, padx=30)
        self.lbt = Label(self, text='Total Time', fg='black')
        self.lbt.grid(row=2, column=0)
        self.lbth = Label(self, text='Hours', fg='black')
        self.lbth.grid(row=2, column=1, sticky=W)
        self.lbtm = Label(self, text='Minutes', fg='black')
        self.lbtm.grid(row=2, column=1, sticky=E, padx=40)
        self.lbi = Label(self, text='Ingredients', fg='black')
        self.lbi.grid(row=3, column=0)
        self.lbc = Label(self, text='Category', fg='black')
        self.lbc.grid(row=4, column=0)
        self.lbd = Label(self, text='Directions', fg='black')
        self.lbd.grid(row=5, column=0)

    def create_buttons(self):
        self.button = Button(self, text='View Recipe List', command=lambda: [self.controller.show_frame('Page_two'), self.controller.set_geo_page_two()])
        self.button.config(bd=3)
        self.button.grid(row=1, column=3)
        self.button2 = Button(self, text='Save Recipe', command=lambda: [self.save_recipe()])
        self.button2.config(bd=3)
        self.button2.grid(row=2, column=3)

    def clear_entries(self):
        self.entry.delete(0, 'end')
        self.entry_tm.delete(0, 'end')
        self.entry_tm.insert(0, 0)
        self.entry_th.delete(0, 'end')
        self.entry_th.insert(0, 0)
        self.entry_i.delete(0, 'end')
        self.entry_ol.set(self.controller.option_list[0])
        self.entry_d.delete(1.0, END)
        self.entry.focus()

    def print_names(self):
        name = self.entry.get()
        self.controller.listbox('end', name)

    def opt_menu_update(self, value):
        for i in self.controller.option_list:
            if value == i:
                self.c_name = i

    def create_py_dict(self):
        f_name = self.entry.get()
        t_name = [int(self.entry_th.get()), int(self.entry_tm.get())]
        i_name = self.entry_i.get()
        try:
            self.c_name
        except:
            self.c_name = 'All'
        c_name = self.c_name
        d_name = self.entry_d.get('1.0', END)

        self.recipe_list = [f_name, t_name, i_name, c_name, d_name]
        self.save_pydict = self.controller.recipe_dict

        count = 0
        for key in self.save_pydict:
            self.save_pydict[key] = self.recipe_list[count]
            count+=1

        return f_name

    def save_recipe(self):
        if not os.path.exists(self.controller.recipe_path):
            os.makedirs(self.controller.recipe_path)

        if os.getcwd() != self.controller.recipe_path:
            os.chdir(self.controller.recipe_path)

        json_file_name = self.create_py_dict()

        for i in self.recipe_list:
            if len(i) > 1:
                continue
            else:
                self.bell()
                messagebox.showinfo('Error',
                                    'Please fill out all of the fields')
                return

        with open(json_file_name + '.json', 'w') as f:
            json.dump(self.save_pydict, f)
        self.clear_entries()
        self.controller.editing = 0

class Page_two(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.button3 = Button(self, text='Return Home',
                            command=lambda: [controller.show_frame('Page_one'),
                            self.controller.set_geo_page_one()])
        self.button3.grid(row=0, column=0)

        self.button4 = Button(self, text='Load Recipe',
                            command=lambda:[controller.show_frame('Page_two'),
                            self.load_recipe()])
        self.button4.grid(row=1, column = 0)

        self.button5 = Button(self, text='All Recipes',
                              command=lambda: [self.display_saved_recipes(),
                              self.cat_ol_var.set('All')])
        self.button5.grid(row=0, column=1)
        self.button6 = Button(self, text='Delete Recipe',
                              command=lambda: [self.delete_recipe(),
                              self.display_saved_recipes()])
        self.button6.grid(row=0, column=3, stick=E)
        self.button7 = Button(self, text='Edit Recipe',
                              command=lambda: [self.edit_recipe()])
        self.button7.grid(row=1, column=3, sticky=E)
        self.cat_ol_var = StringVar()
        self.cat_ol_var.set('All')
        self.cat_ol = OptionMenu(self, self.cat_ol_var,
                                *self.controller.option_list,
                                command=self.refine_recipe_list)
        self.cat_ol.grid(row=1, column=1)

        self.listbox = Listbox(self, height=24)
        self.listbox.grid(row=2, column=0, columnspan=2, rowspan=2)

        self.recipe_box = Text(self)
        self.recipe_box.config(wrap=WORD)
        self.recipe_box.grid(row = 2, column = 2, columnspan = 2)

        self.display_saved_recipes()

    def display_saved_recipes(self):
        self.listbox.delete(0, END)
        if not os.path.exists(self.controller.recipe_path):
            os.makedirs(self.controller.recipe_path)
        count = 0
        for filename in os.listdir(self.controller.recipe_path):
            self.listbox.insert(count, os.path.splitext(filename)[0])
            count+=1

    def load_recipe(self):
        self.recipe_box.delete(1.0, END)
        select = self.listbox.get('active')
        json_file = os.path.join(self.controller.recipe_path, select) + '.json'
        with open(json_file, 'r') as f:
            data = f.read()

        json_recipe = json.loads(data)

        for item in json_recipe:
            if item == 'name':
                self.recipe_box.insert(
                    END,'{} \n\n'.format(json_recipe.get(item)))
            if item == 'time':
                self.recipe_box.insert(END,'Estimated Time:\n')
                t_list = json_recipe.get(item)
                if t_list[0] > 0 and t_list[1] > 0:
                    self.recipe_box.insert(
                        END,'{} hours and {} minutes \n\n'.format
                        (t_list[0], t_list[1]))
                elif t_list[0] == 0:
                    self.recipe_box.insert(
                        END,'{} minutes \n\n'.format(t_list[1]))
                elif t_list[1] == 0:
                    self.recipe_box.insert(
                        END,'{} hours \n\n'.format(t_list[0]))
                else:
                    self.recipe_box.insert(
                        END,'{}:{} \n\n'.format(t_list[0], t_list[1]))
            if item == 'ingredients':
                self.recipe_box.insert(
                    END,'Ingredients:\n{} \n\n'.format(json_recipe.get(item)))
            if item == 'directions':
                self.recipe_box.insert(
                    END,'Directions:\n{} \n'.format(json_recipe.get(item)))

    def refine_recipe_list(self, value):
        self.listbox.delete(0, END)
        self.recipe_box.delete(1.0, END)
        if not os.path.exists(self.controller.recipe_path):
            os.makedirs(self.controller.recipe_path)
        count = 0
        for filename in os.listdir(self.controller.recipe_path):
            json_file = os.path.join(self.controller.recipe_path, filename)
            with open(json_file, 'r') as f:
                data = f.read()
            json_recipe = json.loads(data)
            if value == 'All':
                self.display_saved_recipes()
            elif json_recipe['category'] == value:
                self.listbox.insert(count, os.path.splitext(filename)[0])
                count+=1

    def delete_recipe(self):
        select = self.listbox.get('active')
        if messagebox.askyesno('Confirm',
                            'Are you sure you want to delete '
                            + os.path.splitext(select)[0] + '?'):
            rmv = (os.path.join(self.controller.recipe_path, select) + '.json')
            os.remove(rmv)

    def edit_recipe(self):
        self.controller.frames['Page_one'].clear_entries()
        select = self.listbox.get('active')
        json_file = os.path.join(self.controller.recipe_path, select) + '.json'
        with open(json_file, 'r') as f:
            data = f.read()

        json_recipe = json.loads(data)
        page_one = self.controller.frames['Page_one']
        for item in json_recipe:
            if item == 'name':
                page_one.entry.insert(0, json_recipe.get(item))
            if item == 'time':
                t_list = json_recipe.get(item)
                page_one.entry_th.delete(0, END)
                page_one.entry_th.insert(0, t_list[0])
                page_one.entry_tm.delete(0, END)
                page_one.entry_tm.insert(0, t_list[1])
            if item == 'ingredients':
                page_one.entry_i.insert(0, json_recipe.get(item))
            if item == 'category':
                page_one.entry_ol.set(json_recipe.get(item))
            if item == 'directions':
                page_one.entry_d.insert(1.0, json_recipe.get(item))

        self.controller.show_frame('Page_one')
        self.controller.set_geo_page_one()

if __name__ == '__main__':
    print(sys.platform)
    app = Mainwindow()
    app.title('Recipe Organizer')
    app.mainloop()
    
