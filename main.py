from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
# komentarz
import os


Builder.load_file('NoLimits.kv')

Window.size = (300, 600)
# W wesrsji ostatecznej uzuń window size i zmień nazy na angielskie


class WindowManager(ScreenManager):
    pass


class ScreanSelected(Screen):
    pass


class Courses(Screen):
    pass


class Plan(Screen):
    pass


class AddACourse(Screen):

    def day(self, text):
        global DAY
        DAY = text

    def time(self, text):
        global TIME
        TIME = text

    def mode(self, text):
        global MODE
        MODE = text

    def addition_coures(self):
        global ADDTEXT
        try:
            ADDTEXT = f'''New Course was add successful:

Day: {str(DAY)}
Time: {str(TIME)}
Level: {str(MODE)}

Is everything corect?'
                        '''
        except:
            ADDTEXT = f'You didint make a choice, please back!'


class AddNewCourse(Screen):

    label_wid = ObjectProperty()

    def state(self):
        self.label_wid.text = ADDTEXT

    def addnewcourse_yes(self):
        addnew = f'{DAY}_{TIME}_{MODE}.json,\n'
        addnew = addnew.replace(':', '_')
        addnew_file = addnew.replace(',\n', '')

        plan_string = ''
        global MESSAGE
        if JsonStore('plan.json').count():
            if JsonStore(addnew_file).count():
                self.label_wid.text = 'This cours is alredy existed!'
                MESSAGE = self.label_wid.text
            else:
                with open('plan.json', 'r', encoding="UTF-8") as file:
                    plan_string = file.read()

                with open(addnew_file, 'w', encoding="UTF-8") as file:
                    file.write(plan_string)

                file_json = JsonStore('file.json')
                file_json.put(addnew_file, day=DAY, mode=MODE, all='yes')
                MESSAGE = ADDTEXT.replace('\n\nIs everything corect?', '')
                MESSAGE = MESSAGE.replace("'", "")

# dodaj jeszcze plik z plikami, żebyś mógł otworzyć listę otwieraną z plikami i day='monday'
# przy dodaniu kursu dodasz plik do pliku z kursami put(file, day='monday')
# jeśli będziesz uwał to po unikalnym kluczy id który będzie ścieżką do pliku z kursem file
        else:
            self.label_wid.text = 'Add a plan to continue,\n\nwithout plan you cant add courses!!'
            MESSAGE = self.label_wid.text


class UpdateTheData(Screen):

    spiner_day = ObjectProperty()
    spiner_cours = ObjectProperty()
    spiner_figure = ObjectProperty()

    def set_day(self):
        file_json = JsonStore('file.json')
        entries = list((x for x in file_json.find(all='yes')))

        idd = []
        for id, dictionary in entries:
            for key in dictionary:
                if key == 'day':
                    idd.append(dictionary[key])

        day = list(set(idd))
        day.sort()
        self.spiner_day.values = day
        self.spiner_cours.text = 'Cours'
        self.spiner_figure.text = 'Figure'

    def show_day(self, text):

        self.chosse_day = text

    def set_cours(self):

        try:
            file_json = JsonStore('file.json')
            entries = list((x for x in file_json.find(day=self.chosse_day)))

            idd = []
            for id, dictionary in entries:
                idd.append(id)
            idd_new = []
            for i in idd:
                i = i.replace('.json', '')
                i = i.replace('_', ' ')
                i = i.replace(' 00', ':00')
                i = i.replace(' 30', ':30')
                i = i.replace(f'{self.chosse_day} ', '')
                idd_new.append(i)

            cours = list(set(idd_new))
            cours.sort()
            self.spiner_cours.values = cours
            self.spiner_figure.text = 'Figure'
        except:
            pass

    def show_cours(self, text):

        self.chosse_cours = text

    def set_figure(self):

        try:
            text = f'{self.chosse_day}_{self.chosse_cours}.json'
            text = text.replace(' ', '_')
            text = text.replace(':', '_')
            self.file_chosse = text

            plan_file_json = JsonStore(text)
            entries = list((x for x in plan_file_json.find(done='no')))

            idd = []
            for id, dictionary in entries:
                idd.append(id)

            idd_new = []
            for i in idd:
                i = [i, plan_file_json.get(i)['level'],
                     plan_file_json.get(i)['figures']]
                idd_new.append(i)

            figure = []

            for table in idd_new:
                a = f'{table[0]}, {table[1]}, {table[2]}'
                figure.append(a)

            self.spiner_figure.values = figure
        except:
            pass

    def show_figures(self, text):

        self.done_figures = text

    def done(self):

        try:
            done_to_check = list(self.done_figures.split(", "))
            plan_file_json = JsonStore(self.file_chosse)
            plan_file_json.put(
                done_to_check[0], level=done_to_check[1], figures=done_to_check[2], done='yes')
            self.spiner_figure.text = 'Whose next?'
        except:
            pass


