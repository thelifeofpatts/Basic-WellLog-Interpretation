import numpy as np

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

def sw_archie(phi, Rt, Rw, a, m, n):
    if phi <= 0 or Rt <= 0 or Rw <= 0:
        return np.nan  # Invalid input leads to NaN, not a complex number
    try:
        Sw = (a * Rw / (phi**m * Rt))**(1/n)
        return Sw
    except ValueError:
        return np.nan

def sw_archie_new(Rw, Rt, Phi, a, m, n):
    # Ensure Rt is broadcastable to the same shape as Phi
    Rt = np.broadcast_to(Rt, Phi.shape)  # This handles scalar Rt
    
    # Handle invalid inputs (ensure no negative or zero values)
    invalid_mask = (Phi <= 0) | (Rt <= 0) | (Rw <= 0)  # Mask invalid entries
    Sw = np.full_like(Phi, np.nan, dtype=np.float64)  # Initialize output array
    
    # Calculate Sw for valid entries only
    valid_mask = ~invalid_mask
    if np.any(valid_mask):  # Perform calculation only if there are valid entries
        # Perform the Archie equation calculation for valid rows
        Sw[valid_mask] = (a * Rw / (Phi[valid_mask] ** m * Rt[valid_mask])) ** (1 / n)
    
    return Sw

def sw_waxman(Rw, Qv, a, m, n, Temp, Rt, Phi):
    try:
        # Input validation
        if Rw == 0 or Rt == 0 or Phi == 0 or n == 0:
            return np.nan

        Sw, Swi = 0.0, 0.0

        # Calculate Bmax and b
        Bmax = 51.31 * math.log(Temp + 460) - 317.2
        b = (1 - 0.83 / math.exp(0.5 / Rw)) * Bmax
        F = a / (Phi ** m)

        # Initial Swi calculation
        Swi = (F * Rw / Rt) ** (1 / n)

        # Protect against Swi being zero in the loop
        while abs(Sw - Swi) > 0.01 and Swi != 0:
            denominator = (1 / Rw + (b * Qv / Swi))
            if denominator == 0:
                return np.nan

            Sw = (F / Rt / denominator) ** (1 / n)
            Swi = Sw

        return Sw

    except:
        return np.nan

def sw_simandoux(Rw, Rt, Vsh, Poro, a, m, n, Rsh):
    F = a / (Poro ** m)
    X = Vsh / Rsh
    term = X ** 2 + (4 / a) * F * Rw / Rt
    Sw_modsim = ((F * (Rw / 2) * (np.sqrt(term) - X)) ** (2 / n))

    return Sw_modsim