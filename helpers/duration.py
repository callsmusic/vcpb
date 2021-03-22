def format_duration(seconds: int) -> str:
    result = ""
    remainder = seconds
    r_ange_s = {
        "d": (24 * 60 * 60),
        "h": (60 * 60),
        "m": 60,
        "s": 1
    }
    for age in r_ange_s:
        divisor = r_ange_s[age]
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m}{age} "
    return " ".join(result.split())
