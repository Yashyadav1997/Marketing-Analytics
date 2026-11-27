"""Unit-economics helpers for Module 1.

Every function is a plain formula with its assumptions stated, because the
point of the module is to see where each formula stops being true.
Rates are fractions (0.58, not 58) and money is in whatever currency you use,
as long as you stay consistent.
"""

from __future__ import annotations

from dataclasses import dataclass


def gross_margin(revenue: float, cogs: float) -> float:
    """(Revenue - COGS) / Revenue. COGS should include shipping and payment fees
    if they scale with orders; otherwise margin is overstated."""
    if revenue <= 0:
        raise ValueError("revenue must be positive")
    return (revenue - cogs) / revenue


def break_even_roas(margin: float) -> float:
    """Revenue per unit of ad spend at which gross profit exactly repays the ad.

    Pass gross margin for a floor on first-order economics, or contribution margin
    (margin after all variable costs) for a more honest floor.
    """
    if not 0 < margin <= 1:
        raise ValueError("margin must be in (0, 1]")
    return 1.0 / margin


def loaded_cac(
    ad_spend: float,
    new_customers: int,
    agency_fees: float = 0.0,
    creative_costs: float = 0.0,
    tools: float = 0.0,
    team_time: float = 0.0,
) -> float:
    """Fully loaded cost of acquiring one *new* customer.

    Note the denominator: new customers, not orders and not platform-attributed
    conversions. Repeat buyers inflate platform CAC downward.
    """
    if new_customers <= 0:
        raise ValueError("new_customers must be positive")
    total = ad_spend + agency_fees + creative_costs + tools + team_time
    return total / new_customers


def cac_load_factor(platform_cac: float, loaded: float) -> float:
    """How much heavier loaded CAC is than the platform figure (0.6 means +60%)."""
    return loaded / platform_cac - 1.0


def payback_months_simple(
    cac: float, aov: float, margin: float, monthly_orders: float
) -> float:
    """Constant-rate payback: CAC / (AOV x margin x orders per month).

    Treats a customer as buying at a steady rate from month one. Real repeat
    behaviour decays, so this is optimistic; compare it to cohort_payback_month.
    """
    monthly_profit = aov * margin * monthly_orders
    if monthly_profit <= 0:
        raise ValueError("monthly gross profit must be positive")
    return cac / monthly_profit


def cohort_payback_month(
    cac: float, cumulative_gross_profit_per_customer: list[float]
) -> float | None:
    """First month (interpolated) in which cumulative gross profit per customer
    reaches CAC. Index 0 is month 0 (the first order). Returns None if the cohort
    never pays back inside the observed window.
    """
    prev = 0.0
    for month, cum in enumerate(cumulative_gross_profit_per_customer):
        if cum >= cac:
            if month == 0:
                return 0.0
            span = cum - prev
            return (month - 1) + (cac - prev) / span if span else float(month)
        prev = cum
    return None


def ltv_simple(
    aov: float, margin: float, annual_orders: float, lifespan_years: float
) -> float:
    """Gross-profit LTV under constant frequency and a fixed lifespan."""
    return aov * margin * annual_orders * lifespan_years


def ltv_cac_ratio(ltv: float, cac: float) -> float:
    if cac <= 0:
        raise ValueError("cac must be positive")
    return ltv / cac


def marketing_spend_ratio(total_marketing_spend: float, revenue: float) -> float:
    if revenue <= 0:
        raise ValueError("revenue must be positive")
    return total_marketing_spend / revenue


def required_incremental_revenue(monthly_fee: float, contribution_margin: float) -> float:
    """Extra monthly revenue a client must generate just to fund a fee, given the
    margin left on incremental sales. Used in Lesson 4 to size client value."""
    if not 0 < contribution_margin <= 1:
        raise ValueError("contribution_margin must be in (0, 1]")
    return monthly_fee / contribution_margin


@dataclass(frozen=True)
class ModelSummary:
    margin: float
    be_roas: float
    loaded_cac: float
    payback_months: float
    ltv: float
    ltv_cac: float


def summarise(
    revenue: float,
    cogs: float,
    ad_spend: float,
    new_customers: int,
    aov: float,
    monthly_orders: float,
    lifespan_years: float,
    **other_costs: float,
) -> ModelSummary:
    """Run the chain in dependency order: margin -> CAC -> payback -> LTV."""
    m = gross_margin(revenue, cogs)
    cac = loaded_cac(ad_spend, new_customers, **other_costs)
    return ModelSummary(
        margin=m,
        be_roas=break_even_roas(m),
        loaded_cac=cac,
        payback_months=payback_months_simple(cac, aov, m, monthly_orders),
        ltv=(ltv := ltv_simple(aov, m, monthly_orders * 12, lifespan_years)),
        ltv_cac=ltv_cac_ratio(ltv, cac),
    )
