import flet as ft


class _BaseCallbackHandler(ft.UserControl):
    ERROR_DIALOG = "ERROR"
    SUCCESS_DIALOG = "SUCCESS"

    def _theme_change(
            self,
            checkbox: ft.Checkbox,
            theme_mode: ft.ThemeMode,
            mode_label: str,
    ) -> None:
        checkbox.label = mode_label
        self.page.theme_mode = theme_mode

    def _show_alert_dialog(self, title: str, message: str) -> ft.AlertDialog:
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton(
                    "Ok",
                    on_click=lambda _: (
                        setattr(dialog, "open", False),
                        self.page.update(),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        return dialog
