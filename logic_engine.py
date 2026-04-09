# logic_engine.py
# Updated based on West Bengal Land Reforms Act, 1955
# Sections: 14K (Definitions), 14M (Ceiling), 14U (Bar on Transfer), 14Y (Future Acquisition)

def get_conversion_factor(land_type):
    """
    Returns the conversion factor based on Section 14K/14L.
    - 1.00 Standard Hectare = 1.00 Physical Hectare (Irrigated)
    - 1.00 Standard Hectare = 1.40 Physical Hectares (Non-Irrigated/Orchard/Bastu)
    """
    land_type = str(land_type).lower()
    
    # Strict Keywords for Irrigated
    if "irrigated" in land_type or "shali" in land_type:
        if "non" not in land_type: 
            return 1.0
    
    # Everything else (Danga, Orchard, Homestead, Bastu) is 1.40
    return 1.40

def acres_to_standard_hectares(acres, land_type):
    """
    Converts Acres -> Physical Hectares -> Standard Hectares (SH)
    """
    if acres <= 0: return 0.0
    
    # 1 Acre = 0.404686 Hectares
    physical_hectares = acres * 0.404686
    factor = get_conversion_factor(land_type)
    
    # Formula: Standard = Physical / Factor
    return physical_hectares / factor

def get_ceiling_limit(family_size):
    """
    Calculates Ceiling Limit per Section 14M.
    """
    family_size = int(family_size)
    
    if family_size == 1:
        # Section 14M(1)(a) & (b): Adult unmarried or sole survivor
        return 2.50
    elif family_size <= 5:
        # Section 14M(1)(c): Family of 2-5
        return 5.00
    else:
        # Section 14M(1)(d): Family > 5
        # 5.00 + 0.50 per extra member, Max Cap 7.00
        extra_members = family_size - 5
        calculated_limit = 5.00 + (extra_members * 0.50)
        return min(calculated_limit, 7.00)

def check_ceiling_limit(family_size, current_acres, current_type, new_acres, new_type, intent):
    """
    Master Logic for Legality Check.
    Handles: BUY, SELL, TRANSFER, INHERIT, GIFT.
    """
    intent = str(intent).lower()
    
    # 1. Calculate Status
    current_sh = acres_to_standard_hectares(current_acres, current_type)
    new_sh = acres_to_standard_hectares(new_acres, new_type)
    ceiling_limit = get_ceiling_limit(family_size)
    
    # --- SCENARIO 1: OUTGOING LAND (Sell, Gift, Transfer) ---
    if intent in ['sell', 'gift', 'transfer', 'donate', 'will']:
        
        # Rule 1: Possession Check
        if current_acres < new_acres:
             return False, (
                f"🚫 IMPOSSIBLE: You are trying to {intent} {new_acres} acres, "
                f"but you only own {current_acres} acres."
            )
        
        # Rule 2: Section 14U (Bar on Transfer by Ceiling Surplus Holder)
        # "A raiyat owning land in excess of the ceiling... shall not transfer... until excess land has vested."
        if current_sh > ceiling_limit:
            return False, (
                f"🚫 ILLEGAL TRANSFER (Section 14U Violation): You currently hold {current_sh:.2f} SH, "
                f"which exceeds your ceiling of {ceiling_limit:.2f} SH. "
                "Under Section 14U, you are BARRED from selling/transferring any land until the State takes possession of your excess."
            )

        # If passed checks
        remaining_sh = current_sh - new_sh
        return True, (
            f"✅ LEGAL {intent.upper()}: Valid transaction. Your holding will reduce to {remaining_sh:.2f} Standard Hectares. "
            "You are compliant with the Land Reforms Act."
        )

    # --- SCENARIO 2: INCOMING LAND (Buy, Inherit, Acquire) ---
    else:
        # Calculate Future Holding
        total_sh = current_sh + new_sh
        
        # Rule 3: Section 14M (The Ceiling)
        if total_sh > ceiling_limit:
            
            # Special Message for Inheritance (Section 14Y)
            if intent in ['inherit', 'inheritance', 'succession']:
                excess_sh = total_sh - ceiling_limit
                return False, (
                    f"⚠️ PARTIALLY VOID (Section 14Y): Inheritance allows you to receive this land, "
                    f"BUT your total ({total_sh:.2f} SH) will exceed the limit ({ceiling_limit:.2f} SH). "
                    f"The excess {excess_sh:.2f} SH will automatically VEST in the State."
                )
            
            # Message for Buying (Section 14M)
            return False, (
                f"🚫 ILLEGAL ACQUISITION (Section 14M): This purchase would take your total holding to "
                f"{total_sh:.2f} Standard Hectares. Your statutory limit is {ceiling_limit:.2f} SH. "
                "Transaction prohibited."
            )
            
        return True, (
            f"✅ LEGAL {intent.upper()}: Your total holding will be {total_sh:.2f} Standard Hectares. "
            f"This is within your ceiling limit of {ceiling_limit:.2f} SH."
        )