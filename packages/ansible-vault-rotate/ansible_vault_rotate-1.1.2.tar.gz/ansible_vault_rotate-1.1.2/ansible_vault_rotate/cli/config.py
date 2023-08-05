from os import chdir

from ansible_vault_rotate.vault import build_vault_source


class CliConfig:
    def __init__(self, args: dict[str]):
        self.args = args

        self.source_vault_passphrase = None
        self.source_vault = None
        self.target_vault = None
        self.target_vault_passphrase = None

        self.file_glob_patterns = self.__parse_glob_patterns()
        self.ignore_errors = self.__with_default('ignore_errors', False)
        self.update_source_secret = self.__with_default('update_source_secret', False)

    def __with_default(self, name: str, default: any) -> any:
        if self.__has_arg(name):
            return self.args[name]

        return default

    def __parse_glob_patterns(self) -> list[str]:
        patterns = self.__with_default('file_glob_pattern', [])
        if len(patterns) == 0:
            patterns = ["**/*.yml", "**/*.yaml"]

        return patterns

    def __has_arg(self, name: str) -> bool:
        return name in self.args and self.args[name] is not None

    def switch_to_pwd(self) -> "CliConfig":
        if self.__has_arg("pwd"):
            chdir(self.args['pwd'])

        return self

    def parse_vaults(self) -> "CliConfig":
        self.source_vault = build_vault_source(self.args['old_vault_secret_source'])
        self.source_vault_passphrase = self.source_vault.read()

        self.target_vault = build_vault_source(self.args['new_vault_secret_source'])
        self.target_vault_passphrase = self.target_vault.read()

        return self
