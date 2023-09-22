from customtkinter import CTkFrame, CTkButton, filedialog, CTkLabel, StringVar, EW
from typing import Any, List, Tuple, Callable, Optional
from ....libs.pubsub import PubSub
from ....utils import FileUtil
from ....services import services_instance


PUBSUB_KEY_FILE_SELECTED = "PUBSUB_KEY_FILE_SELECTED"


class FileSelectBar(CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

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

        # 更新 資料表
        services_instance.base_data_frame_service.read_file(file_path)
        # 清空 舊紀錄
        # services_instance.investment_strategy_service.delete_all()

        # 發布 pubsub 消息
        PubSub.publish(PUBSUB_KEY_FILE_SELECTED, file_path)