class ShowMyCourses(Screen):

    show_courses_text = ObjectProperty()
    spiner = ObjectProperty()
    spiner_course = ObjectProperty()
    spiner_done = ObjectProperty()

    def show_all(self):

        self.chosse = 'All'

        file_json = JsonStore('file.json')
        entries = list((x for x in file_json.find(all='yes')))

        plan_show = ''

        for id, dictionary in entries:
            plan_show += f'\n{str(id)}, '

        plan_show = plan_show.replace('.json', '')

        self.show_courses_text.text = plan_show

    def set_day(self):
        file_json = JsonStore('file.json')
        entries = list((x for x in file_json.find(all='yes')))

        idd = []
        for id, dictionary in entries:
            for key in dictionary:
                if key == 'day':
                    idd.append(dictionary[key])

        day = list(set(idd))
        day.sort()
        self.spiner.values = day

    def set_file(self):

        try:
            if self.chosse == 'All':
                pass
        except:
            self.chosse = 'All'
            pass
        if self.chosse == 'All':
            file_json = JsonStore('file.json')
            entries = list((x for x in file_json.find(all='yes')))
        else:
            file_json = JsonStore('file.json')
            entries = list((x for x in file_json.find(day=self.chosse)))

        idd = []
        for id, dictionary in entries:
            idd.append(id)
        idd_new = []
        for i in idd:
            i = i.replace('.json', '')
            i = i.replace('_', ' ')
            i = i.replace(' 00', ':00')
            i = i.replace(' 30', ':30')
            idd_new.append(i)

        file_name = list(set(idd_new))
        file_name.sort()
        self.spiner_course.values = file_name

    def show_by_day(self, text):

        self.chosse = text
        self.day = text

        file_json = JsonStore('file.json')
        entries = list((x for x in file_json.find(day=text)))

        plan_show = ''

        for id, dictionary in entries:
            plan_show += f'\n{str(id)}, '

        plan_show = plan_show.replace('.json', '')

        self.show_courses_text.text = plan_show

    def show_detals(self, text):

        text = text.replace(' ', '_')
        text = text.replace(':', '_') + '.json'
        self.file_chosse = text

        plan_file_json = JsonStore(text)
        entries = list((x for x in plan_file_json.find(done='yes')))
        entries2 = list((x for x in plan_file_json.find(done='no')))

        plan_show = ''
        entries = entries + entries2

        for id, dictionary in entries:
            plan_show += f'\n{str(id)}, '
            for key in dictionary:
                plan_show += f'{dictionary[key]}, '
        plan_show = plan_show.replace(' no,', '')
        plan_show = plan_show.replace(' yes,', '')
        self.show_courses_text.text = plan_show

        self.spiner_done.text = 'Done'

    def show_change_detals(self, text):

        self.yes_no = text

        try:
            if self.file_chosse != 'All':

                plan_file_json = JsonStore(self.file_chosse)
                if text == 'yes':
                    entries = list(
                        (x for x in plan_file_json.find(done='yes')))
                else:
                    entries = list((x for x in plan_file_json.find(done='no')))

                plan_show = ''

                for id, dictionary in entries:
                    plan_show += f'\n{str(id)}, '
                    for key in dictionary:
                        plan_show += f'{dictionary[key]}, '
                if text == 'no':
                    plan_show = plan_show.replace(' no,', '')
                else:
                    plan_show = plan_show.replace(' yes,', '')

                self.show_courses_text.text = plan_show

        except:
            self.show_courses_text.text = 'Please first you must, choose cours!'


