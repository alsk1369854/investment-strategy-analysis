from customtkinter import CTkFrame, CTkButton, filedialog, CTkLabel, StringVar, EW
from typing import Any, List, Tuple, Callable, Optional
from ...utils import FileUtil, PandasUtil
from ...modules.thread_local import thread_local_manager
from pandas import DataFrame


class FileSelectFrame(CTkFrame):
    def __init__(
        self,
        master: Any,
        on_selected: Optional[Callable[[str], None]] = None,
    ):
        super().__init__(master)
        self._on_selected: Optional[Callable[[str], None]] = on_selected

        # 添加元件
        self._create_widgets()
        # 元件排版
        self._build_layout()

    def _create_widgets(self):
        # 所選到的文件名稱標籤
        self._select_file_name: StringVar = StringVar()
        self._select_file_name_label: CTkLabel = CTkLabel(
            self, textvariable=self._select_file_name
        )

        # 開啟文件選擇器按鈕
        self._select_file_btn: CTkButton = CTkButton(
            self,
            width=80,
            text="選擇文件",
            command=self._select_file_btn_click_handler,
        )

    def _build_layout(self):
        self._select_file_btn.grid(row=0, column=0, padx=5, pady=5, sticky=EW)
        self._select_file_name_label.grid(row=0, column=1, sticky=EW)

    def _select_file_btn_click_handler(self):
        filetypes: List[Tuple[str, str]] = [
            ("Excel file", " .".join(FileUtil.excel_extension)),
            ("CSV file", " .".join(FileUtil.csv_extension)),
        ]
        file_path: str = filedialog.askopenfilename(filetypes=filetypes)
        # 更新 GUI
        # file_name: str = FileUtil.get_file_name(file_path)
        self._select_file_name.set(file_path)

        # 更新 thread local
        base_data_frame: DataFrame = PandasUtil.read_file(file_path)
        thread_local_manager.set_base_data_frame(base_data_frame)

        if self._on_selected != None:
            self._on_selected(file_path)
