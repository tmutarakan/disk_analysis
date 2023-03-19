import urwid


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


edit = urwid.Edit("Укажите путь до директории.\n")


class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            f"{edit.edit_text}\n\nPress Q to exit.")


def input_path():
    fill = QuestionBox(edit)
    loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
    loop.run()
    return edit.get_edit_text()


if __name__ == '__main__':
    print(input_path())