class CloseTheCourse(Screen):

    spiner = ObjectProperty()
    label_input = ObjectProperty()

    def set_file(self):

        file_json = JsonStore('file.json')
        entries = list((x for x in file_json.find(all='yes')))

        idd = []
        for id, dictionary in entries:
            idd.append(id)
        idd_new = []
        for i in idd:
            i = i.replace('.json', '')
            i = i.replace('_', ' ')
            i = i.replace(' 00', ':00')
            i = i.replace(' 30', ':30')
            idd_new.append(i)

        file_name = list(set(idd_new))
        file_name.sort()
        self.spiner.values = file_name

    def show_file(self, text):

        text = text.replace(' ', '_')
        text = text.replace(':', '_') + '.json'
        self.delete = text

    def delete_cours(self):

        try:
            plan_file_json = JsonStore(self.delete)
            plan_file_json.clear()

            file_json = JsonStore('file.json')
            file_json.delete(self.delete)
            self.spiner.text = 'Whose next?'
        except:
            pass


class AddAPlan(Screen):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            with open(os.path.join(path, filename[0]), encoding="UTF-8") as file:
                self.plan_list = [line.replace(
                    ",\n", "").split(", ") for line in file]
                file.seek(0)
                self.text_input.text = file.read()
            self.dismiss_popup()
        except:
            self.text_input.text = 'Adding file failed!'

    def save(self):

        if JsonStore('plan.json').count():
            self.text_input.text = 'plan file already exists,\n\n\nif you want change something go to "Edit plan"'
        else:
            plan_json = JsonStore('plan.json')
            plan_json.clear()
            for i in self.plan_list:
                plan_json.put(i[0], level=i[1], figures=i[2], done=i[3])

            entries = list((x for x in plan_json.find(done='no')))


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class EditPlan(Screen):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            with open(os.path.join(path, filename[0]), encoding="UTF-8") as file:
                self.plan_list = [line.replace(
                    ",\n", "").split(", ") for line in file]
                file.seek(0)
                self.text_input.text = file.read()
            self.dismiss_popup()
        except:
            self.text_input.text = 'Adding file failed!'
            # zrób z tego screena z opcją powrotu

    def save(self):
        try:
            plan_json = JsonStore('plan.json')
            plan_json.clear()
            for i in self.plan_list:
                plan_json.put(i[0], level=i[1], figures=i[2], done=i[3])

            entries = list((x for x in plan_json.find(done='no')))

            self.text_input.text = 'Adding file success'
            # zrób z tego screena z opcją powrotu
        except:
            self.text_input.text = 'please, firt you must load the plan!'


class ShowPlan(Screen):

    spiner = ObjectProperty(None)
    text_input_show = ObjectProperty(None)

    def show_all(self):

        plan_json = JsonStore('plan.json')
        entries = list((x for x in plan_json.find(done='no')))
        plan_show = ''

        idd = []
        for id, dictionary in entries:
            idd.append(id)
            plan_show += f'\n{str(id)}, '
            for key in dictionary:
                idd.append(dictionary[key])
                plan_show += f'{dictionary[key]}, '

        self.text_input_show.text = plan_show

    def show_by_level(self, text):

        plan_json = JsonStore('plan.json')
        entries = list((x for x in plan_json.find(level=text)))

        plan_show = ''

        idd = []
        for id, dictionary in entries:
            idd.append(id)
            plan_show += f'\n{str(id)}, '
            for key in dictionary:
                idd.append(dictionary[key])
                plan_show += f'{dictionary[key]}, '

        self.text_input_show.text = plan_show

    def set_level(self):
        plan_json = JsonStore('plan.json')
        entries = list((x for x in plan_json.find(done='no')))

        idd = []
        for id, dictionary in entries:
            for key in dictionary:
                if key == 'level':
                    idd.append(dictionary[key])

        levels = list(set(idd))
        levels.sort()
        self.spiner.values = levels


class Messege(Screen):

    mmmesage = ObjectProperty()

    def message_run(self):
        self.mmmesage.text = MESSAGE


sm = ScreenManager()
sm.add_widget(ScreanSelected(name='main'))
sm.add_widget(Courses(name='courses'))
sm.add_widget(Plan(name='plan'))
sm.add_widget(AddACourse(name='addacourse'))
sm.add_widget(AddNewCourse(name='addnewcourse'))
sm.add_widget(UpdateTheData(name='updatethedate'))
sm.add_widget(ShowMyCourses(name='showmycourses'))
sm.add_widget(CloseTheCourse(name='closethecourse'))
sm.add_widget(AddAPlan(name='addaplan'))
sm.add_widget(EditPlan(name='editplan'))
sm.add_widget(ShowPlan(name='showplan'))
sm.add_widget(Messege(name='messege'))


class Start(App):

    def build(self):
        return sm


if __name__ == '__main__':
    Start().run()
