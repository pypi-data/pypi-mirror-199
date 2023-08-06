"""
获取上海银行间同业拆放利率（Shibor）
贷款基础利率（LPR）
"""
from testforPPshare.stock.macro.shibor import (shibor, LPR)
"""
获取中国银行同业间拆借市场数据（chinbor）
伦敦银行同业间拆借市场数据（Libor）
香港银行同业间拆借市场数据（hibor）
欧洲银行同业间拆借市场数据（euribor）
新加坡银行同业间拆借市场数据（sibor）
"""
from testforPPshare.stock.macro.bor import (get_chinbor, get_euribor,
                                            get_hibor, get_libor, get_sibor)
"""
全球宏观-中国宏观
"""
from testforPPshare.stock.macro.macro_china import (
    China_bank_financing, China_insurance_income, China_mobile_number,
    China_vegetable_basket, China_agricultural_product,
    China_agricultural_index, China_energy_index, China_commodity_price_index,
    Global_sox_index, China_yw_electronic_index, China_construction_index,
    China_construction_price_index, China_lpi_index, China_bdti_index,
    China_bsi_index, China_CPI_monthly, China_CPI_yearly, China_M2_yearly,
    China_fx_reserves_yearly, China_cx_PMI_yearly, China_PMI_yearly,
    China_daily_energy, China_non_man_PMI, China_rmb, China_GDP_yearly,
    China_CPI_monthly, China_PPI_yearly, China_cx_services_pmi_yearly,
    China_market_margin_sz, China_au_report, China_ctci_detail,
    China_ctci_detail_hist, China_ctci, China_exports_yoy, China_imports_yoy,
    China_trade_balance, China_industrial_production_yoy, China_ISFC,
    China_new_house_price, China_enterprise_boom_index,
    China_national_tax_receipts, China_new_financial_credit, China_fx_gold,
    China_money_supply, China_stock_market_cap, China_cpi, China_gdp,
    China_ppi, China_pmi, China_gdzctz, China_hgjck, China_czsr, China_whxd,
    China_wbck, China_CGPI, China_xfzxx, China_reserve_requirement_ratio,
    China_consumer_goods_retail, China_society_electricity,
    China_society_traffic_volume, China_postal_telecommunicational,
    China_international_tourism_fx, China_passenger_load_factor,
    China_freight_index, China_central_bank_balance, China_insurance,
    China_supply_of_money, China_swap_rate, China_foreign_exchange_gold,
    China_retail_price_index, China_real_estate, China_FDI, China_CGPI)
