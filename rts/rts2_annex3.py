#!/usr/bin/python

# Three clause BSD license: https://opensource.org/licenses/BSD-3-Clause

# Copyright (c) 2017, Bruce Badger All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = "Bruce Badger"
__copyright__ = "Copyright (c) 2017 Bruce Badger"
__license__ = "BSD-3-Clause"

"""
This is an implementation of the rules defined in annex 3 of RTS 2:
http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0583&rid=1
As far as possible the terminology is taken directly from RTS 2.
"""

from rts2_annex3_model import *

class_root = AssetClassSet(
    version_id="EU 2017/583 of 14 July 2016",
)


class_root.append(
    AssetClass(
        name="Bonds (all bond types except ETCs and ETNs)",
        ref="Table 2.1, 2.2 and 2.3",
        sub_asset_classes=[

            SubAssetClass(
                name="Sovereign Bond",
                criteria=[],
            ),

            SubAssetClass(
                name="Other Public Bond",
                criteria=[],
            ),

            SubAssetClass(
                name="Convertible Bond",
                criteria=[],
            ),

            SubAssetClass(
                name="Covered Bond",
                criteria=[],
            ),

            SubAssetClass(
                name="Corporate Bond",
                criteria=[],
            ),

            SubAssetClass(
                name="Other Bond",
                criteria=[],
            ),

        ]
    )
)

class_root.append(
    AssetClass(
        name="Bonds (ETC and ETN bond types)",
        ref="Table 2.4 and 2.5",
        sub_asset_classes=[

            SubAssetClass(
                name="Exchange Traded Commodities (ETCs)",
                description=\
                    "a debt instrument issued against a direct investment by the "
                    "issuer in commodities or commodities derivative contracts.  "
                    "The price of an  ETC  is  directly or indirectly linked to "
                    "the performance of the underlying.  An ETC passively tracks "
                    "the performance of the commodity or commodity indices to "
                    "which it refers.", 
                criteria=[],
            ),

            SubAssetClass(
                name="Exchange Traded Notes (ETNs)",
                description=\
                    "a debt instrument issued against a direct investment by the "
                    "issuer in the underlying or underlying derivative contracts.  "
                    "The  price  of  an  ETN  is  directly or indirectly linked to "
                    "the performance of the underlying.  An ETN passively tracks "
                    "the performance of the underlying to which it refers.", 
                criteria=[],
            ),

        ]
    )
)

class_root.append(
    AssetClass(
        name="Structured Finance Products (SFPs)",
        ref="Table 3.1, 3.2 and 3.3",
        sub_asset_classes=[]
    )
)

class_root.append(
    AssetClass(
        name="Securitised Derivatives",
        ref="Table 4.1 and 4.2",
        sub_asset_classes=[]
    )
)

