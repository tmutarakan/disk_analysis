from urwid import (
    connect_signal, Text, Divider, Button, AttrMap, ListBox,
    SimpleFocusListWalker, ExitMainLoop, Padding,
    MainLoop, Frame, AttrWrap
)
import pickle


WIDTH = 80


class MainMenu:
    footer_text = [
        ('key', "Quit(press q or Q)"),
        ]
    
    def __init__(self, data: list) -> None:
        self.data = data
        title = self.get_parent('parent_id', -1)
        choices = [elem for elem in data if elem['parent_id'] == self.parent_id]
        self.menu = Padding(self.create_menu(title, choices), left=2, right=2)
        self.footer = AttrWrap(Text(self.footer_text), 'foot')
        self.main_frame = Frame(self.menu, footer=self.footer)
        self.loop = MainLoop(self.main_frame, palette=[('reversed', 'standout', '')], unhandled_input=self.unhandled_input)
    
    def get_parent(self, attr, id):
        for elem in self.data:
            if elem[attr] == id:
                self.parent_id = elem['id']
                return elem

    def run(self) -> None:
        self.loop.run()

    def create_menu(self, title, choices):
        body = [Text(print_directory(title)), Divider()]
        for elem in choices:
            if elem['type'] == 'Directory':
                button = Button(print_directory(elem))
                curr_choices = [subelem for subelem in self.data if subelem['parent_id'] == elem['id']]
                connect_signal(button, 'click', self.chose_item, (elem, curr_choices))
            else:
                button = Button(print_file(elem))
            body.append(AttrMap(button, None, focus_map='reversed'))
        return ListBox(SimpleFocusListWalker(body))

    def chose_item(self, button, user_data):
        title, choices = user_data
        body = [Text(print_directory(title)), Divider()]
        title = self.get_parent('id', title['parent_id'])
        if title:
            button = Button('..')
            connect_signal(button, 'click', self.chose_item, (title, [elem for elem in self.data if elem['parent_id'] == title['id']]))
            body.append(AttrMap(button, None, focus_map='reversed'))
        for elem in choices:
            if elem['type'] == 'Directory':
                button = Button(print_directory(elem))
                curr_choices = [subelem for subelem in self.data if subelem['parent_id'] == elem['id']]
                connect_signal(button, 'click', self.chose_item, (elem, curr_choices))
            else:
                button = Button(print_file(elem))
            body.append(AttrMap(button, None, focus_map='reversed'))
        self.menu.original_widget = ListBox(SimpleFocusListWalker(body))
    
    def unhandled_input(self, k):
        # update display of focus directory
        if k in ('q','Q'):
            raise ExitMainLoop()


def print_directory(obj: dict):
    LENGTH = WIDTH - len(f"{obj['name']}{obj['subdirs']}{obj['files']}{obj['size']}") - 2
    return f"{obj['name']}{' ' * LENGTH}{obj['subdirs']} {obj['files']} {obj['size']}"


def print_file(obj: dict):
    LENGTH = WIDTH - len(f"{obj['name']}{obj['size']}")
    return f"{obj['name']}{' ' * LENGTH}{obj['size']}"


def main():
    with open('out.pickle', 'rb') as f:
        data = pickle.load(f)
    curr_menu = MainMenu(data)
    curr_menu.run()


if __name__ == '__main__':
    main()