"""
金十数据中心-外汇情绪
"""
from testforPPshare.stock.macro.macro_other import macro_fx_sentiment
"""
金十数据中心-经济指标-欧元区
"""
from testforPPshare.stock.macro.macro_euro import (
    macro_euro_gdp_yoy,
    macro_euro_cpi_mom,
    macro_euro_cpi_yoy,
    macro_euro_current_account_mom,
    macro_euro_employment_change_qoq,
    macro_euro_industrial_production_mom,
    macro_euro_manufacturing_pmi,
    macro_euro_ppi_mom,
    macro_euro_retail_sales_mom,
    macro_euro_sentix_investor_confidence,
    macro_euro_services_pmi,
    macro_euro_trade_balance,
    macro_euro_unemployment_rate_mom,
    macro_euro_zew_economic_sentiment,
    macro_euro_lme_holding,
    macro_euro_lme_stock,
)
"""
金十数据中心-经济指标-央行利率-主要央行利率
"""
from testforPPshare.stock.macro.macro_bank import (
    macro_bank_australia_interest_rate,
    macro_bank_brazil_interest_rate,
    macro_bank_china_interest_rate,
    macro_bank_brazil_interest_rate,
    macro_bank_english_interest_rate,
    macro_bank_euro_interest_rate,
    macro_bank_india_interest_rate,
    macro_bank_japan_interest_rate,
    macro_bank_newzealand_interest_rate,
    macro_bank_russia_interest_rate,
    macro_bank_switzerland_interest_rate,
    macro_bank_usa_interest_rate,
)
"""
中国宏观杠杆率数据
"""
from testforPPshare.stock.macro.macro_cnbs import macro_cnbs
"""
宏观-加拿大
"""
from testforPPshare.stock.macro.macro_canada import (
    macro_canada_cpi_monthly,
    macro_canada_core_cpi_monthly,
    macro_canada_bank_rate,
    macro_canada_core_cpi_yearly,
    macro_canada_cpi_yearly,
    macro_canada_gdp_monthly,
    macro_canada_new_house_rate,
    macro_canada_retail_rate_monthly,
    macro_canada_trade,
    macro_canada_unemployment_rate,
)
"""
宏观-澳大利亚
"""
from testforPPshare.stock.macro.macro_australia import (
    macro_australia_bank_rate,
    macro_australia_unemployment_rate,
    macro_australia_trade,
    macro_australia_cpi_quarterly,
    macro_australia_cpi_yearly,
    macro_australia_ppi_quarterly,
    macro_australia_retail_rate_monthly,
)
"""
英国-宏观
"""
from testforPPshare.stock.macro.macro_uk import (
    macro_uk_gdp_yearly,
    macro_uk_gdp_quarterly,
    macro_uk_retail_yearly,
    macro_uk_rightmove_monthly,
    macro_uk_rightmove_yearly,
    macro_uk_unemployment_rate,
    macro_uk_halifax_monthly,
    macro_uk_bank_rate,
    macro_uk_core_cpi_monthly,
    macro_uk_core_cpi_yearly,
    macro_uk_cpi_monthly,
    macro_uk_cpi_yearly,
    macro_uk_halifax_yearly,
    macro_uk_retail_monthly,
    macro_uk_trade,
)
"""
日本-宏观
"""
from testforPPshare.stock.macro.macro_japan import (
    macro_japan_bank_rate,
    macro_japan_core_cpi_yearly,
    macro_japan_cpi_yearly,
    macro_japan_head_indicator,
    macro_japan_unemployment_rate,
)
"""
瑞士-宏观
"""
from testforPPshare.stock.macro.macro_swiss import (
    macro_swiss_trade,
    macro_swiss_svme,
    macro_swiss_cpi_yearly,
    macro_swiss_gbd_yearly,
    macro_swiss_gbd_bank_rate,
    macro_swiss_gdp_quarterly,
)
"""
全球宏观-机构宏观
"""
from testforPPshare.stock.macro.macro_constitute import (
    macro_cons_gold,
    macro_cons_silver,
    macro_cons_opec_month,
)
"""
全球宏观-美国宏观
"""
from testforPPshare.stock.macro.macro_usa import (
    macro_usa_eia_crude_rate,
    macro_usa_non_farm,
    macro_usa_unemployment_rate,
    macro_usa_adp_employment,
    macro_usa_core_pce_price,
    macro_usa_cpi_monthly,
    macro_usa_crude_inner,
    macro_usa_gdp_monthly,
    macro_usa_initial_jobless,
    macro_usa_lmci,
    macro_usa_api_crude_stock,
    macro_usa_building_permits,
    macro_usa_business_inventories,
    macro_usa_cb_consumer_confidence,
    macro_usa_core_cpi_monthly,
    macro_usa_core_ppi,
    macro_usa_current_account,
    macro_usa_durable_goods_orders,
    macro_usa_trade_balance,
    macro_usa_spcs20,
    macro_usa_services_pmi,
    macro_usa_rig_count,
    macro_usa_retail_sales,
    macro_usa_real_consumer_spending,
    macro_usa_ppi,
    macro_usa_pmi,
    macro_usa_personal_spending,
    macro_usa_pending_home_sales,
    macro_usa_nfib_small_business,
    macro_usa_new_home_sales,
    macro_usa_nahb_house_market_index,
    macro_usa_michigan_consumer_sentiment,
    macro_usa_exist_home_sales,
    macro_usa_export_price,
    macro_usa_factory_orders,
    macro_usa_house_price_index,
    macro_usa_house_starts,
    macro_usa_import_price,
    macro_usa_industrial_production,
    macro_usa_ism_non_pmi,
    macro_usa_ism_pmi,
    macro_usa_job_cuts,
    macro_usa_cftc_nc_holding,
    macro_usa_cftc_c_holding,
    macro_usa_cftc_merchant_currency_holding,
    macro_usa_cftc_merchant_goods_holding,
    macro_usa_phs,
)
"""
德国-经济指标
"""
from testforPPshare.stock.macro.macro_germany import (
    macro_germany_gdp,
    macro_germany_ifo,
    macro_germany_cpi_monthly,
    macro_germany_retail_sale_monthly,
    macro_germany_trade_adjusted,
    macro_germany_retail_sale_yearly,
    macro_germany_cpi_yearly,
    macro_germany_zew,
)

from testforPPshare.util.function import get_method