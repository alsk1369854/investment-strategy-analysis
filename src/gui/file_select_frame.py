from customtkinter import CTkFrame, CTkButton, filedialog, CTkLabel, StringVar, EW
from typing import Any, List, Tuple
from ..utils import FileUtil


class FileSelectFrame(CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        # 添加元件
        self._widgets()
        # 元件排版
        self._layout()

    def _widgets(self):
        # 所選到的文件名稱標籤
        self.select_file_name: StringVar = StringVar()
        self.select_file_name_label: CTkLabel = CTkLabel(
            self, textvariable=self.select_file_name
        )

        # 開啟文件選擇器按鈕
        def select_file_btn_click_handler():
            filetypes: List[Tuple[str, str]] = [
                ("Excel file", " .".join(FileUtil.excel_extension)),
                ("CSV file", " .".join(FileUtil.csv_extension)),
            ]
            file_path: str = filedialog.askopenfilename(filetypes=filetypes)
            file_name: str = FileUtil.get_file_name(file_path)
            self.select_file_name.set(file_name)

        self.select_file_btn: CTkButton = CTkButton(
            self,
            width=80,
            text="選擇文件",
            command=select_file_btn_click_handler,
        )

    def _layout(self):
        self.select_file_btn.grid(row=0, column=0, padx=5, pady=5, sticky=EW)
        self.select_file_name_label.grid(row=0, column=1, sticky=EW)
