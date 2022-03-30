def ranking_suffix(rank: int) -> str:
    """Provides ordering ranking e.g. 1st, 11th, 21st

    Args:
        rank (int): rank or placing

    Returns:
        str: ordering rank
    """
    str_rank = str(rank)
    suffix = "th"
    if len(str_rank) > 1:
        if str_rank[-2:] in ["11", "12", "13"]:
            return f"{str_rank}{suffix}"
    if str_rank[-1] == "1":
        suffix = "st"
    elif str_rank[-1] == "2":
        suffix = "nd"
    elif str_rank[-1] == "3":
        suffix = "rd"
    return f"{str_rank}{suffix}"
