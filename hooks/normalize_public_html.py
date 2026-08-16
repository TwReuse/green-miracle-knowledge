"""Normalize public HTML values that must differ from MkDocs locale keys."""


def on_post_page(output: str, **_kwargs) -> str:
    """Emit the BCP 47 language tag while retaining the zh_TW theme locale."""
    output = output.replace('<html lang="zh_Hant_TW"', '<html lang="zh-Hant-TW"', 1)
    return output.replace('<html lang="zh_TW"', '<html lang="zh-TW"', 1)
