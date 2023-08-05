import re

from netmiko.cisco_base_connection import CiscoSSHConnection


class MypowerOsSSH(CiscoSSHConnection):

    def session_preparation(self) -> None:
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        # 根据账号权限不同，进入后显示的prompt也会有差异
        self._test_channel_read(pattern=r">|#")
        # 迈普设备需要enable 才能取消分页，或者账号权限足够
        if self.secret:
            self.enable()
            self.disable_paging(command="more off")
            self.exit_enable_mode()
            self.set_base_prompt()
        else:
            self.disable_paging(command="more off")

    # 迈普的设备会有两种符号，类似思科，一种是# ，一种是>
    def set_base_prompt(self, pri_prompt_terminator=r'#',
                        alt_prompt_terminator=r'>',
                        delay_factor=0.1) -> str:
        return super(MypowerOsSSH, self).set_base_prompt(pri_prompt_terminator=pri_prompt_terminator,
                                                         alt_prompt_terminator=alt_prompt_terminator,
                                                         delay_factor=delay_factor)

    def normalize_linefeeds(self, a_string: str) -> str:
        """Convert '\r\n' or '\r\r\n' to '\n, and remove extra '\r's in the text."""
        newline = re.compile(r"(\r\r\n\r|\r\r\n|\r\n)")
        return newline.sub(self.RESPONSE_RETURN, a_string).replace("\r", "\n")

    def enable(
        self,
        cmd="enable",
        pattern="ssword",
        enable_pattern=None,
        re_flags=re.IGNORECASE,
    ):
        """Enter enable mode."""
        return super().enable(
            cmd=cmd, pattern=pattern, enable_pattern=enable_pattern, re_flags=re_flags
        )

    def check_enable_mode(self, check_string="#"):
        return super().check_enable_mode(check_string=check_string)

    def check_config_mode(self, check_string: str = ")#", pattern: str = "") -> bool:
        """
        Checks if the device is in configuration mode or not.
        """
        return super().check_config_mode(check_string=check_string, pattern=pattern)

    # 迈普的离开enable 模式命令有disable 和exit 两种，直接使用原有的方法即可
    # def exit_enable_mode(self, exit_command="disable")

    def config_mode(
            self,
            config_command: str = "configure terminal",
            pattern: str = "",
            re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )
    # 迈普的 exit_config_mode 参数与思科的基类完全一致，无需修改
    # def exit_config_mode(self, exit_config: str = "end", pattern: str = r"\#") -> str:
    #     """Exit from configuration mode."""
    #     return super().exit_config_mode(exit_config=exit_config, pattern=pattern)

    def save_config(
            self,
            cmd="write",
            confirm=True,
            confirm_response="yes",
    ):
        """Saves Config."""
        return super(MypowerOsSSH, self).save_config(
            cmd=cmd,
            confirm=confirm,
            confirm_response=confirm_response,
        )
