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

import datetime
import calendar
import collections

import rts23_table2

import locale
locale.setlocale(locale.LC_ALL, '')


class TaxonomyNode(object):
    """
    This class defines the API which much be implemented by all nodes.
    Essentially this means requiring that every node knows it's parent
    and children.  Handy for presenting the taxonomy as a tree.
    """

    @property
    def parent(self):
        raise NotImplementedError('parent() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    @parent.setter
    def parent(self, value):
        raise NotImplementedError('*setter* of @property parent() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    @property
    def children(self):
        raise NotImplementedError('children() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    @property
    def parents(self):
        """
        I return the list of my parents with the root first and me last.
        """
        if self.parent is None:
            return [self]
        else:
            return self.parent.parents.append(self)


class AssetClassSet(TaxonomyNode):

    def __init__(self, version_id, asset_classes=None):
        self.version_id = version_id
        self._asset_classes = []
        given_asset_classes = asset_classes or []
        self._asset_classes.extend(given_asset_classes)

    @property
    def asset_classes(self):
        return self._asset_classes

    def leaf_for(self, subject):
        """
        This method simply delegates to the newer visitor-pattern based classification_for()
        Consider this method deprecated.
        """
        return self.classification_for(subject)

    def classification_for(self, subject):
        classification = Classification(subject=subject, root=self)
        asset_class = self.asset_class_by_name(subject.asset_class_name)
        if asset_class:
            asset_class.extend_classification(classification)
        else:
            classification.errors.append("RTS 2 has no Asset Class named '{asset_class_name}'.".format(
                asset_class_name=subject.asset_class_name
            ))
        return classification

    def asset_class_by_name(self, asset_class_name):
        return next((asset_class
                     for asset_class
                     in self.asset_classes
                     if asset_class_name == asset_class.name),
                    None)

    def append(self, asset_class):
        self._asset_classes.append(asset_class)

    def display(self, prefix=""):
        target = "The set of all Asset Classes:"
        for asset_class in self._asset_classes:
            target += "\n"
            target += asset_class.display(prefix=prefix+'- ')
        return target

    @property
    def parent(self):
        return None

    @property
    def children(self):
        return self.asset_classes

    def all_sub_asset_classes(self):
        sub_asset_class_list = []
        for asset_class in self.children:
            sub_asset_class_list.extend(asset_class.children)
        return sub_asset_class_list


class AssetClass(TaxonomyNode):
    def __init__(self, name, ref, sub_asset_classes, description=None):
        self.name = name
        self.description = description
        self.ref = ref
        # Claim ownership of the asset classes, then assign them as my children
        for sub_asset_class in sub_asset_classes:
            sub_asset_class.parent = self
        self.sub_asset_classes = sub_asset_classes

    def matches(self, subject):
        return subject.asset_class_name == self.name

    def extend_classification(self, classification):
        classification.asset_class = self
        sub_asset_class = self.sub_asset_class_by_name(classification.subject.sub_asset_class_name)
        if sub_asset_class:
            sub_asset_class.extend_classification(classification)
        else:
            classification.errors.append(
                "Asset class '{asset_class_name}' has no Sub-asset Class named '{sub_asset_class_name}'.".format(
                    asset_class_name=self.name,
                    sub_asset_class_name=classification.subject.sub_asset_class_name
                )
            )
        return classification

    def sub_asset_class_by_name(self, sub_asset_class_name):
        return next((sub_asset_class
                     for sub_asset_class
                     in self.sub_asset_classes
                     if sub_asset_class_name == sub_asset_class.name),
                    None)

    def full_name(self):
        return "Asset class: " + self.name

    def path_name(self):
        return "\n" + self.full_name()

    def display(self, prefix=""):
        target = prefix + self.full_name()
        if self.description:
            target += "\n" + self.description
        for sub_asset_class in self.sub_asset_classes:
            target += "\n"
            target += sub_asset_class.display(prefix=prefix+'- ')
        return target

    def classification_dict(self):
        return {'Asset class': self.name}

    @property
    def parent(self):
        return None

    @property
    def children(self):
        return self.sub_asset_classes


class SubAssetClass(TaxonomyNode):
    def __init__(
            self,
            ref,
            name,
            description=None,
            criteria=None,
            thresholds=None,):
        self.ref = ref
        self.name = name
        self.description = description
        # Claim ownership of the criteria, then assign them as my children
        given_criteria = [] if criteria is None else criteria
        for criterion in given_criteria:
            criterion.parent = self
        self._criteria = given_criteria
        self._thresholds = thresholds
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if self._parent is None:
            self._parent = value
        else:
            raise AttributeError("Parent already assigned.  You may not change it.")

    @property
    def children(self):
        return self.criteria

    @property
    def criteria(self):
        return self._criteria

    @property
    def thresholds(self):
        return self._thresholds

    def matches(self, subject):
        return subject.sub_asset_class_name == self.name

    def extend_classification(self, classification):
        classification.sub_asset_class = self
        for a_criterion in self.criteria:
            a_criterion.extend_classification(classification)
        return classification

    def full_name(self):
        return "Sub-asset class: {name} (ref={ref}).".format(name=self.name, ref=self.ref)

    def path_name(self):
        return self.parent.path_name() + "\n" + self.full_name()

    def display(self, prefix):
        target = prefix + self.full_name()
        for criterion in self.criteria:
            target += "\n"
            target += criterion.display(prefix=prefix+'- ')
        return target

    def classification_dict(self):
        return {'Sub-asset class': self.name}

    def criterion_number_for(self, criterion):
        index = self.criteria.index(criterion)
        return index + 1


class Classification(object):
    """
    A Classification is a specific combination of allowable Asset Class Sub-asset class and
    criterion options for a single subject.

    A complete classification is the identity of an RTS 2 sub-class.  A sub-class can be
    looked as as a sort of virtual ISIN.  Trades with the same sub-class are for the same
    instrument in SI terms.

    Incomplete classifications indicate a trade which could not be classified.  Classification
    problems are noted in the errors dictionary.
    """

    def __init__(self, subject=None, root=None, sub_asset_class=None, options=None):
        self._subject = subject
        self._root = root
        self._asset_class = None
        self._sub_asset_class = sub_asset_class
        self._options = options
        self._errors = None

    @property
    def subject(self):
        return self._subject

    @property
    def root(self):
        return self._root

    @property
    def asset_class(self):
        """
        TODO:  Remove getting the asset class from the sub-asset class once classification code
         is stable, since there should always be an asset class if there is a sub-asset class.
        """
        if not self._asset_class:
            if self.sub_asset_class:
                self._asset_class = self.sub_asset_class.parent
        return self._asset_class

    @asset_class.setter
    def asset_class(self, value):
        if not self._asset_class:
            self._asset_class = value
        return None

    @property
    def sub_asset_class(self):
        return self._sub_asset_class

    @sub_asset_class.setter
    def sub_asset_class(self, value):
        if not self._sub_asset_class:
            self._sub_asset_class = value
        return None

    @property
    def options(self):
        if self._options is None:
            self._options = []
        return self._options

    @property
    def errors(self):
        if self._errors is None:
            self._errors = []
        return self._errors

    def full_name(self):
        full_name_string = self.sub_asset_class.path_name()
        full_name_string += "\n Segmentation criteria options:"
        for option in self.options:
            full_name_string += "\n" + option.full_name()
        return full_name_string

    def classification_dict(self):
        """
        This dictionary is the stored form of the classification.  The string literal form of
        the dictionary is the literal name used to identify RTS 2 sub-classes.
        """
        target_dict = collections.OrderedDict()
        if self.root:
            target_dict['RTS2 version'] = self.root.version_id
        if self.asset_class:
            target_dict.update(self.asset_class.classification_dict())
        if self.sub_asset_class:
            target_dict.update(self.sub_asset_class.classification_dict())
        for option in self.options:
            target_dict.update(option.classification_dict())
        if self.errors:
            target_dict['errors'] = str(self.errors)
        return target_dict


class Criterion(TaxonomyNode):
    def __init__(self, description):
        self._description = description
        self._parent = None

    @property
    def description(self):
        return self._description

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if self._parent is None:
            self._parent = value
        else:
            raise AttributeError("Parent already assigned to this Criterion.  You may not change it.")

    def extend_classification(self, classification):
        raise NotImplementedError('extend_classification() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    @property
    def criterion_number(self):
        return self.parent.criterion_number_for(self)

    @property
    def criterion_name(self):
        return 'Segmentation criterion {n}'.format(n=self.criterion_number)

    def display(self, prefix):
        return prefix + self.full_name()

    def full_name(self):
        return '{criterion_name} - {criterion_description}'.format(
            criterion_name=self.criterion_name,
            criterion_description=self.description,
        )

    @property
    def children(self):
        return []


class CriterionOption(TaxonomyNode):
    def __init__(self, criterion):
        self._criterion = criterion

    @property
    def criterion(self):
        return self._criterion

    @property
    def parent(self):
        return self.criterion

    @property
    def children(self):
        return []

    def full_name(self):
        return self.parent.display(prefix=' - ')

    def classification_dict(self):
        raise NotImplementedError('classification_dict() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))


class ArbitraryValueCriterion(Criterion):
    def __init__(self, description):
        super(ArbitraryValueCriterion, self).__init__(description)
        self.concrete_options = dict()

    def subject_value(self, subject):
        raise NotImplementedError('subject_value() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    def extend_classification(self, classification):
        try:
            this_value = str(self.subject_value(classification.subject))
            if this_value not in self.concrete_options:
                new_option = ValueOption(criterion=self, value=this_value)
                self.concrete_options[this_value] = new_option
            this_option= self.concrete_options[this_value]
            classification.options.append(this_option)
        except AttributeError as ex:
            classification.errors.append('{my_class} exception: {exception_string}'.format(
                my_class=type(self),
                exception_string=str(ex),
                )
            )
        return classification


class DescreteValueCriterion(Criterion):
    def __init__(self, description):
        super(DescreteValueCriterion, self).__init__(description)
        self._concrete_options = None

    @property
    def concrete_options(self):
        if self._concrete_options is None:
            values_dict = dict()
            for allowed_value in self.allowed_values():
                new_option = ValueOption(criterion=self, value=allowed_value)
                values_dict[allowed_value] = new_option
            self._concrete_options = values_dict
        return self._concrete_options

    def subject_value(self, subject):
        raise NotImplementedError('subject_value() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    def allowed_values(self):
        raise NotImplementedError('allowed_values() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    def extend_classification(self, classification):
        try:
            this_value = self.subject_value(classification.subject)
            this_option = self.concrete_options[this_value]
            classification.options.append(this_option)
        except (KeyError, AttributeError) as ex:
            classification.errors.append('{my_class} got bad value: {value}.  Should be one of [{good_values}].'.format(
                my_class=type(self).__name__,
                value=self.subject_value(classification.subject),
                good_values=", ".join(self.concrete_options),
            ))
        return classification


class ValueOption(CriterionOption):
    def __init__(self, criterion, value):
        super(ValueOption, self).__init__(criterion)
        self._value = value

    @property
    def value(self):
        return self._value

    def full_name(self):
        return '{parent}" for {value}'.format(
            parent=self.parent.full_name(),
            value=self.value)

    def classification_dict(self):
        criterion_name = self.parent.criterion_name
        description_name = criterion_name + " description"
        target_dict = {
            criterion_name: self.value,
            description_name: self.parent.description}
        return target_dict


class NotionalCurrencyCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.notional_currency


class UnderlyingIssuerCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_issuer


class UnderlyingCurrencyPairCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_currency_pair


class UnderlyingStockIndexCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_stock_index


class UnderlyingShareCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_share


class UnderlyingShareEntitlingToDividendsCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_share_entitling_to_dividends


class UnderlyingDividendIndexCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_dividend_index


class UnderlyingVolatilityIndexCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_volatility_index


class UnderlyingETFCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_etf


class UnderlyingEquityTypeCriterion(DescreteValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_type

    def allowed_values(self):
        return['single name', 'index', 'basket']


class UnderlyingEquityCriterion(ArbitraryValueCriterion):

    def subject_value(self, subject):
        return subject.underlying_equity


class EquityParameterCriterion(DescreteValueCriterion):

    def subject_value(self, subject):
        return subject.equity_parameter

    def allowed_values(self):
        return['price', 'dividend', 'variance']


class EnergyTypeCriterion(DescreteValueCriterion):

    def subject_value(self, subject):
        return subject.energy_type

    @staticmethod
    def rts23_nrgy_nodes():
        return rts23_table2.root.child_with_code('NRGY').children

    def allowed_values(self):
        """
        I am **assuming** that all possible values here are the children of 'NRGY' in
        the RTS 23 taxonomy.
        """
        return [node.code for node in self.rts23_nrgy_nodes()]


class MetalTypeCriterion(DescreteValueCriterion):

    def subject_value(self, subject):
        return subject.metal_type

    @staticmethod
    def rts23_metl_nodes():
        return rts23_table2.root.child_with_code('METL').children

    def allowed_values(self):
        """
        I am **assuming** that all possible values here are the children of 'METL' in
        the RTS 23 taxonomy.
        """
        return [node.code for node in self.rts23_metl_nodes()]


class UnderlyingEnergyCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_energy


class SettlementTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.settlement_type


class LoadTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.load_type


class DeliveryCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.delivery


class UnderlyingInstrumentCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_instrument


class UnderlyingInterestRateCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_interest_rate


class TermOfUnderlyingInterestRateCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.term_of_underlying_interest_rate


class UnderlyingSwapTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_swap_type


class InflationIndexCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.inflation_index


class NotionalCurrencyPairCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.notional_currency_pair


class UnderlyingMetalCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_metal


class UnderlyingAgriculturalCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_agricultural


class UnderlyingIndexCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_index


class UnderlyingReferenceEntityCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.underlying_ref_entity


class UnderlyingReferenceEntityTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.ref_entity_type


class CDSIndexSubClassCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.cds_index_sub_class


class CDSSubClassCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.cds_sub_class


class ContractTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.contract_type


class FreightTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.freight_type


class FreightSubTypeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.freight_sub_type


class FreightSizeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.freight_size


class FreightRouteOrTimeCriterion(ArbitraryValueCriterion):
    def subject_value(self, subject):
        return subject.freight_route_or_time


class BucketedTermOfUnderlyingCriterion(Criterion):
    def __init__(self, description, bucket_ceilings):
        super(BucketedTermOfUnderlyingCriterion, self).__init__(description)
        self._bucket_ceilings = bucket_ceilings
        self._root_option = None

    @property
    def bucket_ceilings(self):
        return self._bucket_ceilings

    @property
    def root_option(self):
        if self._root_option is None:
            new_root = DateBucketOption(parent=self, bucket_ceilings=self.bucket_ceilings)
            self._root_option = new_root
        return self._root_option

    def extend_classification(self, classification):
        try:
            option = self.root_option.option_for_dates(
                classification.subject.term_from_date,
                classification.subject.term_to_date)
            if option:
                classification.options.append(option)
            else:
                raise KeyError
        except KeyError as _:
            classification.errors.append(
                'Bad term bucket. '
                'Dates: from_date={from_date}, to_date={to_date}.'.format(
                    from_date=classification.subject.term_from_date,
                    to_date=classification.subject.term_to_date,
                )
            )
        return classification


class SwapMaturityBucketCriterion(Criterion):
    def __init__(self, description, bucket_ceilings):
        super(SwapMaturityBucketCriterion, self).__init__(description)
        self._bucket_ceilings = bucket_ceilings
        self._root_option = None

    @property
    def bucket_ceilings(self):
        return self._bucket_ceilings

    @property
    def root_option(self):
        if self._root_option is None:
            new_root = DateBucketOption(parent=self, bucket_ceilings=self.bucket_ceilings)
            self._root_option = new_root
        return self._root_option

    def extend_classification(self, classification):
        try:
            option = self.root_option.option_for_dates(
                classification.subject.swap_from_date,
                classification.subject.swap_to_date)
            if option:
                classification.options.append(option)
            else:
                raise KeyError
        except KeyError as _:
            classification.errors.append(
                'Bad swap maturity bucket. '
                'Dates: from_date={from_date}, to_date={to_date}.'.format(
                    from_date=classification.subject.swap_from_date,
                    to_date=classification.subject.swap_to_date,
                )
            )
        return classification


class OptionMaturityBucketCriterion(Criterion):
    def __init__(self, description, bucket_ceilings):
        super(OptionMaturityBucketCriterion, self).__init__(description)
        self._bucket_ceilings = bucket_ceilings
        self._root_option = None

    @property
    def bucket_ceilings(self):
        return self._bucket_ceilings

    @property
    def root_option(self):
        if self._root_option is None:
            new_root = DateBucketOption(parent=self, bucket_ceilings=self.bucket_ceilings)
            self._root_option = new_root
        return self._root_option

    def extend_classification(self, classification):
        try:
            option = self.root_option.option_for_dates(
                classification.subject.option_from_date,
                classification.subject.option_to_date)
            if option:
                classification.options.append(option)
            else:
                raise KeyError
        except KeyError:
            classification.errors.append(
                'Bad option maturity bucket. '
                'Dates: from_date={from_date}, to_date={to_date}.'.format(
                    from_date=classification.subject.from_date,
                    to_date=classification.subject.to_date,
                )
            )
        return classification


class MetalsMaturityBucketCriterion(Criterion):
    def __init__(self, description, options):
        super(MetalsMaturityBucketCriterion, self).__init__(description)
        self._options = options
        # Claim ownership of the criteria, then assign them as my children
        for criterion in options.values():
            criterion.parent = self

    @property
    def description(self):
        """
        I need to return a blend of my description and that of my parenr
        """
        return self._description

    def extend_classification(self, classification):
        """
        Here I simply delegate to the maturity bucket Criterion for the parameter of my subject
        """
        metal_type = 'Unknown'
        try:
            metal_type = classification.subject.metal_type
            bucket_criterion = self._options[metal_type]
            bucket_criterion.extend_classification(classification)
        except KeyError:
            classification.errors.append(
                'Bad metals maturity bucket.  Metal type: {metal_type}. '
                'Dates: from_date={from_date}, to_date={to_date}.'.format(
                    metal_type=metal_type,
                    from_date=classification.subject.from_date,
                    to_date=classification.subject.to_date,
                )
            )
        return classification

    def criterion_number_for(self, criterion):
        """
        I delegate this to my parent since I represent the Segmentation number here, not criterion.
        """
        if criterion.parent == self:
            return self.parent.criterion_number_for(self)

    def display(self, prefix):
        target = super(MetalsMaturityBucketCriterion, self).display(prefix=prefix)
        segment_prefix = prefix + '- '
        for (bucket_name, bucket_criterion) in self._options.items():
            target += '\n' + segment_prefix + 'Maturity buckets for "' + bucket_name + '"\n'
            target += bucket_criterion.root_option.display(prefix=segment_prefix + '- ')
        return target


class EnergyMaturityBucketCriterion(Criterion):
    def __init__(self, description, options):
        super(EnergyMaturityBucketCriterion, self).__init__(description)
        self._bucket_map = None
        self._options = options
        # Claim ownership of the criteria, then assign them as my children
        for criterion in options.values():
            criterion.parent = self

    @property
    def bucket_map(self):
        """
        Really this is a guess.  These mappings are to Sub Products in RTS 23.
        I'm guessing 'RNNG' goes in gas_electricty.
        """
        if self._bucket_map is None:
            product_map = dict(
                oil=['OILP', 'DIST', 'LGHT'],
                coal=['COAL'],
                gas_electricity=['ELEC', 'NGAS', 'INRG', 'RNNG'],
            )
            reversed_map = {}
            for bucket_name, sub_product_names in product_map.iteritems():
                for sub_product_name in sub_product_names:
                    reversed_map[sub_product_name] = bucket_name
            self._bucket_map = reversed_map
        return self._bucket_map

    def extend_classification(self, classification):
        """
        Here I simply delegate to the maturity bucket Criterion for the parameter of my subject
        Energy type must be one of the Subproduct vales of NRGY in RTS 23
        """
        try:
            bucket_key = self.bucket_map[classification.subject.energy_type]
            bucket_criterion = self._options[bucket_key]
            bucket_criterion.extend_classification(classification)
        except KeyError:
            classification.errors.append(
                'Bad energy maturity bucket.  Energy type: {energy_type}. '
                'Dates: from_date={from_date}, to_date={to_date}.'.format(
                    energy_type=classification.subject.energy_type,
                    from_date=classification.subject.from_date,
                    to_date=classification.subject.to_date,
                )
            )
        return classification

    def criterion_number_for(self, criterion):
        """
        I delegate this to my parent since I represent the Segmentation number here, not criterion.
        """
        if criterion.parent == self:
            return self.parent.criterion_number_for(self)

    def display(self, prefix):
        target = super(EnergyMaturityBucketCriterion, self).display(prefix=prefix)
        segment_prefix = prefix + '- '
        for (bucket_name, bucket_criterion) in self._options.items():
            target += '\n' + segment_prefix + 'Maturity buckets for "' + bucket_name + '"\n'
            target += bucket_criterion.root_option.display(prefix=segment_prefix + '- ')
        return target


class EquityParameterMaturityBucketCriterion(Criterion):
    def __init__(self, description, options):
        super(EquityParameterMaturityBucketCriterion, self).__init__(description)
        self._options = options
        # Claim ownership of the criteria, then assign them as my children
        for criterion in options.values():
            criterion.parent = self

    def extend_classification(self, classification):
        bucket_criterion = self._options.get(classification.subject.equity_parameter, None)
        if bucket_criterion:
            bucket_criterion.extend_classification(classification)
        else:
            classification.errors.append("{my_class} error - no bucketing for parameter: {parameter}.  "
                                         "Must be one of: [{good_values}].".format(
                my_class=type(self).__name__,
                parameter=classification.subject.equity_parameter,
                good_values=", ".join(self._options.keys()),
            ))
        return classification

    def criterion_number_for(self, criterion=None):
        """
        I delegate this to my parent since I represent the Segmentation number here, not criterion.
        """
        if criterion.parent == self:
            return self.parent.criterion_number_for(self)

    def display(self, prefix):
        target = super(EquityParameterMaturityBucketCriterion, self).display(prefix=prefix)
        segment_prefix = prefix + '- '
        for (bucket_name, bucket_criterion) in self._options.items():
            target += '\n' + segment_prefix + 'Maturity buckets for "' + bucket_name + '"\n'
            target += bucket_criterion.root_option.display(prefix=segment_prefix + '- ')
        return target


class MaturityBucketCriterion(Criterion):
    def __init__(self, description, bucket_ceilings):
        super(MaturityBucketCriterion, self).__init__(description)
        self._bucket_ceilings = bucket_ceilings
        self._root_option = None

    @property
    def bucket_ceilings(self):
        return self._bucket_ceilings

    @property
    def root_option(self):
        if self._root_option is None:
            new_root = DateBucketOption(parent=self, bucket_ceilings=self.bucket_ceilings)
            self._root_option = new_root
        return self._root_option

    def display(self, prefix):
        target = super(MaturityBucketCriterion, self).display(prefix=prefix)
        target += self.description + "\n"
        target += self.root_option.display(prefix=prefix+'- ')
        return target

    def extend_classification(self, classification):
        option = self.root_option.option_for(classification.subject)
        if option:
            classification.options.append(option)
        else:
            classification.errors.append('Bad maturity bucket dates: from_date={from_date}, to_date={to_date}.'.format(
                from_date=classification.subject.from_date,
                to_date=classification.subject.to_date,
            ))
        return classification


class MaturityBucketCeiling(object):

    def __init__(self, periods, description=None):
        self._periods = periods
        self._description = description

    @property
    def periods(self):
        return self._periods

    @property
    def period_name(self):
        raise NotImplementedError('period_name() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    def ceiling_string(self):
        """
        A string which describes my ceiling, e.g. 1 month or 5 years
        """
        target = "{n} {name}".format(
            n=self.periods,
            name=self.period_name)
        return target

    def display(self, prefix=""):
        target = "time to maturity <= {ceiling}".format(
            ceiling=self.ceiling_string,
        )
        return target

    def end_date_from(self, base_date):
        raise NotImplementedError('end_date_from() must be implemented in concrete subclass {my_class}'
                                  .format(my_class=type(self)))

    @staticmethod
    def date_on_or_before(year, month, day):
        """
        I return a date which is ideally year/month/day but if I can't
        make a date with those values I return the closest date prior.
        e.g. if you ask for 2016/02/31 you'll get 2016/02/29
        """
        sane_day = max(1, min(day, 31))
        sane_month = max(1, min(month, 12))
        sane_year = max(1900, min(year, 9999))  # though 1900 or 9999 may not be very sane years
        best_date = None
        while best_date is None:
            try:
                best_date = datetime.date(sane_year, sane_month, sane_day)
            except ValueError:
                if sane_day > 1:
                    sane_day -= 1
                    pass
        return best_date

    def next_step(self, bucket_option):
        """
        I return a new instance of my class which takes the next step into the future by
        exactly the same amount of time I represent from the preceding step of option.
        I'll only do this if my class and the one before me is of the same type ... for now,
        anyway.
        """
        previous_bucket_ceiling = bucket_option.previous_bucket_option.ceiling
        my_type = type(self)
        if type(previous_bucket_ceiling) == my_type:
            difference_since_last = self.periods - previous_bucket_ceiling.periods
            next_number_of_periods = self.periods + difference_since_last
            return my_type(next_number_of_periods)
        else:
            error_message = "Can't work out the next step.  I am a {my_type}, the preceding is {preceding}".format(
                my_type=my_type,
                preceding=type(previous_bucket_ceiling)
            )
            raise ValueError(error_message)


class WeekBucketCeiling(MaturityBucketCeiling):

    @property
    def period_name(self):
        if self.periods == 1:
            return "week"
        else:
            return "weeks"

    def end_date_from(self, base_date):
        """
        I work out the end date by simply adding 6 days to the start date.
        """
        delta = datetime.timedelta(days=6)
        return base_date + delta


class MonthBucketCeiling(MaturityBucketCeiling):

    @property
    def period_name(self):
        if self.periods == 1:
            return "month"
        else:
            return "months"

    @staticmethod
    def add_months(base_date, months):
        """
        From http://stackoverflow.com/questions/4130922/
            how-to-increment-datetime-by-custom-months-in-python-without-using-library
        I would have preferred using relativedelta as explained here:
        http://stackoverflow.com/questions/546321/
            how-do-i-calculate-the-date-six-months-from-the-current-date-using-the-datetime
        ... but we don't have dateutil.relative delta :-(

        """
        month = base_date.month - 1 + months
        year = int(base_date.year + month / 12)
        month = month % 12 + 1
        day = min(base_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def end_date_from(self, base_date):
        return self.add_months(base_date, self.periods)


class YearBucketCeiling(MaturityBucketCeiling):

    @property
    def period_name(self):
        if self.periods == 1:
            return "year"
        else:
            return "years"

    def end_date_from(self, base_date):
        """
        I work out the end date by dumbly adding the number of years to the start date, then
        if this is not a valid date I try day -1.  So if start date is the 29th Feb on a leap
        year and the dumb addition ends up in February in a non-leap year then I'll try 29th Feb
        & fail and then try 28th Feb which will work.  28th Feb would be the end date.
        """
        return self.date_on_or_before(
            year=base_date.year + self.periods,
            month=base_date.month,
            day=base_date.day,
        )


class UnboundedBucketCeiling(MaturityBucketCeiling):
    """
    This ceiling would used as a catch all.
    For example, Interest Rate Derivatives / Swaptions have a time to maturuty
    bucket for the option which is "over 10 years".
    ... so this class will be developed when we need to implement Interest Rate Derivatives / Swaptions
    """
    def __init__(self, description=None):
        super(UnboundedBucketCeiling, self).__init__(
            periods=1,
            description=description)

    def ceiling_string(self):
        """
        A string which describes my ceiling, e.g. 1 month or 5 years
        """
        return "unbounded"

    def display(self, prefix=""):
        return prefix + "time to maturity unbounded"

    @property
    def period_name(self):
        return "unbounded"

    def end_date_from(self, base_date):
        """
        I'm unbounded so I have no end date.
        """
        return None


class DateBucketOption(object):
    def __init__(self, parent, bucket_ceilings, previous_bucket_option=None):
        """
        I represent a range of dates which are compared against various dates of
        subjects (trades).  The most common dates are maturity dates.
        Typically I will form a part of a linked list of buckets reaching into the future.  If
        I am created with a previous bucket I link to that and take it's last date + 1 day
        as my starting day.  If I have no previous bucket then I start 'today'.
        """
        self._parent = parent
        self._ceiling = bucket_ceilings[0]  # There must be one so failing if this is none is good
        self._previous_bucket_option = previous_bucket_option
        remaining_bucket_ceilings = bucket_ceilings[1:]
        if remaining_bucket_ceilings:  # If there are more ceilings create the next option in the list
            self._next_bucket_option = type(self)(
                parent=parent,
                bucket_ceilings=remaining_bucket_ceilings,
                previous_bucket_option=self)
        else:
            self._next_bucket_option = None
        self._end_date = None

    @property
    def parent(self):
        return self._parent

    @property
    def ceiling(self):
        """
        My ceiling is a MaturityBucketCeiling which defines a duration such as 1 week,
        3 months or 2 years.
        """
        return self._ceiling

    @property
    def next_bucket_option(self):
        return self._next_bucket_option

    @property
    def previous_bucket_option(self):
        return self._previous_bucket_option

    @property
    def bucket_number(self):
        if self.previous_bucket_option is None:
            return 1
        else:
            return self.previous_bucket_option.bucket_number + 1

    @property
    def start_date(self):
        """
        If I'm the first bucket I start on the base date (the date of my context).  If I'm
        subsequent bucket I start on the day after the end of the previous bucket.
        """
        if self.previous_bucket_option is None:
            return self.parent.base_date
        else:
            return self.previous_bucket_option.end_date + datetime.timedelta(days=1)

    @property
    def end_date(self):
        if self._end_date is None:
            self._end_date = self.ceiling.end_date_from(base_date=self.parent.base_date)
        return self._end_date

    def name(self):
        if self.previous_bucket_option:
            floor_string = self.previous_bucket_option.ceiling.ceiling_string() + " to "
        else:
            floor_string = "Zero to "
        return 'Maturity bucket {bucket_number}: {floor}{ceiling}'.format(
            bucket_number=self.bucket_number,
            floor=floor_string,
            ceiling=self.ceiling.ceiling_string(),
        )

    def display(self, prefix=""):
        target = prefix + self.name()
        if self.next_bucket_option:
            target += "\n" + self.next_bucket_option.display(prefix=prefix)
        return target

    def classification_dict(self):
        """
        I return the a dictionary containing my attributes of the sub class.
        """
        criterion_name = self.parent.criterion_name
        description_name = criterion_name + " description"
        target_dict = {
            criterion_name: self.name(),
            description_name: self.parent.description}
        return target_dict

    def option_for_dates(self, from_date, to_date):
        # print(str(self.full_name()))
        # print(">>From" + str(from_date) + ", to: " + str(to_date))
        # sanity checks ...
        if from_date is None or to_date is None or to_date < from_date:
            return None
        bucket_end_date = self.ceiling.end_date_from(base_date=from_date)
        if bucket_end_date is None or to_date <= bucket_end_date:
            return self
        else:
            return self.get_next_bucket_option().option_for_dates(from_date=from_date, to_date=to_date)

    def option_for(self, subject):
        return self.option_for_deal_lifetime(subject)
        # return self.option_for_maturity_date(subject)

    def option_for_deal_lifetime(self, subject):
        """
        I return myself if the, given a base of subject.from_date, the subject.to_date
        is beneath my ceiling.  Otherwise I delegate to the next bucket.
        """
        return self.option_for_dates(
            from_date=subject.from_date,
            to_date=subject.to_date,
        )

    def get_next_bucket_option(self):
        """
        This is the more assertive way of asking for the next bucket.  If I currently
        have no next bucket then I make one based on me.
        """
        if not self.next_bucket_option:
            my_class = type(self)
            new_bucket = my_class(
                parent=self.parent,
                bucket_ceilings=[self.ceiling.next_step(bucket_option=self)],
                previous_bucket_option=self)
            self._next_bucket_option = new_bucket
        return self.next_bucket_option

    def full_name(self):
        target = self.parent.full_name() + ' '
        target += self.name()
        return target


class ThresholdSpecification(object):
    """
    The rules and thresholds which determine if a sub-class is reportable.
    """
    def __init__(
            self,
            liquidity_criteria=None,
            liquid_thresholds=None,
            non_liquid_thresholds=None,
    ):
        self.liquidity_criteria = liquidity_criteria
        self.liquid_thresholds = liquid_thresholds or []
        self.non_liquid_thresholds = non_liquid_thresholds

    def summary_string(self):
        target_string = "ThresholdSpecification:"
        if self.liquidity_criteria:
            target_string += "\n >" + self.liquidity_criteria.summary_string()
        else:
            target_string += "\n >" + "No liquidity criteria"
        target_string += "\n-Liquid:"
        if self.liquid_thresholds:
            for liquid_threshold in self.liquid_thresholds:
                target_string += "\n>" + liquid_threshold.summary_string()
        else:
            target_string += "\n >" + "NONE"
        target_string += "\n-Non-liquid:"
        if self.non_liquid_thresholds:
            target_string += "\n >" + self.non_liquid_thresholds.summary_string()
        else:
            target_string += "\n >" + "NONE"
        return target_string


class LiquidityCriteria(object):
    """
    The rules which determine if a sub-class is deemed to be liquid or not.
    From the document (e.g. Table 5.1):
        "Each sub-class shall be determined not to have a liquid market as per
        Articles 6 and 8(1)(b) if it does not meet one or all of the following
        thresholds of the quantitative liquidity criteria. For sub-classes
        determined to have a liquid market the additional qualitative liquidity
        criterion, where applicable, shall be applied"
    """

    def __init__(
            self,
            average_daily_notional_amount=None,
            average_daily_number_of_trades=None,
            qualitative_liquidity_criterion=None):
        self.average_daily_notional_amount = average_daily_notional_amount
        self.average_daily_number_of_trades = average_daily_number_of_trades
        self.qualitative_liquidity_criterion = qualitative_liquidity_criterion

    def summary_string(self):
        target_string = 'LiquidityCriteria: ADNA={adna}, No.ofTrades={number}, Qualitative="{qualitative}".'.format(
            adna=self.average_daily_notional_amount or "None",
            number=self.average_daily_number_of_trades or "None",
            qualitative=self.qualitative_liquidity_criterion or "None",
        )
        return target_string


class ThresholdTable(object):
    """
    Text taken from RTS 2 (c.f Table 5.2):

    [Table for] pre-trade and post-trade SSTI and LIS thresholds for
    sub-classes determined to have a liquid market

    Transactions to be considered for the calculations of the thresholds
    ... calculation of thresholds should be performed for each sub-class of
    the sub-asset class considering the transactions executed on financial
    instruments belonging to the sub-class
    """

    def __init__(
            self,
            ssti_pre_trade,
            lis_pre_trade,
            ssti_post_trade,
            lis_post_trade,
            adna_floor=None):
        self.adna_floor = adna_floor
        self.ssti_pre_trade = ssti_pre_trade
        self.lis_pre_trade = lis_pre_trade
        self.ssti_post_trade = ssti_post_trade
        self.lis_post_trade = lis_post_trade

    def summary_string(self):
        target_string = \
            "ThresholdTable: " \
            "\n adna_floor={adna_floor}, " \
            "\n ssti_pre_trade={ssti_pre_trade}, " \
            "\n lis_pre_trade={lis_pre_trade}, " \
            "\n ssti_post_trade={ssti_post_trade}, " \
            "\n lis_post_trade={lis_post_trade}".format(
                    adna_floor=self.adna_floor,
                    ssti_pre_trade=self.ssti_pre_trade,
                    lis_pre_trade=self.lis_pre_trade,
                    ssti_post_trade=self.ssti_post_trade,
                    lis_post_trade=self.lis_post_trade,
                    )
        return target_string


class SumOfMoney(object):
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = locale.atoi(amount)

    def __repr__(self):
        return 'SumOfMoney("{currency}", {amount})'.format(
            currency=self.currency,
            amount=locale.format("%d", self.amount, grouping=True),
        )


class PreTrade(object):
    def __init__(self, trade_percentile=None, threshold_floor=None):
        self.trade_percentile = trade_percentile
        self.threshold_floor = threshold_floor

    def __repr__(self):
        return 'PreTrade(trade_percentile={percentile}, threshold_floor={floor})'.format(
            percentile=self.trade_percentile,
            floor=self.threshold_floor,
        )


class PostTrade(object):
    def __init__(self, trade_percentile=None, volume_percentile=None, threshold_floor=None):
        self.trade_percentile = trade_percentile
        self.volume_percentile = volume_percentile
        self.threshold_floor = threshold_floor

    def __repr__(self):
        return 'PostTrade(trade_percentile={trade_percentile}, ' \
               'volume_percentile={volume_percentile}, ' \
               'threshold_floor={floor})'.format(
                    trade_percentile=self.trade_percentile,
                    volume_percentile=self.volume_percentile,
                    floor=self.threshold_floor,
                    )
