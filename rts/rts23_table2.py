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
This is an implementation of the rules defined here:
http://ec.europa.eu/finance/securities/docs/isd/mifid/rts/160714-rts-23-annex_en.pdf
This is the annex to RTS 23.  The index to all MiFID Technical Standards documents is here:
http://ec.europa.eu/finance/securities/docs/isd/mifid/its-rts-overview-table_en.pdf
As far as possible the terminology is taken directly from the Annex to RTS 23.
"""


class ProductClassificationElement(object):

    def __init__(self, children=None):
        self.children = children or []
        for child in self.children:
            child.parent = self


class ProductClassificationSet(ProductClassificationElement):

    _cls_singleton = None

    @classmethod
    def singleton(cls):
        if cls._cls_singleton is None:
            cls._cls_singleton = cls()
        return cls._cls_singleton

    def node_for_triplet(self, triplet):
        """
        Examples requests might be:
            <module>.root.node_for_triplet(['OTHR', None, None])
            <module>.root.node_for_triplet(['PAPR', 'CBRD', None])
            <module>.root.node_for_triplet(['METL', 'PRME', 'GOLD'])
            <module>.root.node_for_triplet(['NRGY', 'COAL', None])
        """
        for child in self.children:
            selected = child.node_for_triplet(triplet)
            if selected:
                return selected
        return None

    def child_with_code(self, a_code):
        for child in self.children:
            if child.code == a_code:
                return child
        return None


class ProductClassificationNode(ProductClassificationElement):

    def __init__(self, code, description, children=None):
        super(ProductClassificationNode, self).__init__(children)
        self.code = code
        self.description = description
        self.parent = None

    def node_for_triplet(self, triplet):
        """
        c.f. ProductClassificationSet.node_for_triplet()
        """
        if self.matches_triplet(triplet):
            # print('Selected!')
            # print('My code = ' + str(self.code))
            if self.children:
                for child in self.children:
                    selected = child.node_for_triplet(triplet)
                    if selected:
                        return selected
            else:
                return self
        return None

    def matches_triplet(self, triplet):
        """
        This must be implemented by my subclasses.
        """
        raise NotImplementedError(
            'matches_triplet() must be implemented in concrete subclass {my_class}'
            .format(my_class=type(self)))

    @property
    def base_product(self):
        return None

    @property
    def sub_product(self):
        return None

    @property
    def further_sub_product(self):
        return None


class BaseProductClassification(ProductClassificationNode):

    def matches_triplet(self, triplet):
        return self.code == triplet[0]

    def triplet(self):
        return [self.code, None, None]

    @property
    def base_product(self):
        return self.code


class SubProductClassification(ProductClassificationNode):

    def matches_triplet(self, triplet):
        return self.code == triplet[1]

    def triplet(self):
        return [
            self.parent.code,
            self.code,
            None]

    @property
    def base_product(self):
        return self.parent

    @property
    def sub_product(self):
        return self


class FurtherSubProductClassification(ProductClassificationNode):

    def matches_triplet(self, triplet):
        return self.code == triplet[2]

    def triplet(self):
        return [
            self.parent.parent.code,
            self.parent.code,
            self.code]

    @property
    def base_product(self):
        return self.parent.parent

    @property
    def sub_product(self):
        return self.parent

    @property
    def further_sub_product(self):
        return self


root = ProductClassificationSet(children=[

    BaseProductClassification(
        code='AGRI',
        description='Agricultural',
        children=[
            SubProductClassification(
                code='GROS',
                description='Grains and Oil Seeds',
                children=[
                    FurtherSubProductClassification(code='FWHT', description='Feed Wheat'),
                    FurtherSubProductClassification(code='SOYB', description='Soybeans'),
                    FurtherSubProductClassification(code='CORN', description='Maize'),
                    FurtherSubProductClassification(code='RPSD', description='Rapeseed'),
                    FurtherSubProductClassification(code='RICE', description='Rice'),
                    FurtherSubProductClassification(code='OTHR', description='Other'),
                ]
            ),

            SubProductClassification(
                code='SOFT',
                description='Softs',
                children=[
                    FurtherSubProductClassification(code='CCOA', description='Cocoa'),
                    FurtherSubProductClassification(code='ROBU', description='Robusta Coffee'),
                    FurtherSubProductClassification(code='WHSG', description='White Sugar'),
                    FurtherSubProductClassification(code='BRWN', description='Raw Sugar'),
                    FurtherSubProductClassification(code='OTHR', description='Other'),
                ]
            ),

            SubProductClassification(code='POTA', description='Potato'),

            SubProductClassification(
                code='OOLI',
                description='Olive oil',
                children=[
                    FurtherSubProductClassification(code='LAMP', description='Lampante'),
                ]
            ),

            SubProductClassification(code='DIRY', description='Dairy'),

            SubProductClassification(code='FRST', description='Forestry'),

            SubProductClassification(code='SEAF', description='Seafood'),

            SubProductClassification(code='LSTK', description='Livestock'),

            SubProductClassification(
                code='GRIN',
                description='Grain',
                children=[
                    FurtherSubProductClassification(code='MWHT', description='Milling Wheat'),
                ]
            ),

        ]
    ),


    BaseProductClassification(
        code='NRGY',
        description='Energy',
        children=[

            SubProductClassification(
                code='ELEC',
                description='Electricity',
                children=[
                    FurtherSubProductClassification(code='BSLD', description='Base load'),
                    FurtherSubProductClassification(code='FITR', description='Financial Transmission Rights'),
                    FurtherSubProductClassification(code='PKLD', description='Peak load'),
                    FurtherSubProductClassification(code='OFFP', description='Off-peak'),
                    FurtherSubProductClassification(code='OTHR', description='Other'),
                ]
            ),

            SubProductClassification(
                code='NGAS',
                description='Natural Gas',
                children=[
                    FurtherSubProductClassification(code='GASP', description='GASPOOL'),
                    FurtherSubProductClassification(code='LNGG', description='LNG'),
                    FurtherSubProductClassification(code='NBPG', description='NBP'),
                    FurtherSubProductClassification(code='NCGG', description='NCG'),
                    FurtherSubProductClassification(code='TTFG', description='TTF'),
                ]
            ),

            SubProductClassification(
                code='OILP',
                description='Oil',
                children=[
                    FurtherSubProductClassification(code='BAKK', description='Bakken'),
                    FurtherSubProductClassification(code='BDSL', description='Biodiesel'),
                    FurtherSubProductClassification(code='BRNT', description='Brent'),
                    FurtherSubProductClassification(code='BRNX', description='Brent NX'),
                    FurtherSubProductClassification(code='CNDA', description='Canadian'),
                    FurtherSubProductClassification(code='COND', description='Condensate'),
                    FurtherSubProductClassification(code='DSEL', description='Diesel'),
                    FurtherSubProductClassification(code='DUBA', description='Dubai'),
                    FurtherSubProductClassification(code='ESPO', description='ESPO'),
                    FurtherSubProductClassification(code='ETHA', description='Ethanol'),
                    FurtherSubProductClassification(code='FUEL', description='Fuel'),
                    FurtherSubProductClassification(code='FOIL', description='Fuel Oil'),
                    FurtherSubProductClassification(code='GOIL', description='Gasoil'),
                    FurtherSubProductClassification(code='GSLN', description='Gasoline'),
                    FurtherSubProductClassification(code='HEAT', description='Heating Oil'),
                    FurtherSubProductClassification(code='JTFL', description='Jet Fuel'),
                    FurtherSubProductClassification(code='KERO', description='Kerosene'),
                    FurtherSubProductClassification(code='LLSO', description='Light Louisiana Sweet (LLS)'),
                    FurtherSubProductClassification(code='MARS', description='Mars'),
                    FurtherSubProductClassification(code='NAPH', description='Naptha'),
                    FurtherSubProductClassification(code='NGLO', description='NGL'),
                    FurtherSubProductClassification(code='TAPI', description='Tapis'),
                    FurtherSubProductClassification(code='URAL', description='Urals'),
                    FurtherSubProductClassification(code='WTIO', description='WTI'),
                    FurtherSubProductClassification(code='COAL', description='Coal'),
                    FurtherSubProductClassification(code='INRG', description='Inter Energy'),
                    FurtherSubProductClassification(code='RNNG', description='Renewable energy'),
                    FurtherSubProductClassification(code='LGHT', description='Light ends'),
                    FurtherSubProductClassification(code='DIST', description='Distillates'),
                ]
            ),

            SubProductClassification(code='COAL', description='Coal'),

            SubProductClassification(code='INRG', description='Inter Energy'),

            SubProductClassification(code='RNNG', description='Renewable energy'),

            SubProductClassification(code='LGHT', description='Light ends'),

            SubProductClassification(code='DIST', description='Distillates'),

        ]
    ),


    BaseProductClassification(
        code='ENVR',
        description='Environmental',
        children=[

            SubProductClassification(
                code='EMIS',
                description='Emissions',
                children=[
                    FurtherSubProductClassification(code='CERE', description='CER'),
                    FurtherSubProductClassification(code='ERUE', description='ERU'),
                    FurtherSubProductClassification(code='EUAE', description='EUA'),
                    FurtherSubProductClassification(code='EUAA', description='EUAA'),
                    FurtherSubProductClassification(code='OTHR', description='Other'),
                ]
            ),

            SubProductClassification(code='WTHR', description='Weather'),

            SubProductClassification(code='CRBR', description='Carbon related'),

        ]
    ),


    BaseProductClassification(
        code='FRGT',
        description='Freight',
        children=[

            SubProductClassification(
                code='WETF',
                description='Wet',
                children=[
                    FurtherSubProductClassification(code='TNKR', description='Tankers'),

                ]
            ),

            SubProductClassification(
                code='DRYF',
                description='Dry',
                children=[
                    FurtherSubProductClassification(code='DBCR', description='Dry bulk carriers'),

                ]
            ),

            SubProductClassification(code='CSHP', description='Container ships'),

        ]
    ),


    BaseProductClassification(
        code='FRTL',
        description='Fertilizer',
        children=[
            SubProductClassification(code='AMMO', description='Ammonia'),
            SubProductClassification(code='DAPH', description='DAP (Diammonium Phosphate)'),
            SubProductClassification(code='PTSH', description='Potash'),
            SubProductClassification(code='SLPH', description='Sulphur'),
            SubProductClassification(code='UREA', description='Urea'),
            SubProductClassification(code='UAAN', description='UAN (urea and ammonium nitrate)'),
        ]
    ),


    BaseProductClassification(
        code='INDP',
        description='Industrial products',
        children=[
            SubProductClassification(code='CSTR', description='Construction'),
            SubProductClassification(code='MFTG', description='Manufacturing'),
        ]
    ),


    BaseProductClassification(
        code='METL',
        description='Metals',
        children=[
            SubProductClassification(
                code='NPRM',
                description='Non Precious',
                children=[
                    FurtherSubProductClassification(code='ALUM', description='Aluminium'),
                    FurtherSubProductClassification(code='ALUA', description='Aluminium Alloy'),
                    FurtherSubProductClassification(code='CBLT', description='Cobalt'),
                    FurtherSubProductClassification(code='COPR', description='Copper'),
                    FurtherSubProductClassification(code='IRON', description='Iron ore'),
                    FurtherSubProductClassification(code='LEAD', description='Lead'),
                    FurtherSubProductClassification(code='MOLY', description='Molybdenum'),
                    FurtherSubProductClassification(code='NASC', description='NASAAC'),
                    FurtherSubProductClassification(code='NICK', description='Nickel'),
                    FurtherSubProductClassification(code='STEL', description='Steel'),
                    FurtherSubProductClassification(code='TINN', description='Tin'),
                    FurtherSubProductClassification(code='ZINC', description='Zinc'),
                    FurtherSubProductClassification(code='OTHR', description='Other'),
                ]
            ),

            SubProductClassification(
                code='PRME',
                description='Precious',
                children=[
                    FurtherSubProductClassification(code='GOLD', description='Gold'),
                    FurtherSubProductClassification(code='SLVR', description='Silver'),
                    FurtherSubProductClassification(code='PTNM', description='Platinum'),
                    FurtherSubProductClassification(code='PLDM', description='Palladium'),
                    FurtherSubProductClassification(code='OTHR', description='Other'),
                ]
            ),
        ]
    ),


    BaseProductClassification(code='MCEX', description='Multi Commodity Exotic'),


    BaseProductClassification(
        code='PAPR',
        description='Paper',
        children=[
            SubProductClassification(code='CBRD', description='Containerboard'),
            SubProductClassification(code='NSPT', description='Newsprint'),
            SubProductClassification(code='PULP', description='Pulp'),
            SubProductClassification(code='RCVP', description='Recovered paper'),
        ]
    ),


    BaseProductClassification(
        code='POLY',
        description='Polypropylene',
        children=[
            SubProductClassification(code='PLST', description='Plastic'),
        ]
    ),


    BaseProductClassification(code='INFL', description='Inflation'),


    BaseProductClassification(code='OEST', description='Official economic statistics'),


    BaseProductClassification(
        code='OTHC',
        description="Other C10 'as defined in Table 10.1 of Section 10 of Annex III to Commission "
                    "Delegated Regulation supplementing Regulation (EU) No 600/2014 of the European "
                    "Parliament and of the Council with regard to regulatory technical standards on "
                    "transparency requirements for trading venues and investment firms in respect of "
                    "bonds, structured finance products, emission allowances and derivatives"),


    BaseProductClassification(code='OTHR', description='Other'),
    ])
