from PyQt5 import QtWidgets

class SmallButton(QtWidgets.QPushButton):
    def __init__(self):
        super(SmallButton, self).__init__()
        text_padding = 55
        text_color = '#c3ccdf'
        btn_color = "#e1e1e1"
        btn_hover = "#4f5368"
        btn_pressed = "#282a36"
        is_active = False

        # a = '35'
        #
        style = f'''
                QPushButton {{
                    color: {text_color};
                    background-color: {btn_color};
                    border: 1px solid lightgrey;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: lightblue;
                }}
                QPushButton:pressed {{
                    background-color: {btn_pressed};
                }}
                '''


        # style = f'''
        #         QPushButton {{
        #             background-color: white;
        #             border-style: outset;
        #             border-radius: 6px;
        #         }}
        #         '''


        # active_style = f"""
        #         QPushButton {{
        #             background-color: {btn_hover};
        #             border-right: 5px solid {btn_pressed};
        #         }}
        #         """
        self.setStyleSheet(style)
        # print(style)
        # if not is_active:
        #     self.setStyleSheet(style)
        # else:
        #     self.setStyleSheet(style + active_style)