class_root.append(
    AssetClass(
        name="Interest Rate Derivatives",
        ref="Table 5.1, 5.2 and 5.3",

        sub_asset_classes=[

            SubAssetClass(
                name="Bond futures/forwards",
                criteria=[
                    UnderlyingIssuerCriterion(description="issuer of the underlying"),
                    BucketedTermOfUnderlyingCriterion(
                        description="term of the underlying deliverable bond defined as follows:",
                        bucket_ceilings=[
                            YearBucketCeiling(
                                periods=4,
                                description="Short-term: the underlying deliverable bond with a term between " \
                                            "1 and 4 years shall be considered to have a short-term"),
                            YearBucketCeiling(
                                periods=8,
                                description="Medium-term: the underlying deliverable bond with a term between " \
                                            "4 and 8 years shall be considered to have a medium-term"),
                            YearBucketCeiling(
                                periods=15,
                                description="Long-term: the underlying deliverable bond with a term between " \
                                            "8 and 15 years shall be considered to have a long-term"),
                            UnboundedBucketCeiling(
                                description="Ultra-long-term: the underlying deliverable bond with a term longer " \
                                            "than 15 years shall be considered to have an ultra-long-term"),
                        ]
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '5,000,000'),
                        average_daily_number_of_trades=10,
                        qualitative_liquidity_criterion=""
                        "whenever a sub-class is determined to have a liquid market with respect "
                        "to a specific time to maturity bucket and the sub-class defined by the "
                        "next time to maturity bucket is determined not to have a liquid market, "
                        "the first back month contract is determined to have a liquid market 2 "
                        "weeks before expiration of the front month",
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '25,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Bond options",
                criteria=[
                    UnderlyingInstrumentCriterion(description="underlying bond or underlying bond future/forward"),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '5,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '25,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="IR futures and FRA",
                criteria=[
                    UnderlyingInterestRateCriterion(description="underlying interest rate"),
                    TermOfUnderlyingInterestRateCriterion(description="term of the underlying interest rate"),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '500,000,000'),
                        average_daily_number_of_trades=10,
                        qualitative_liquidity_criterion=""
                        "whenever a sub-class is determined to have a liquid market with respect "
                        "to a specific time to maturity bucket and the sub-class defined by the "
                        "next time to maturity bucket is determined not to have a liquid market, "
                        "the first back month contract is determined to have a liquid market 2 "
                        "weeks before expiration of the front month",
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70,
                                                   threshold_floor=SumOfMoney('EUR', '10,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '25,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="IR options",
                criteria=[
                    UnderlyingInterestRateCriterion(description="underlying interest rate or underlying "
                                                                "interest rate future or FRA"),
                    TermOfUnderlyingInterestRateCriterion(description="term of the underlying interest rate"),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '500,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70,
                                                   threshold_floor=SumOfMoney('EUR', '10,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '25,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Swaptions",
                criteria=[
                    UnderlyingSwapTypeCriterion(
                        description="underlying swap type defined as follows: fixed-to-fixed single currency swap, "
                                    "futures/forwards on fixed-to-fixed single currency swap, fixed-to-float single "
                                    "currency swap, futures/forwards on fixed-to-float single currency swap, "
                                    "float-to-float single currency swap, futures/forwards on float-to-float "
                                    "single currency swap, inflation single currency swap, futures/forwards on "
                                    "inflation single currency swap, OIS single currency swap, futures/forwards "
                                    "on OIS single currency swap, fixed-to-fixed multi-currency swap, "
                                    "futures/forwards on fixed-to-fixed multi-currency swap, fixed-to-float "
                                    "multi-currency swap, futures/forwards on fixed-to-float multi-currency "
                                    "swap, float-to-float multi-currency swap, futures/forwards on "
                                    "float-to-float multi-currency swap, inflation multi-currency swap, "
                                    "futures/forwards on inflation multi-currency swap, OIS multi-currency "
                                    "swap, futures/forwards on OIS multi-currency swap"
                    ),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional amount "
                                    "of the option is denominated",
                    ),
                    InflationIndexCriterion(
                        description="inflation index if the underlying swap type is either an inflation single "
                                    "currency swap or an inflation multi-currency swap"
                    ),
                    SwapMaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                    OptionMaturityBucketCriterion(
                        description="time to maturity bucket of the option defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(5),
                            YearBucketCeiling(10),
                            UnboundedBucketCeiling(),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '500,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Fixed-to-Float 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards "
                     "on Fixed-to-Float 'multi-currency swaps' or 'cross-currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows "
                            "denominated in different currencies and the cash flows of one leg are "
                            "determined by a fixed interest rate while those of the other leg are "
                            "determined by a floating interest rate",
                criteria=[
                    NotionalCurrencyPairCriterion(
                        description="notional currency pair defined as combination of the two currencies "
                                    "in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Float-to-Float 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards "
                     "on Float-to-Float 'multi-currency swaps' or 'cross-currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows "
                            "denominated in different currencies and where the cash flows of both legs "
                            "are determined by floating interest rates",
                criteria=[
                    NotionalCurrencyPairCriterion(
                        description="notional currency pair defined as combination of the two currencies "
                                    "in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Fixed-to-Fixed 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards "
                     "on Fixed-to-Fixed 'multi-currency swaps' or 'cross-currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows "
                            "denominated in different currencies and where the cash flows of both legs "
                            "are determined by fixed interest rates",
                criteria=[
                    NotionalCurrencyPairCriterion(
                        description="notional currency pair defined as combination of the two currencies "
                                    "in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Overnight Index Swap (OIS) 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards "
                     "on Overnight Index Swap (OIS) 'multi-currency swaps' or 'cross-currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows denominated "
                            "in different currencies and where the cash flows of at least one leg are determined "
                            "by an Overnight Index Swap (OIS) rate",
                criteria=[
                    NotionalCurrencyPairCriterion(
                        description="notional currency pair defined as combination of the two currencies "
                                    "in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Inflation 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Inflation "
                     "'multi-currency swaps' or 'cross-currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows denominated "
                            "in different currencies and where the cash flows of at least one leg are determined by "
                            "an inflation rate",
                criteria=[
                    NotionalCurrencyPairCriterion(
                        description="notional currency pair defined as combination of the two currencies "
                                    "in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Fixed-to-Float 'single currency swaps' and futures/forwards "
                     "on Fixed-to-Float 'single currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows denominated in "
                            "the same currency and the cash flows of one leg are determined by a fixed interest rate "
                            "while those of the other leg are determined by a floating interest rate",
                criteria=[
                    NotionalCurrencyCriterion(
                        description="notional currency in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Float-to-Float 'single currency swaps' and futures/forwards on "
                     "Float-to-Float 'single currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows "
                            "denominated in the same currency and where the cash flows of both legs are "
                            "determined by floating interest rates",
                criteria=[
                    NotionalCurrencyCriterion(
                        description="notional currency in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Fixed-to-Fixed 'single currency swaps' and futures/forwards on "
                     "Fixed-to-Fixed 'single currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows "
                            "denominated in the same currency and where the cash flows of both legs are "
                            "determined by fixed interest rates",
                criteria=[
                    NotionalCurrencyCriterion(
                        description="notional currency in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Overnight Index Swap (OIS) 'single currency swaps' and futures/forwards on "
                     "Overnight Index Swap (OIS) 'single currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows "
                            "denominated in the same currency and where the cash flows of at least one leg are "
                            "determined by an Overnight Index Swap (OIS) rate",
                criteria=[
                    NotionalCurrencyCriterion(
                        description="notional currency in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Inflation 'single currency swaps' and futures/forwards on Inflation 'single currency swaps'",
                description="a swap or a future/forward on a swap where two parties exchange cash flows denominated "
                            "in the same currency and where the cash flows of at least one leg are determined by an "
                            "inflation rate",
                criteria=[
                    NotionalCurrencyCriterion(
                        description="notional currency in which the two legs of the swap are denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '4,000,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '9,000,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Other Interest Rate Derivatives",
                description="an interest rate derivative that does not belong to any of the above sub-asset classes",
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '9,000,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
                    ),
                ),
            ),

            # ---

        ]
    )
)


class_root.append(
    AssetClass(
        name="Equity Derivatives",
        ref="Table 6.1, 6.2 and 6.3",
        sub_asset_classes=[

            SubAssetClass(
                name="Stock index options",
                criteria=[
                    UnderlyingStockIndexCriterion(
                        description="underlying stock index",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '30,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '200,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '50,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '55,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '600,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '15,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '160,000,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Stock index futures/ forwards",
                criteria=[
                    UnderlyingStockIndexCriterion(
                        description="underlying stock index",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '1,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '50,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '55,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '3,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '15,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '160,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '30,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '250,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '260,000,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Stock options",
                criteria=[
                    UnderlyingShareCriterion(
                        description="underlying share",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '300,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '10,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '20,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Stock futures/ forwards",
                criteria=[
                    UnderlyingShareCriterion(
                        description="underlying share",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '300,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '10,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '20,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Stock dividend options",
                criteria=[
                    UnderlyingShareEntitlingToDividendsCriterion(
                        description="underlying share entitling to dividends",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '400,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '450,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '30,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '10,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '50,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '20,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '150,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Stock dividend futures/ forwards",
                criteria=[
                    UnderlyingShareEntitlingToDividendsCriterion(
                        description="underlying share entitling to dividends",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '400,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '450,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '30,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '10,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '50,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '20,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '150,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Dividend index options",
                criteria=[
                    UnderlyingDividendIndexCriterion(
                        description="underlying dvidend index",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '30,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '200,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '50,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '55,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '600,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '15,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '160,000,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Dividend index futures/ forwards",
                criteria=[
                    UnderlyingDividendIndexCriterion(
                        description="underlying dividend index",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '1,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '50,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '55,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '3,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '15,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '160,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '30,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '250,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '260,000,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Volatility index options",
                criteria=[
                    UnderlyingVolatilityIndexCriterion(
                        description="underlying volatility index",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '30,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '200,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '50,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '55,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '600,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '15,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '160,000,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Volatility index futures/ forwards",
                criteria=[
                    UnderlyingVolatilityIndexCriterion(
                        description="underlying volatility index",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '1,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '50,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '55,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '3,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '15,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '160,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '30,000,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '250,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '260,000,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="ETF options",
                criteria=[
                    UnderlyingETFCriterion(
                        description="underlying ETF",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '300,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '10,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '20,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="ETF futures/ forwards",
                criteria=[
                    UnderlyingETFCriterion(
                        description="underlying ETF",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '0'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '5,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '300,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '10,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '20,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                    ],
                ),
            ),

            SubAssetClass(
                name="Swaps",
                criteria=[
                    UnderlyingEquityTypeCriterion("underlying type: single name, index, basket"),
                    UnderlyingEquityCriterion("underlying single name, index, basket"),
                    EquityParameterCriterion(
                        description="parameter: price return basic performance parameter, parameter return dividend," \
                                    " parameter return variance,parameter return volatility"),
                    EquityParameterMaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        options=dict(
                            price=MaturityBucketCriterion(
                                description="Price return basic performance parameter",
                                bucket_ceilings=[
                                    MonthBucketCeiling(1),
                                    MonthBucketCeiling(3),
                                    MonthBucketCeiling(6),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),
                            volatility=MaturityBucketCriterion(
                                description="Parameter return variance/volatility",
                                bucket_ceilings=[
                                    MonthBucketCeiling(3),
                                    MonthBucketCeiling(6),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),
                            dividend=MaturityBucketCriterion(
                                description="Parameter return dividendMaturity",
                                bucket_ceilings=[
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),
                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=15,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '50,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '300,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '200,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Portfolio Swaps",
                criteria=[
                    UnderlyingEquityTypeCriterion("underlying type: single name, index, basket"),
                    UnderlyingEquityCriterion("underlying single name, index, basket"),
                    EquityParameterCriterion(
                        description="parameter: price return basic performance parameter, parameter return dividend," \
                                    " parameter return variance,parameter return volatility"),
                    MaturityBucketCriterion(
                        description="Price return basic performance parameter",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ],
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=15,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '50,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '300,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,250,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '100,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '550,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '3,000,000')),
                        ),
                        ThresholdTable(
                            adna_floor=SumOfMoney('EUR', '200,000,000'),
                            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '1,500,000')),
                            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
                            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '5,500,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Other equity derivatives",
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '20,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '150,000')),
                    ),
                ),
            ),
            
        ]
    )
)


class_root.append(
    AssetClass(
        name="Commodity Derivatives",
        ref="Table 7.1, 7.3 and 7.3",
        sub_asset_classes=[

            SubAssetClass(
                name="Metal commodity futures/forwards",
                criteria=[
                    MetalTypeCriterion("metal type: precious metal, non-precious metal"),
                    UnderlyingMetalCriterion("underlying metal"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional amount " \
                                    "of the future/forward is denominated",
                    ),
                    MetalsMaturityBucketCriterion(
                        description="time to maturity bucket of the future/forward defined as follows:",
                        options=dict(
                            PRME=MaturityBucketCriterion(
                                description="Precious metal",
                                bucket_ceilings=[
                                    MonthBucketCeiling(3),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),
                            NPRM=MaturityBucketCriterion(
                                description="Non-precious metal",
                                bucket_ceilings=[
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),

                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Metal commodity options",
                criteria=[
                    MetalTypeCriterion("metal type: precious metal, non-precious metal"),
                    UnderlyingMetalCriterion("underlying metal"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional amount " \
                                    "of the option is denominated",
                    ),
                    MetalsMaturityBucketCriterion(
                        description="time to maturity bucket of the option defined as follows:",
                        options=dict(
                            PRME=MaturityBucketCriterion(
                                description="precious metal",
                                bucket_ceilings=[
                                    MonthBucketCeiling(3),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),
                            NPRM=MaturityBucketCriterion(
                                description="non-precious metal",
                                bucket_ceilings=[
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),

                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Metal commodity swaps",
                criteria=[
                    MetalTypeCriterion("metal type: precious metal, non-precious metal"),
                    UnderlyingMetalCriterion("underlying metal"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional " \
                                    "amount of the swap is denominated",
                    ),
                    SettlementTypeCriterion("settlement type defined as cash, physical or other"),
                    MetalsMaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        options=dict(
                            PRME=MaturityBucketCriterion(
                                description="precious metal",
                                bucket_ceilings=[
                                    MonthBucketCeiling(3),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),
                            NPRM=MaturityBucketCriterion(
                                description="non-precious metal",
                                bucket_ceilings=[
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                    YearBucketCeiling(3),
                                ]
                            ),

                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Energy commodity futures/forwards",
                criteria=[
                    EnergyTypeCriterion("energy type: oil, oil distillates, coal, oil light ends, "
                                        "natural gas, electricity, inter-energy"),
                    UnderlyingEnergyCriterion("underlying energy"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional amount "
                                    "of the future/forward is denominated",
                    ),
                    LoadTypeCriterion("load type defined as baseload, peakload, off-peak or others, "
                                      "applicable to energy type: electricity"),
                    DeliveryCriterion("delivery/ cash settlement location applicable to energy types: oil, "
                                      "oil distillates, oil light ends, electricity, inter-energy"),
                    EnergyMaturityBucketCriterion(
                        description="time to maturity bucket of the future/forward defined as follows:",
                        options=dict(
                            oil=MaturityBucketCriterion(
                                description="Oil/ Oil Distillates/ Oil Light ends",
                                bucket_ceilings=[
                                    MonthBucketCeiling(4),
                                    MonthBucketCeiling(8),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                            coal=MaturityBucketCriterion(
                                description="Coal",
                                bucket_ceilings=[
                                    MonthBucketCeiling(6),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                            gas_electricity=MaturityBucketCriterion(
                                description="Natural Gas/'Electricity/Inter-energy",
                                bucket_ceilings=[
                                    MonthBucketCeiling(1),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Energy commodity options",
                criteria=[
                    EnergyTypeCriterion("energy type: oil, oil distillates, coal, oil light ends, "
                                        "natural gas, electricity, inter-energy"),
                    UnderlyingEnergyCriterion("underlying energy"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional "
                                    "amount of the option is denominated",
                    ),
                    LoadTypeCriterion("load type defined as baseload, peakload, off-peak or others, "
                                      "applicable to energy type: electricity"),
                    DeliveryCriterion("delivery/ cash settlement location applicable to energy types: oil, "
                                      "oil distillates, oil light ends, electricity, inter-energy"),
                    EnergyMaturityBucketCriterion(
                        description="time to maturity bucket of the option defined as follows:",
                        options=dict(
                            oil=MaturityBucketCriterion(
                                description="Oil/ Oil Distillates/ Oil Light ends",
                                bucket_ceilings=[
                                    MonthBucketCeiling(4),
                                    MonthBucketCeiling(8),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                            coal=MaturityBucketCriterion(
                                description="Coal",
                                bucket_ceilings=[
                                    MonthBucketCeiling(6),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                            gas_electricity=MaturityBucketCriterion(
                                description="Natural Gas/'Electricity/Inter-energy",
                                bucket_ceilings=[
                                    MonthBucketCeiling(1),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Energy commodity swaps",
                criteria=[
                    EnergyTypeCriterion("energy type: oil, oil distillates, coal, oil light ends, "
                                        "natural gas, electricity, inter-energy"),
                    UnderlyingEnergyCriterion("underlying energy"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional "
                                    "amount of the swap is denominated",
                    ),
                    SettlementTypeCriterion("settlement type defined as cash, physical or other"),
                    LoadTypeCriterion("load type defined as baseload, peakload, off-peak or others, "
                                      "applicable to energy type: electricity"),
                    DeliveryCriterion("delivery/ cash settlement location applicable to energy types: oil, "
                                      "oil distillates, oil light ends, electricity, inter-energy"),
                    EnergyMaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        options=dict(
                            oil=MaturityBucketCriterion(
                                description="Oil/ Oil Distillates/ Oil Light ends",
                                bucket_ceilings=[
                                    MonthBucketCeiling(4),
                                    MonthBucketCeiling(8),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                            coal=MaturityBucketCriterion(
                                description="Coal",
                                bucket_ceilings=[
                                    MonthBucketCeiling(6),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                            gas_electricity=MaturityBucketCriterion(
                                description="Natural Gas/'Electricity/Inter-energy",
                                bucket_ceilings=[
                                    MonthBucketCeiling(1),
                                    YearBucketCeiling(1),
                                    YearBucketCeiling(2),
                                ]
                            ),
                        ),
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Agricultural commodity futures/forwards",
                criteria=[
                    UnderlyingAgriculturalCriterion("underlying agricultural commodity"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional " \
                                    "amount of the future/forward is denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the future/forward defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Agricultural commodity options",
                criteria=[
                    UnderlyingAgriculturalCriterion("underlying agricultural commodity"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional " \
                                    "amount of the option is denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the option defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Agricultural commodity swaps",
                criteria=[
                    UnderlyingAgriculturalCriterion("underlying agricultural commodity"),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional " \
                                    "amount of the swap is denominated",
                    ),
                    SettlementTypeCriterion("settlement type defined as cash, physical or other"),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '250,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '500,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '750,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '1,000,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            ),

            SubAssetClass(
                name="Other commodity derivatives",
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '250,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '500,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '750,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '1,000,000')),
                    ),
                ),
            )

        ]
    )
)


common_fx_thresholds = \
    ThresholdSpecification(
        non_liquid_thresholds=ThresholdTable(
            ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '4,000,000')),
            lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
            ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '20,000,000')),
            lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '25,000,000')),
        ),
    )


class_root.append(
    AssetClass(
        name="Foreign Exchange Derivatives",
        ref="Table 8.1 and 8.2",
        sub_asset_classes=[

            SubAssetClass(
                name="Non-deliverable forward (NDF)",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative contract",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="Deliverable forward (DF)",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative contract",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="Non-Deliverable FX options (NDO)",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative contract",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="Deliverable FX options (DO)",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative contract",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="Non-Deliverable FX swaps (NDS)",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative contract",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="Deliverable FX swaps (DS)",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative contract",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="FX futures",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="underlying currency pair defined as combination of the two currencies "
                                    "underlying the derivative",
                    ),
                    MaturityBucketCriterion(
                        description="time to maturity bucket of the swap defined as follows:",
                        bucket_ceilings=[
                            WeekBucketCeiling(1),
                            MonthBucketCeiling(3),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=common_fx_thresholds,  # See above
            ),

            SubAssetClass(
                name="Other Foreign Exchange Derivatives",
                description="an FX derivative that does not belong to any of the above sub-asset classes",
                thresholds=common_fx_thresholds,  # See above
            )

        ]
    )
)

common_credit_liquid_thresholds = \
    [
        ThresholdTable(
            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                    threshold_floor=SumOfMoney('EUR', '2,500,000')),
            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '5,000,000')),
            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                      threshold_floor=SumOfMoney('EUR', '7,500,000')),
            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                     threshold_floor=SumOfMoney('EUR', '10,000,000')),
        ),
    ]

common_credit_non_liquid_thresholds = \
    ThresholdTable(
        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '2,500,000')),
        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '5,000,000')),
        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '7,500,000')),
        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '10,000,000')),
    )

class_root.append(
    AssetClass(
        name="Credit Derivatives",
        ref="Table 9.1, 9.2 and 9.3",
        sub_asset_classes=[

            SubAssetClass(
                name="Index credit default swap (CDS)",
                description="a swap whose exchange of cash flows is linked to the creditworthiness of " \
                            "several issuers of financial instruments composing an index and the " \
                            "occurrence of credit events",
                criteria=[
                    UnderlyingIndexCriterion(
                        description="underlying index",
                    ),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional " \
                                    "amount of the derivative is denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time maturity bucket of the CDS defined as follows:",
                        bucket_ceilings=[
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '200,000,000'),
                        average_daily_number_of_trades=10,
                        qualitative_liquidity_criterion=""
                        "The underlying index is considered to have a liquid "
                        "market: "
                        "(1) during the whole period of its 'on-the-run status' "
                        "(2) for the first 30 working days of its '1x off-the-run status' "
                        "'on-the-run' index means the rolling most recent "
                        "version (series) of the index created on the date on "
                        "which the composition of the index is effective and "
                        "ending one day prior to the date on which the "
                        "composition of the next version (series) of the index is "
                        "effective. "
                        "'1x off-the-run status' means the version (series) of the "
                        "index which is immediately prior to the current 'on-the-run' "
                        "version (series) at a certain point in time. A version "
                        "(series) ceases being 'on-the-run' and acquires "
                        "its '1x off-the-run' status when the latest version "
                        "(series) of the index is created.",
                    ),
                    liquid_thresholds=common_credit_liquid_thresholds,          # See above
                    non_liquid_thresholds=common_credit_non_liquid_thresholds,  # See above
                ),
            ),

            SubAssetClass(
                name="Single name credit default swap (CDS)",
                description="a swap whose exchange of cash flows is linked to the creditworthiness of "
                            "one issuer of financial instruments and the occurrence of credit events",
                criteria=[
                    UnderlyingReferenceEntityCriterion(
                        description="underlying reference entity",
                    ),
                    UnderlyingReferenceEntityTypeCriterion(
                        description=""
                        "underlying reference entity type defined as follows: "
                        '"Issuer of sovereign and public type" means an issuer entity which is either: '
                        "(a) the Union; "
                        "(b) a Member State including a government department, an agency or a special purpose vehicle "
                        "of a Member State; "
                        "(c) a sovereign entity which is not listed under points (a) and (b); "
                        "(d) in the case of a federal Member State, a member of that federation; "
                        "(e) a special purpose vehicle for several Member States; "
                        "(f) an international financial institution established by two or more Member States "
                        "which have the purpose of mobilising funding and providing financial assistance to the "
                        "benefit of its members that are experiencing or are threatened by severe financial problems; "
                        "(g) the European Investment Bank; "
                        "(h) a public entity which is not a sovereign issuer as specified in the points (a) to (c). "
                        '"Issuer of corporate type" means an issuer entity which is not an issuer of sovereign and '
                        'public type.',
                    ),
                    NotionalCurrencyCriterion(
                        description="notional currency defined as the currency in which the notional "
                                    "amount of the derivative is denominated",
                    ),
                    MaturityBucketCriterion(
                        description="time maturity bucket of the CDS defined as follows:",
                        bucket_ceilings=[
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=common_credit_liquid_thresholds,          # See above
                    non_liquid_thresholds=common_credit_non_liquid_thresholds,  # See above
                ),
            ),
            
            SubAssetClass(
                name="Bespoke basket credit default swap (CDS)",
                criteria=[], 
            ), 

            SubAssetClass(
                name="CDS index options",
                description="an option whose underlying is a CDS index",
                criteria=[
                    CDSIndexSubClassCriterion(
                        description="CDS index sub-class as specified for the sub-asset class of "
                                    "index credit default swap (CDS )",
                    ),
                    MaturityBucketCriterion(
                        description="time maturity bucket of the option defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion=""
                        "a CDS index option whose underlying CDS index is a sub-class determined to have a liquid "
                        "market and whose time to maturity bucket is 0-6 months is considered to have a liquid market "
                        "a CDS index option whose underlying CDS index is a sub-class determined to have a liquid "
                        "market and whose time to maturity bucket is not 0-6 months is not considered to have a "
                        "liquid market "
                        "a CDS index option whose underlying CDS index is a sub-class determined not to have a liquid "
                        "market is not considered to have a liquid market for any given time to maturity bucket",
                    ),
                    liquid_thresholds=common_credit_liquid_thresholds,          # See above
                    non_liquid_thresholds=common_credit_non_liquid_thresholds,  # See above
                ),
            ),

            SubAssetClass(
                name="Single name CDS options",
                description="an option whose underlying is a single name CDS",
                criteria=[
                    CDSSubClassCriterion(
                        description="single name CDS sub-class as specified for the sub-asset class of single name CDS",
                    ),
                    MaturityBucketCriterion(
                        description="time maturity bucket of the option defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(6),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion=""
                        "a single name CDS option whose underlying single name CDS is a sub-class determined "
                        "to have a liquid market and whose time to maturity bucket is 0-6 months is considered "
                        "to have a liquid market "
                        "a single name CDS option whose underlying single name CDS is a sub-class determined "
                        "to have a liquid market and whose time to maturity bucket is not 0-6 months is not "
                        "considered to have a liquid market "
                        "a single name CDS option whose underlying single name CDS is a sub-class determined "
                        "not to have a liquid market is not considered to have a liquid market for any given "
                        "time to maturity bucket",
                    ),
                    liquid_thresholds=common_credit_liquid_thresholds,          # See above
                    non_liquid_thresholds=common_credit_non_liquid_thresholds,  # See above
                ),
            ),

            SubAssetClass(
                name="Other credit derivatives",
                description="a credit derivative that does not belong to any of the above sub-asset classes",
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_credit_non_liquid_thresholds,  # See above
                ),
            )

        ],
    )
)

class_root.append(
    AssetClass(
        name="C10 Derivatives",
        ref="Table 10.1, 10.2 and 10.3",
        sub_asset_classes=[

            # ---

            SubAssetClass(
                name="Freight derivatives",
                description="a financial instrument relating to freight rates as defined in " \
                            "Section C(10) of Annex I of Directive 2014/65/EU",
                criteria=[
                    ContractTypeCriterion(
                        description="contract type: Forward Freight Agreements (FFAs) or options",
                    ),
                    FreightTypeCriterion(
                        description="freight type: wet freight, dry freight",
                    ),
                    FreightSubTypeCriterion(
                        description="freight sub-type: dry bulk carriers, tanker, containership",
                    ),
                    FreightSizeCriterion(
                        description="specification of the size related to the freight sub-type",
                    ),
                    FreightRouteOrTimeCriterion(
                        description="specific route or time charter average",
                    ),
                    MaturityBucketCriterion(
                        description="time maturity bucket of the derivative defined as follows:",
                        bucket_ceilings=[
                            MonthBucketCeiling(1),
                            MonthBucketCeiling(3),
                            MonthBucketCeiling(6),
                            MonthBucketCeiling(9),
                            YearBucketCeiling(1),
                            YearBucketCeiling(2),
                            YearBucketCeiling(3),
                        ]
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '10,000,000'),
                        average_daily_number_of_trades=10,
                    ),
                    liquid_thresholds=[
                        ThresholdTable(
                            ssti_pre_trade=PreTrade(trade_percentile={'S1': 30, 'S2': 40, 'S3': 50, 'S4': 60},
                                                    threshold_floor=SumOfMoney('EUR', '25,000')),
                            lis_pre_trade=PreTrade(trade_percentile=70, threshold_floor=SumOfMoney('EUR', '50,000')),
                            ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                                      threshold_floor=SumOfMoney('EUR', '75,000')),
                            lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                                     threshold_floor=SumOfMoney('EUR', '100,000')),
                        ),
                    ],
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '50,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '75,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                    ),
                ),
            ),

            # ---

            SubAssetClass(
                name="Other C10 derivatives",
                description="a financial instrument as defined in Section C(10) of Annex I of "
                            "Directive 2014/65/EU which is not a 'Freight derivative', any of the "
                            "following interest rate derivatives sub-asset classes: 'Inflation "
                            "multi-currency swap or cross-currency swap', a 'Future/forward on "
                            "inflation multi-currency swaps or cross-currency swaps', an 'Inflation "
                            "single currency swap', a 'Future/forward on inflation single currency "
                            "swap' and any of the following equity derivatives sub-asset classes: a "
                            "'Volatility index option', a 'Volatility index future/forward', a swap "
                            "with parameter return variance, a swap with parameter return volatility, "
                            "a portfolio swap with parameter return variance, a",

                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion="any other C10 derivatives is considered "
                                                        "not to have a liquid market",
                    ),
                    non_liquid_thresholds=ThresholdTable(
                        ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '25,000')),
                        lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '50,000')),
                        ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '75,000')),
                        lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
                    ),
                ),
            )

            # ---

        ]
    )
)

common_cfd_liquid_thresholds=[
    ThresholdTable(
        ssti_pre_trade=PreTrade(trade_percentile=60,
                                threshold_floor=SumOfMoney('EUR', '50,000')),
        lis_pre_trade=PreTrade(trade_percentile=70,
                               threshold_floor=SumOfMoney('EUR', '60,000')),
        ssti_post_trade=PostTrade(trade_percentile=80, volume_percentile=60,
                                  threshold_floor=SumOfMoney('EUR', '90,000')),
        lis_post_trade=PostTrade(trade_percentile=90, volume_percentile=70,
                                 threshold_floor=SumOfMoney('EUR', '100,000')),
        ),
    ]

common_cfd_non_liquid_thresholds=ThresholdTable(
    ssti_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '50,000')),
    lis_pre_trade=PreTrade(threshold_floor=SumOfMoney('EUR', '60,000')),
    ssti_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '90,000')),
    lis_post_trade=PostTrade(threshold_floor=SumOfMoney('EUR', '100,000')),
    )

class_root.append(
    AssetClass(
        name="Financial contracts for differences (CFDs)",
        ref="Table 11.1, 11.3 and 11.3",
        sub_asset_classes=[

            SubAssetClass(
                name="Currency CFDs",
                criteria=[
                    UnderlyingCurrencyPairCriterion(
                        description="a currency CFD sub-class is defined by the underlying "
                                    "currency pair defined as combination of the two currencies "
                                    "underlying the CFD/spread betting contract",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=100,
                    ),
                    liquid_thresholds=common_cfd_liquid_thresholds,
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Commodity CFDs",
                criteria=[
                    UnderlyingCommodityCriterion(
                        description="a commodity CFD sub-class is defined by the underlying commodity of the "
                                    "CFD/spread betting contract",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        average_daily_notional_amount=SumOfMoney('EUR', '50,000,000'),
                        average_daily_number_of_trades=100,
                    ),
                    liquid_thresholds=common_cfd_liquid_thresholds,
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Equity CFDs",
                criteria=[
                    UnderlyingEquityCriterion(
                        description="an equity CFD sub-class is defined by the underlying equity security of the "
                                    "CFD/spread betting contract",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion="an equity CFD sub-class is considered to "
                                                        "have a liquid market if the underlying is an "
                                                        "equity security for which there is a liquid "
                                                        "market as determined in accordance with "
                                                        "Article 2(1)(17)(b) of Regulation "
                                                        "600/2014",
                    ),
                    liquid_thresholds=common_cfd_liquid_thresholds,
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Bond CFDs",
                criteria=[
                    UnderlyingBondCriterion(
                        description="a bond CFD sub-class is defined by the underlying bond or bond future of the "
                                    "CFD/spread betting contract",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion="a bond CFD sub-class is considered to have "
                                                        "a liquid market if the underlying is a bond "
                                                        "or bond future for which there is a liquid "
                                                        "market as determined in accordance with "
                                                        "Articles 6 and 8(1)(b).",
                    ),
                    liquid_thresholds=common_cfd_liquid_thresholds,
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="CFDs on an equity future/forward",
                criteria=[
                    UnderlyingFutureForwardCriterion(
                        description="a CFD on an equity future/forward sub-class is defined by the underlying "
                                    "future/forward on an equity of the CFD/spread betting contract",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion="a CFD on an equity future/forward subclass "
                                                        "is considered to have a liquid market "
                                                        "if the underlying is an equity "
                                                        "future/forward for which there is a liquid "
                                                        "market as determined in accordance with "
                                                        "Articles 6 and 8(1)(b).",
                    ),
                    liquid_thresholds=common_cfd_liquid_thresholds,
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="CFDs on an equity option",
                criteria=[
                    UnderlyingEquityOptionCriterion(
                        description="a CFD on an equity option sub-class is defined by the underlying option on "
                                    "an equity of the CFD/spread betting contract",
                    ),
                ],
                thresholds=ThresholdSpecification(
                    liquidity_criteria=LiquidityCriteria(
                        qualitative_liquidity_criterion="a CFD on an equity option sub-class is "
                                                        "considered to have a liquid market if the "
                                                        "underlying is an equity option for which "
                                                        "there is a liquid market as determined in "
                                                        "accordance with Articles 6 and 8(1)(b).",
                    ),
                    liquid_thresholds=common_cfd_liquid_thresholds,
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Other CFDs",
                description="a CFD/spread betting that does not belong to any of the above sub-asset classes",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

        ]
    )
)

class_root.append(
    AssetClass(
        name="Emission Allowances",
        ref="Table 12.1, 12.2 and 12.3",
        sub_asset_classes=[
        
            SubAssetClass(
                name="European Union Allowances (EUA)",
                description="any unit recognised for compliance with the requirements of "
                    "Directive 2003/87/EC of the European Parliament and  of  the  Council(1) "
                    "(Emissions Trading Scheme)  which represents the right to emit the "
                    "equivalent to 1 tonne of carbon dioxide equivalent (tCO2e)",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="European Union Aviation Allowances (EUAA)",
                description="any unit recognised for compliance with the requirements of "
                    "Directive 2003/87/EC (Emissions Trading Scheme) which represents the "
                    "right to emit the equivalent to 1 tonne of carbon dioxide equivalent "
                    "(tCO2e) from aviation ",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Certified Emission Reductions (CER)",
                description="any unit recognised for compliance with the requirements of "
                    "Directive 2003/87/EC (Emissions Trading Scheme) which represents the "
                    "emissions reduction equivalent to 1 tonne of carbon dioxide equivalent "
                    "(tCO2e)",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Emission Reduction Units (ERU)",
                description="any unit recognised for compliance with the requirements of "
                    "Directive 2003/87/EC (Emissions Trading Scheme) which represents the "
                    "emissions reduction equivalent to 1 tonne of carbon dioxide equivalent "
                    "(tCO2e)",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

        ]
    )
)

class_root.append(
    AssetClass(
        name="Emission Allowance Derivatives",
        ref="Table 13.1, 13.2 and 13.3",
        sub_asset_classes=[
        
            SubAssetClass(
                name="Emission allowance derivatives whose underlying is of the type European Union Allowances (EUA)",
                description="a financial instrument relating to emission allowances of the "
                    "type European Union Allowances (EUA) as defined in Section C(4) of "
                    "Annex I of Directive 2014/65/EU",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Emission allowance derivatives whose underlying is of the type European Union Aviation Allowances (EUAA)",
                description="a financial instrument relating to emission allowances of the "
                    "type European Union Aviation Allowances (EUAA) as defined in Section "
                    "C(4) of Annex I of Directive 2014/65/EU",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),

            SubAssetClass(
                name="Emission allowance derivatives whose underlying is of the type Certified Emission Reductions (CER)",
                description="a financial instrument relating to emission allowances of the "
                    "type Certified Emission Reductions (CER) as defined in Section C(4) of "
                    "Annex I of Directive 2014/65/EU",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),
            
            SubAssetClass(
                name="Emission allowance derivatives whose underlying is of the type Emission Reduction Units (ERU)",
                description="a financial instrument relating to emission allowances of the "
                    "type Emission Reduction Units (ERU) as defined in Section C(4) of "
                    "Annex I of Directive 2014/65/EU",
                criteria=[ ],
                thresholds=ThresholdSpecification(
                    non_liquid_thresholds=common_cfd_non_liquid_thresholds,
                ),
            ),
            
        ]
    )
)


# Below this point are a set of initial crude tests which will be removed once equivalent tests have
# been added to the unit test suite.

class AbstractSample(object):
    def __init__(self, asset_class_name, sub_asset_class_name, maturity_date):
        self.asset_class_name = asset_class_name
        self.sub_asset_class_name = sub_asset_class_name
        self.maturity_date = maturity_date
        self.from_date = datetime.date.today()
        self.to_date = self.maturity_date


class RatesSample(AbstractSample):
    def __init__(self, asset_class_name, sub_asset_class_name, notional_currency, maturity_date):
        super(RatesSample, self).__init__(asset_class_name, sub_asset_class_name, maturity_date)
        self.notional_currency = notional_currency


class EquitiesSample(AbstractSample):
    def __init__(self, asset_class_name, sub_asset_class_name, underlying_type,
                 underlying_equity, equity_parameter, maturity_date):
        super(EquitiesSample, self).__init__(asset_class_name, sub_asset_class_name, maturity_date)
        self.underlying_type = underlying_type
        self.underlying_equity = underlying_equity
        self.equity_parameter = equity_parameter


class FXSample(AbstractSample):
    def __init__(self, asset_class_name, sub_asset_class_name, underlying_currency_pair, maturity_date):
        super(FXSample, self).__init__(asset_class_name, sub_asset_class_name, maturity_date)
        self.underlying_currency_pair = underlying_currency_pair


def classify(a_sample):
    print("Sample = " + str(a_sample.__dict__))
    a_sub_class = class_root.leaf_for(a_sample)
    if a_sub_class:
        print("\nFull Name:" + a_sub_class.full_name())
        items = a_sub_class.classification_dict().items()
        print("\nClassification Dictionary:")
        for item in sorted(items):
            print(str(item))
    else:
        print('\nNOT CLASSIFIED!')


if __name__ == "__main__":
    print("\n" + class_root.display() + "\n")
    # Tests with sample data
    import datetime
    sample_date = datetime.date.today() + datetime.timedelta(days=60)

    rates_sample = dict(
        asset_class_name="Interest Rate Derivatives",
        sub_asset_class_name="Fixed-to-Float 'single currency swaps' and futures/forwards "
                             "on Fixed-to-Float 'single currency swaps'",
        notional_currency="USD",
        maturity_date=sample_date,
    )

    print("\nRRRR11111111111111111111")
    sample = RatesSample(**rates_sample)
    classify(sample)

    print("\nRRRR22222222222222222222")
    sample = RatesSample(**rates_sample)
    sample.notional_currency = "JPY"
    sample.maturity_date = datetime.date.today() + datetime.timedelta(days=1)
    classify(sample)

    print("\nRRRR333333333333333333333")
    sample = RatesSample(**rates_sample)
    sample.notional_currency = "USD"
    sample.maturity_date = datetime.date.today() + datetime.timedelta(days=365*6)
    classify(sample)

    print("\nRRRR4444444444444444444444")
    print("Deals in the past should not be classified")
    sample = RatesSample(**rates_sample)
    sample.maturity_date = datetime.date.today() + datetime.timedelta(days=-90)
    classify(sample)

    print("\nRRRR5555555555555555555555")
    sample = RatesSample(**rates_sample)
    sample.maturity_date = datetime.date.today()
    classify(sample)

    print("\nRRRR6666666666666666666666")
    sample = RatesSample(**rates_sample)
    sample.sub_asset_class_name = "Bond options"
    sample.underlying_instrument = 'xxx'
    classify(sample)

    print("\nRRRR7777777777777777777777")
    sample = RatesSample(**rates_sample)
    sample.sub_asset_class_name = "Bond futures/forwards"
    sample.underlying_issuer = "Test Country"
    sample.term_from_date = datetime.date.today() + datetime.timedelta(days=-90)
    sample.term_to_date = datetime.date.today() + datetime.timedelta(days=365*2)
    sample.maturity_date = datetime.date.today() + datetime.timedelta(days=365*5)
    classify(sample)

    print("\nRRRR8888888888888888888888")
    sample = RatesSample(**rates_sample)
    sample.sub_asset_class_name = "Swaptions"
    sample.underlying_swap_type = "Swap Type 1"
    sample.inflation_index = "Inflation Index 1"
    sample.swap_from_date = datetime.date.today() + datetime.timedelta(days=-90)
    sample.swap_to_date = datetime.date.today() + datetime.timedelta(days=365*5)
    sample.option_from_date = datetime.date.today() + datetime.timedelta(days=-90)
    sample.option_to_date = datetime.date.today() + datetime.timedelta(days=365*15)
    classify(sample)

    print("\nRRRR99999999999999999999999")
    sample = RatesSample(**rates_sample)
    sample.sub_asset_class_name = "Swaptions"
    sample.underlying_swap_type = "OIS single currency swap"
    sample.inflation_index = "AnInflationIDX"
    sample.swap_from_date = datetime.date.today() + datetime.timedelta(days=-90)
    sample.swap_to_date = datetime.date.today() + datetime.timedelta(days=365*2)
    sample.option_from_date = datetime.date.today() + datetime.timedelta(days=-90)
    sample.option_to_date = datetime.date.today() + datetime.timedelta(days=365*2)
    sample.maturity_date = None
    classify(sample)

    equities_sample = dict(
        asset_class_name="Equity Derivatives",
        sub_asset_class_name="Swaps",
        underlying_type="single name",
        underlying_equity="UNIQA .VI",
        equity_parameter="price",
        maturity_date=sample_date,
    )

    print("\nEEEE111111111111111111111")
    sample = EquitiesSample(**equities_sample)
    print("Sample = " + str(sample.__dict__))
    sub_class = class_root.leaf_for(sample)
    print(sub_class.full_name())

    fx_sample = dict(
        asset_class_name="Foreign Exchange Derivatives",
        sub_asset_class_name="Deliverable FX options (DO)",
        underlying_currency_pair=('GBP', 'USD'),
        maturity_date=sample_date,
    )

    print("\nFXFX111111111111111111111")
    sample = FXSample(**fx_sample)
    classify(sample)

    print("\nFXFX222222222222222222222")
    sample = FXSample(**fx_sample)
    sample.maturity_date = datetime.date.today() + datetime.timedelta(days=1)
    classify(sample)
    
    # print("\nGenerated samples")
    # sample = class_root.make_test_samples(1)[0]
    # classify(sample)
