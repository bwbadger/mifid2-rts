# mifid2-rts

This project implements an executable form of the MiFID II RTS (Regulatory Technical Standard) documents.

Here are some introductory videos:
* [An overview of the context and the objectives of the project](https://www.youtube.com/watch?v=kmV2jDNgH-Q).
* [How to download the code from GitHub and run it](https://youtu.be/Hoo31-LJi4s).

[MiFID (Markets in Financial Instruments Directive)](https://en.wikipedia.org/wiki/Markets_in_Financial_Instruments_Directive_2004) is EU law for the regulation of the financial industry.  The [original MiFID](http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32004L0039:EN:HTML) was introduced in 2004, and following the 2007/8 financial crisis a second version, [MiFID II](https://www.esma.europa.eu/policy-rules/mifid-ii-and-mifir), was introduced in 2014.

The regulator [ESMA (European Securities and Markets Authority)](https://en.wikipedia.org/wiki/European_Securities_and_Markets_Authority) have been entrusted with enacting MiFID II.  ESMA have produced documents which define what firms need to do to comply with MiFID II, a key set of which are the RTS (Regulatory Technical Standards) documents.  Here we are focused on the [final 14th July 2016 version of RTS 2](http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0583&rid=1).  An early 2015 draft of the full set of RTS documents can be read [here](https://www.esma.europa.eu/sites/default/files/library/2015/11/2015-esma-1464_annex_i_-_draft_rts_and_its_on_mifid_ii_and_mifir.pdf).

The code in this GitHub repository implements the taxonomies defined in RTS 2 Annex 3 and in RTS 23 table 2.

The hope is that we can use this code either as an example of, or as the basis of, a body of code which is a working executable model of all MiFID II Regulatory Technical Standards, together with a body of test data which can illustrate how the technical standards are intended to work in practice.

There are [some slides](https://docs.google.com/presentation/d/1sVgeO3IAO7ZMrbzAYWZtbu21MxFlESL0ONvJHUuFgBc/edit?usp=sharing) which present the the intent of the project.

If you would like to see some trivial examples of the code in use, just run rts2_annex3.py from the command line.  This will build the taxonomies and run a few simple example ‘trades’ through.  The module dumps a representation of the RTS 2 taxonomy and the test trade classifications to stdout.

Here is an example of building and classifying a sample deal:

```python
import datetime
import rts2_annex3

class SampleTrade(object):
    pass

sample_trade = SampleTrade()
sample_trade.asset_class_name = 'Foreign Exchange Derivatives'
sample_trade.sub_asset_class_name= 'Deliverable FX options (DO)'
sample_trade.underlying_currency_pair = ('GBP', 'USD')
sample_trade.from_date = datetime.date(2017, 8, 13)
sample_trade.to_date = datetime.date(2017, 10, 12)

sample_classification = rts2_annex3.class_root.classification_for(sample_trade)
sample_classification.classification_dict()
{
'RTS2 version': 'Brussels, 14.7.2016 C(2016) 4301 final ANNEXES 1 to 4', 
'Asset class': 'Foreign Exchange Derivatives', 
'Sub-asset class': 'Deliverable FX options (DO)', 
'Segmentation criterion 1 description': 'underlying currency pair defined as combination of the two currencies underlying the derivative contract', 
'Segmentation criterion 1': "('GBP', 'USD')", 
'Segmentation criterion 2 description': 'time to maturity bucket of the swap defined as follows:',
'Segmentation criterion 2': 'Maturity bucket 2: 1 week to 3 months', 
} 
```

