import numpy as py

def sw_indonesia(Rw, Rt, Poro, a, m, n, vcl, rsh):
    try:
        # Input validation
        if Rt == 0 or rsh == 0 or a == 0 or n == 0:
            return np.nan

        # Calculate terms
        vcl_term = vcl ** (1 - (0.5 * vcl))
        poro_term = (Poro ** m) / (a * Rw)

        # Denominator calculation
        denominator = (vcl_term / (rsh ** 0.5)) + (poro_term ** 0.5)

        if denominator == 0:
            return np.nan

        # Final calculation
        Sw_indonesia = ((1/Rt) / denominator) ** (2/n)

        # Check if result is valid
        # if not 0 <= Sw_indonesia <= 1:
        #     return np.nan

        return Sw_indonesia

    except:
        return np.nan